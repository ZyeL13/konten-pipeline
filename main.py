"""
main.py — OpenClaw entry point
Guaranteed terminal output + robust logging init.
"""
import sys
import json
import logging
import argparse
from pathlib import Path

# ── LOGGING (WAJIB DI SINI, SEBELUM IMPORT MODUL LAIN) ───────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    force=True  # Paksa reset konfigurasi logger yang sudah ada
)
log = logging.getLogger("main")

# ── ARGS ─────────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(prog="openclaw", description="OpenClaw Pipeline")
parser.add_argument("--run-queue", action="store_true", help="Process queue")
parser.add_argument("--scan",      action="store_true", help="Run news scanner")
parser.add_argument("--job",       type=str, default=None, help="Re-run job by ID prefix")
parser.add_argument("--max",       type=int, default=None, help="Max jobs to process")
parser.add_argument("--debug",     action="store_true", help="Debug mode")
args = parser.parse_args()

# ── HELPERS ──────────────────────────────────────────────────────────────────
def load_queue() -> list:
    q = Path("data/queue.json")
    if not q.exists():
        return []
    with open(q, "r", encoding="utf-8") as f:
        return json.load(f)

def run_queue():
    print("🔄 [MAIN] Loading queue...")
    from core.orchestrator import run_job
    
    queue = load_queue()
    pending = [j for j in queue if j.get("status") == "pending"]
    
    if not pending:
        print("✅ [MAIN] Queue kosong — tidak ada job pending.")
        return

    limit = args.max or len(pending)
    to_process = pending[:limit]
    print(f"📦 [MAIN] {len(pending)} job pending. Processing {len(to_process)}.\n")    
    for job in to_process:
        brief = job.get("brief_technical", job.get("headline", "No brief"))[:60]
        print(f"🚀 [MAIN] Running Job {job['id'][:8]} — {brief}")
        print("-" * 50)
        success = run_job(job)
        status = "✅ DONE" if success else "❌ FAILED"
        print(f"🏁 [MAIN] Job {job['id'][:8]} finished: {status}")
        print("=" * 50 + "\n")

def run_scanner():
    print("📡 [MAIN] Starting news scanner...")
    try:
        import news_scanner
        news_scanner.run()
    except ImportError:
        print("❌ [MAIN] news_scanner.py not found.")
        sys.exit(1)

def run_specific_job(job_id_prefix: str):
    print(f"🔄 [MAIN] Resuming job prefix: {job_id_prefix}")
    try:
        from core.orchestrator import run_job
        from core import job_queue as core_queue
    except ImportError as e:
        print(f"❌ [MAIN] Import failed: {e}")
        sys.exit(1)

    queue = load_queue()
    matches = [j for j in queue if j.get("id", "").startswith(job_id_prefix)]
    if not matches:
        print(f"❌ [MAIN] Job '{job_id_prefix}' not found.")
        sys.exit(1)

    job = matches[0]
    print(f"🛠️ [MAIN] Resetting & running {job['id'][:8]}...")
    core_queue.update(job["id"], status="pending", steps={s: False for s in job.get("steps", {})}, retry_count=0)
    run_job(job)

# ── ENTRY POINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🦞 OPENCLAW PIPELINE STARTING")
    if args.run_queue:
        run_queue()
    elif args.scan:
        run_scanner()
    elif args.job:
        run_specific_job(args.job)
    else:
        print("💬 Launching Intent Bot...")
        import subprocess
        subprocess.run([sys.executable, "intent_bot.py"] + (["--debug"] if args.debug else []))
