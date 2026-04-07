#!/usr/bin/env python3
"""
healer_llm_upgraded.py — Self-Healing Router with LLM (ClawRouter/deepseek)
Fitur:
- Watchdog: restart main.py jika mati atau hang
- Fast path + LLM fallback
- Cooldown & rate limiting
- Heartbeat monitoring
- Dry-run & auto-fix mode
"""

import os
import re
import sys
import json
import time
import logging
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List

# ========== KONFIGURASI ==========
CLAWROUTER_URL = "http://127.0.0.1:8402/v1/chat/completions"
MODEL = "free/deepseek-v3.2"
MAX_RETRIES = 3
RETRY_DELAY = 2

# Watchdog
WATCH_INTERVAL = 30          # detik
PROCESS_NAME = "main.py"     # nama proses yang dipantau
HEARTBEAT_FILE = Path("/tmp/konten_heartbeat")  # file heartbeat (optional)
HEARTBEAT_TIMEOUT = 120      # jika heartbeat > 120 detik, dianggap hang
COOLDOWN_FIX = 300            # minimal 5 menit antar fix otomatis
COOLDOWN_RESTART = 60         # minimal 1 menit antar restart

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("healer")

# ========== FAST PATH (hardcoded untuk error umum) ==========
FAST_FIXES = {
    r"KeyError: 'id'": {
        "cmd": 'sed -i "s/s\\[\'id\'\\]/s.get(\'id\', s.get(\'scene\', idx))/g" workers/worker_edit.py && sed -i "s/scene\\[\'id\'\\]/scene.get(\'id\', scene.get(\'scene\', i))/g" workers/worker_visual.py',
        "desc": "Fix KeyError: 'id' → use get() with fallback"
    },
    r"FileNotFoundError.*kirim\.sh": {
        "cmd": 'sed -i \'s/subprocess\\.run(\\["bash", str(kirim), str(run_dir)\\])/log.warning("kirim.sh not found")/g\' core/orchestrator.py',
        "desc": "Disable kirim.sh call"
    },
    r"ModuleNotFoundError: No module named '([^']+)'": {
        "cmd": "pip install {match[1]}",
        "desc": "Install missing module"
    },
    r"JSONDecodeError|Expecting value": {
        "cmd": 'python -c "import json, glob; [open(f,\'w\').write(json.dumps({\"scenes\":[]})) for f in glob.glob(\'output/*/script_output.json\')]"',
        "desc": "Reset corrupted JSON"
    },
    r"(rate limit|429|Too Many Requests)": {
        "cmd": "echo 'Rate limit hit, waiting 60s' && sleep 60",
        "desc": "Wait for rate limit"
    },
    r"ffmpeg.*(not found|No such file)": {
        "cmd": "pkg install ffmpeg -y 2>/dev/null || apt install ffmpeg -y",
        "desc": "Install ffmpeg"
    },
}

# ========== UTILITY ==========
def run_cmd(cmd: str, timeout: int = 30) -> Tuple[bool, str]:
    """Jalankan shell command, return (success, output)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stderr or result.stdout
    except Exception as e:
        return False, str(e)

def get_error_context(log_file: Path = None, lines_before: int = 5, lines_after: int = 3) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Extract error line, surrounding context, and code snippet."""
    if log_file is None:
        candidates = ["logs/pipeline.log", "nohup.out", "error.log", "log.txt"]
        for c in candidates:
            p = Path(c)
            if p.exists():
                log_file = p
                break
    if not log_file or not log_file.exists():
        return None, None, None

    content = log_file.read_text(errors='ignore')
    lines = content.splitlines()
    error_idx = -1
    error_line = ""

    for i in range(len(lines)-1, -1, -1):
        line = lines[i]
        if any(kw in line for kw in ["Error", "Exception", "Traceback", "KeyError", "FileNotFoundError"]):
            error_idx = i
            error_line = line
            break

    if error_idx == -1:
        return None, None, None

    start = max(0, error_idx - lines_before)
    end = min(len(lines), error_idx + lines_after + 1)
    context = "\n".join(lines[start:end])

    # Ambil code snippet dari traceback
    code_snippet = ""
    file_match = re.search(r'File "([^"]+\.py)", line (\d+)', context)
    if file_match:
        file_path = file_match.group(1)
        line_num = int(file_match.group(2))
        if Path(file_path).exists():
            code_lines = Path(file_path).read_text(errors='ignore').splitlines()
            start_code = max(0, line_num - 5)
            end_code = min(len(code_lines), line_num + 5)
            code_snippet = "\n".join(f"{i+1}: {code_lines[i]}" for i in range(start_code, end_code))

    return error_line, context, code_snippet

