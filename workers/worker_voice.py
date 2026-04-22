"""
workers/worker_voice.py — Voice worker.
"""
import json
import logging
import subprocess
import shutil
import time
from pathlib import Path
from datetime import datetime
from agents.voice_agent import generate, build_narration
from core.config import TTS_VOICE

log = logging.getLogger("worker.voice")
MAX_RETRIES = 2
ALT_VOICE = "en-US-DavisNeural"

def _upgrade_audio(mp3: Path):
    tmp = mp3.with_suffix(".hq.mp3")
    res = subprocess.run(["ffmpeg", "-y", "-i", str(mp3), "-codec:a", "libmp3lame", "-b:a", "128k", "-ac", "2", "-ar", "44100", str(tmp)], capture_output=True)
    if res.returncode == 0: shutil.move(str(tmp), str(mp3)); log.info("Audio upgraded → 128kbps")
    else: tmp.unlink(missing_ok=True)

def run(script_data: dict, lang: str, run_dir: Path) -> bool:
    voice_file = run_dir / "voice.mp3"
    narration = build_narration(script_data)
    log.info(f"Generating voice — words={len(narration.split())} voice={TTS_VOICE}")

    audio = None
    for v in [TTS_VOICE, ALT_VOICE]:
        for r in range(MAX_RETRIES):
            try: audio = generate(narration, voice=v)
            except: audio = None
            if audio: break
            log.warning(f"TTS attempt {r+1}/{MAX_RETRIES} failed"); time.sleep(5)
        if audio: break

    if not audio: log.error("All voice attempts failed"); return False
    with open(voice_file, "wb") as f: f.write(audio)
    log.info(f"voice.mp3 saved ({len(audio)/1024:.0f} KB)")
    _upgrade_audio(voice_file)
    return True
