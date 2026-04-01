"""
voice_skill.py — Edge TTS Edition
Converts script JSON → MP3 using Microsoft Edge TTS (free, no API key).
Full English pipeline for AI x Crypto content.

Install: pip install edge-tts
Run    : python voice_skill.py                    <- auto
         python voice_skill.py script.json en     <- force English
"""

import json, os, sys, asyncio, re
from pathlib import Path
from datetime import datetime

try:
    import edge_tts
except ImportError:
    print("[ERROR] edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

# ── CONFIG ────────────────────────────────────────────────────────────────────
SCRIPT_FILE = "script_output.json"
OUTPUT_MP3  = "voice.mp3"
LOG_FILE    = "voice_log.json"

VOICES = {
    "en": {
        "main" : "en-US-AndrewNeural",   # natural, conversational
        "alt"  : "en-US-BrianNeural",    # deeper, suits cold/poetic tone
        "label": "English Male (Andrew)"
    }
}

RATE   = os.environ.get("TTS_RATE",   "-5%")
VOLUME = os.environ.get("TTS_VOLUME", "+0%")

# ── LANG DETECT ───────────────────────────────────────────────────────────────
def detect_lang(script: dict, override: str = "auto") -> str:
    """Always returns 'en' — pipeline is English-only."""
    if override in ["en", "id"]:
        return override
    return "en"

# ── TEXT CLEANER ──────────────────────────────────────────────────────────────
def clean_for_tts(text: str) -> str:
    """Normalize text before sending to TTS."""
    # Strip markdown symbols
    text = re.sub(r'[#*_~`]', '', text)
    # Strip URLs
    text = re.sub(r'https?://\S+', '', text)
    # Normalize number formats
    text = re.sub(r'\$(\d+)B\b', r'\1 billion dollars', text)
    text = re.sub(r'\$(\d+)M\b', r'\1 million dollars', text)
    text = re.sub(r'\$(\d+)K\b', r'\1 thousand dollars', text)
    text = re.sub(r'\$(\d+)',    r'\1 dollars', text)
    text = re.sub(r'(\d+)%',    r'\1 percent', text)
    text = re.sub(r'(\d+)x\b',  r'\1 times', text)
    text = re.sub(r'(\d+)K\b',  r'\1 thousand', text)
    # Clean double spaces
    text = re.sub(r' +', ' ', text).strip()
    return text

# ── BUILD NARRATION ───────────────────────────────────────────────────────────
def build_narration(script: dict) -> str:
    """Assemble full narration from script JSON with cinematic pauses."""
    parts = []

    hook = script.get("hook", "").strip()
    if hook:
        parts.append(hook)

    for scene in script.get("scenes", []):
        text = scene.get("text", "").strip()
        if text:
            parts.append(text)

    cta = script.get("cta", "").strip()
    if cta:
        parts.append(cta)

    # "... " between sections = ~0.5s natural pause each
    raw = "... ".join(parts) + "."
    return clean_for_tts(raw)

# ── TTS ENGINE ────────────────────────────────────────────────────────────────
async def generate_edge_tts(text: str, voice: str, output: str):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=RATE, volume=VOLUME)
    await communicate.save(output)

def run_tts(text: str, voice: str, output: str):
    asyncio.run(generate_edge_tts(text, voice, output))

def load_script(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] Script file not found: {path}")
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def upgrade_audio(mp3_path: str):
    """Upgrade 48kbps mono → 128kbps stereo 44.1kHz."""
    import shutil, subprocess
    tmp = mp3_path.replace(".mp3", "_hq.mp3")
    result = subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path,
        "-codec:a", "libmp3lame",
        "-b:a", "128k",
        "-ac", "2",
        "-ar", "44100",
        tmp
    ], capture_output=True)
    if result.returncode == 0:
        shutil.move(tmp, mp3_path)
        print(f"[voice] Upgraded → 128kbps stereo 44.1kHz")
    else:
        print(f"[voice] Audio upgrade skipped (ffmpeg error)")

# ── MAIN ─────────────────────────────────────────────────────────────────────
def run(script_path: str = SCRIPT_FILE, lang_override: str = "auto"):
    print("\n" + "="*55)
    print("VOICE SKILL — Edge TTS")
    print("="*55)

    script = load_script(script_path)
    lang   = detect_lang(script, lang_override)
    voice  = VOICES["en"]["main"]
    label  = VOICES["en"]["label"]
    text   = build_narration(script)

    print(f"[voice] Lang    : {lang.upper()} — {label}")
    print(f"[voice] Voice   : {voice}")
    print(f"[voice] Rate    : {RATE}")
    print(f"[voice] Preview : {text[:120]}...")
    print(f"[voice] Generating...")

    try:
        run_tts(text, voice, OUTPUT_MP3)
    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")
        print("[voice] Trying alt voice...")
        try:
            alt = VOICES["en"]["alt"]
            run_tts(text, alt, OUTPUT_MP3)
            voice = alt
        except Exception as e2:
            print(f"[ERROR] Alt voice also failed: {e2}")
            sys.exit(1)

    upgrade_audio(OUTPUT_MP3)

    size_kb = Path(OUTPUT_MP3).stat().st_size / 1024
    print(f"[voice] Saved   → {OUTPUT_MP3} ({size_kb:.1f} KB)")

    log = {
        "generated_at"  : datetime.now().isoformat(),
        "source_script" : script_path,
        "lang"          : lang,
        "voice"         : voice,
        "rate"          : RATE,
        "narration_text": text,
        "output_file"   : OUTPUT_MP3
    }
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"[voice] Log     → {LOG_FILE}")
    print("="*55)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else SCRIPT_FILE
    lang = sys.argv[2] if len(sys.argv) > 2 else "auto"
    run(path, lang)

