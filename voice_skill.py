"""
voice_skill.py — Edge TTS Edition
Converts script JSON → MP3 menggunakan Microsoft Edge TTS.
Gratis, no API key, kualitas jauh di atas gTTS.
Support Indonesian + English dengan suara natural.

Install: pip install edge-tts asyncio
Run    : python voice_skill.py              ← auto detect bahasa
         python voice_skill.py script.json id    ← force Indonesian
         python voice_skill.py script.json en    ← force English
"""

import json
import os
import sys
import asyncio
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

try:
    import edge_tts
except ImportError:
    print("[ERROR] edge-tts belum diinstall.")
    print("  pip install edge-tts")
    sys.exit(1)

# ── CONFIG ────────────────────────────────────────────────────────────────────
SCRIPT_FILE = "script_output.json"
OUTPUT_MP3  = "voice.mp3"
LOG_FILE    = "voice_log.json"

# Voice options
VOICES = {
    "id": {
        "main"    : "id-ID-ArdiNeural",      # Male, natural Indonesian
        "alt"     : "id-ID-GadisNeural",     # Female, natural Indonesian
        "label"   : "Indonesian Male (Ardi)"
    },
    "en": {
        "main"    : "en-US-ChristopherNeural", # Deep male, cinematic
        "alt"     : "en-US-GuyNeural",         # Clear male
        "label"   : "English Male (Christopher)"
    }
}

# Pilih bahasa: "id" | "en" | "auto"
LANG = os.environ.get("TTS_LANG", "auto")

# Rate: speaking speed. "-10%" = sedikit lebih lambat (cinematic)
RATE   = os.environ.get("TTS_RATE", "-10%")

# Volume: "+0%" = normal
VOLUME = os.environ.get("TTS_VOLUME", "+0%")

# ── HELPERS ───────────────────────────────────────────────────────────────────
def load_script(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] Script file tidak ada: {path}")
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def detect_lang(script: dict, override: str = "auto") -> str:
    if override in ["id", "en"]:
        return override

    # Auto detect dari hashtags / caption
    text = " ".join([
        script.get("hook", ""),
        *[s.get("text", "") for s in script.get("scenes", [])],
        script.get("cta", "")
    ]).lower()

    id_signals = ["yang", "dan", "dengan", "untuk", "ini", "itu",
                  "bisa", "tidak", "sudah", "akan", "dari", "kamu"]
    id_count   = sum(1 for w in id_signals if w in text)

    return "id" if id_count >= 3 else "en"

def build_narration(script: dict, lang: str) -> str:
    """
    Bangun narasi full dari script.
    Edge TTS support SSML tapi kita pakai plain text + punctuation saja.
    """
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

    # Gabung dengan titik untuk pause natural
    return ". ".join(parts) + "."

async def generate_edge_tts(text: str, voice: str, output: str):
    """Async Edge TTS generation."""
    communicate = edge_tts.Communicate(
        text   = text,
        voice  = voice,
        rate   = RATE,
        volume = VOLUME
    )
    await communicate.save(output)

def run_tts(text: str, voice: str, output: str):
    """Wrapper untuk run async dari sync context."""
    asyncio.run(generate_edge_tts(text, voice, output))

# ── MAIN ─────────────────────────────────────────────────────────────────────
def run(script_path: str = SCRIPT_FILE, lang_override: str = "auto"):
    print("\n" + "="*55)
    print("🎙️  VOICE SKILL — Edge TTS (Microsoft, Free)")
    print("="*55)

    script  = load_script(script_path)
    lang    = detect_lang(script, lang_override)
    voice   = VOICES[lang]["main"]
    label   = VOICES[lang]["label"]
    text    = build_narration(script, lang)

    print(f"[voice_skill] Lang   : {lang.upper()} — {label}")
    print(f"[voice_skill] Voice  : {voice}")
    print(f"[voice_skill] Rate   : {RATE}")
    print(f"[voice_skill] Text   : {text[:100]}...")
    print(f"[voice_skill] Generating...")

    try:
        run_tts(text, voice, OUTPUT_MP3)
    except Exception as e:
        print(f"[ERROR] Edge TTS gagal: {e}")
        print("  Cek koneksi internet.")
        sys.exit(1)

    size_kb = Path(OUTPUT_MP3).stat().st_size / 1024
    print(f"[OK] MP3 saved → {OUTPUT_MP3} ({size_kb:.1f} KB)")

    # Log
    log = {
        "generated_at"  : datetime.now().isoformat(),
        "source_script" : script_path,
        "engine"        : "edge-tts",
        "lang"          : lang,
        "voice"         : voice,
        "rate"          : RATE,
        "narration_text": text,
        "output_file"   : OUTPUT_MP3
    }
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"[voice_skill] Log → {LOG_FILE}")
    print(f"\nGanti voice:")
    print(f"  Indo female : export TTS_VOICE=alt → edit VOICES['id']['main'] ke 'id-ID-GadisNeural'")
    print(f"  English     : python voice_skill.py script_output.json en")
    print(f"  Lebih lambat: export TTS_RATE='-20%'")
    print("="*55)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else SCRIPT_FILE
    lang = sys.argv[2] if len(sys.argv) > 2 else "auto"
    run(path, lang)