# ========== LLM CALL ==========
def ask_llm(prompt: str, error_context: str = "") -> str:
    """Kirim prompt ke ClawRouter, return fix suggestion."""
    system_prompt = """You are a self-healing assistant for a Python video pipeline (konten project).
Given an error and code context, suggest ONE SPECIFIC bash command or python one-liner to fix it.

Rules:
- Output ONLY the command, no extra text, no markdown.
- If unsure, output: echo "MANUAL: describe what to check"
- For KeyError: use sed to replace dictionary access with .get()
- For missing file: create it with default content
- For process crash: suggest restart command
- Always prefer non-destructive fixes.

Examples:
sed -i "s/old/new/g" file.py
pip install requests
python -c "import json; Path('data/queue.json').write_text('[]')"
echo "MANUAL: check line 42 in worker_edit.py"
"""

    user_prompt = f"""
ERROR CONTEXT (last few lines):
{error_context[:1200]}

RELEVANT CODE SNIPPET (if any):
{prompt[:800]}

OUTPUT ONLY THE FIX COMMAND:
"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(CLAWROUTER_URL, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                log.warning(f"LLM attempt {attempt+1}: HTTP {resp.status_code}")
        except Exception as e:
            log.warning(f"LLM attempt {attempt+1}: {e}")
        time.sleep(RETRY_DELAY)
    return "echo 'LLM unavailable; manual fix needed'"

# ========== FIX EXECUTION ==========
def apply_fix(cmd: str, dry_run: bool = True) -> bool:
    """Apply fix command, return success."""
    if not cmd or cmd.startswith("echo 'MANUAL"):
        log.info(f"   [SKIP] {cmd[:80]}")
        return False

    log.info(f"   🔧 Fix: {cmd[:200]}")
    if dry_run:
        log.info("   [DRY RUN] Not executed")
        return True

    # Python one-liner via -c
    if cmd.startswith("python -c"):
        code = cmd[9:].strip().strip('"').strip("'")
        try:
            exec(code)
            log.info("   ✓ Executed (python -c)")
            return True
        except Exception as e:
            log.error(f"   ✗ Failed: {e}")
            return False

    # Regular shell command
    success, output = run_cmd(cmd)
    if success:
        log.info("   ✓ Executed")
    else:
        log.error(f"   ✗ Failed: {output[:200]}")
    return success

def smart_heal(dry_run: bool = True, auto_fix: bool = False) -> bool:
    """Auto-detect error and heal."""
    error_line, context, code_snippet = get_error_context()
    if not error_line:
        log.info("✅ No error found in logs")
        return True

    log.warning(f"🔍 Error detected: {error_line[:100]}")
    cmd = None
    matched_desc = None

    # Fast path
    for pattern, recipe in FAST_FIXES.items():
        m = re.search(pattern, error_line, re.IGNORECASE)
        if m:
            cmd = recipe["cmd"]
            matched_desc = recipe["desc"]
            # Jika ada placeholder {match[1]}, substitusi
            if "{match[1]}" in cmd and m.groups():
                cmd = cmd.format(match=m)
            log.info(f"⚡ Fast fix: {matched_desc}")
            break

    # Fallback ke LLM
    if not cmd:
        log.info("🤔 No fast match, asking LLM...")
        cmd = ask_llm(code_snippet, context)
        if cmd:
            log.info(f"💡 LLM suggestion: {cmd[:100]}")

    if not cmd:
        log.error("❌ No fix generated")
        return False

    return apply_fix(cmd, dry_run=not auto_fix)

# ========== WATCHDOG ==========
def is_process_running(proc_name: str) -> bool:
    """Cek apakah process dengan nama tertentu berjalan."""
    result = subprocess.run(["pgrep", "-f", proc_name], capture_output=True)
    return bool(result.stdout.strip())

def check_heartbeat() -> bool:
    """Cek file heartbeat; return False jika terlalu tua atau tidak ada."""
    if not HEARTBEAT_FILE.exists():
        return True  # tidak wajib
    age = time.time() - HEARTBEAT_FILE.stat().st_mtime
    return age < HEARTBEAT_TIMEOUT

def restart_pipeline():
    """Restart main.py (kill existing, start baru)."""
    log.warning("🔄 Restarting pipeline...")
    # Kill existing
    subprocess.run(["pkill", "-f", "main.py"], capture_output=True)
    time.sleep(2)
    # Start baru
    subprocess.Popen(["python", "main.py", "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log.info("✅ Pipeline restarted")

def watch_and_heal():
    """Main watchdog loop."""
    log.info(f"🐛 Self-Healing Watchdog active")
    log.info(f"   Check interval: {WATCH_INTERVAL}s")
    log.info(f"   Process: {PROCESS_NAME}")
    log.info(f"   Cooldown fix: {COOLDOWN_FIX}s | restart: {COOLDOWN_RESTART}s")

    last_fix_time = 0
    last_restart_time = 0
    last_error_line = ""

    while True:
        time.sleep(WATCH_INTERVAL)
        now = time.time()

        # 1. Cek heartbeat (hang)
        if HEARTBEAT_FILE.exists() and not check_heartbeat():
            log.warning("💀 Heartbeat stale → pipeline mungkin hang")
            if now - last_restart_time > COOLDOWN_RESTART:
                restart_pipeline()
                last_restart_time = now
            continue

        # 2. Cek apakah process mati
        if not is_process_running(PROCESS_NAME):
            log.warning("💀 Main process not running")
            if now - last_restart_time > COOLDOWN_RESTART:
                restart_pipeline()
                last_restart_time = now
            continue

        # 3. Cek error di log (cooldown)
        error_line, _, _ = get_error_context()
        if error_line and error_line != last_error_line and (now - last_fix_time) > COOLDOWN_FIX:
            log.info(f"⚠️ New error detected: {error_line[:80]}")
            # Jalankan healing (dry-run=False hanya jika auto_fix=True)
            # Di watchdog, kita auto-fix karena sudah mode --watch
            success = smart_heal(dry_run=False, auto_fix=True)
            if success:
                last_fix_time = now
                last_error_line = error_line
            else:
                log.warning("Healing failed, will retry later")
        elif error_line and error_line == last_error_line:
            # error sama, jangan spam
            pass

# ========== MAIN ==========
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Self-Healing Router for konten (upgraded)")
    parser.add_argument("--fix", action="store_true", help="Auto-apply fix for last error")
    parser.add_argument("--watch", action="store_true", help="Watchdog mode (auto-restart & heal)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--error", type=str, help="Manually specify error line")
    parser.add_argument("--code", type=str, help="Manually specify code snippet")
    args = parser.parse_args()

    if args.watch:
        watch_and_heal()
        return

    if args.error:
        # Manual mode
        error_line = args.error
        code_snippet = args.code or ""
        cmd = None
        for pattern, recipe in FAST_FIXES.items():
            if re.search(pattern, error_line, re.IGNORECASE):
                cmd = recipe["cmd"]
                log.info(f"⚡ Fast fix: {recipe['desc']}")
                break
        if not cmd and code_snippet:
            log.info("🤔 Asking LLM...")
            cmd = ask_llm(code_snippet, error_line)
        if cmd:
            apply_fix(cmd, dry_run=not args.fix)
        else:
            log.error("No fix available")
        return

    # Auto-detect mode
    smart_heal(dry_run=not args.fix, auto_fix=args.fix)

if __name__ == "__main__":
    main()
