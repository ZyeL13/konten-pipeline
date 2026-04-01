"""
run_pipeline.py — Fixed with step guards
Setiap run punya output folder: output/YYYYMMDD_HHMMSS/

Run: python run_pipeline.py "headline" --lang id --tone 1
     python run_pipeline.py  ← pakai default topic
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# ── ARGS ─────────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("headline", nargs="?", default="AI agent cari uang sendiri")
parser.add_argument("--lang",  default="auto", help="en")
parser.add_argument("--tone",  default=1, type=int, help="Nomor tone 1-10")
parser.add_argument("--skip-visual", action="store_true")
args = parser.parse_args()

# ── RUN DIR ───────────────────────────────────────────────────────────────────
RUN_ID  = datetime.now().strftime("%Y%m%d_%H%M%S")
RUN_DIR = Path("output") / RUN_ID
RUN_DIR.mkdir(parents=True, exist_ok=True)
(RUN_DIR / "scenes").mkdir(exist_ok=True)

def step(label):
    print(f"\n{'─'*50}\n▶  {label}\n{'─'*50}")

def copy_if_exists(src, dst):
    if Path(src).exists():
        shutil.copy(src, dst)
        return True
    return False

def abort(reason):
    print(f"\n[ABORT] {reason}")
    print(f"[ABORT] Run {RUN_ID} dihentikan.")
    sys.exit(1)

print(f"\n{'='*55}")
print(f"🚀  PIPELINE RUN: {RUN_ID}")
print(f"    Headline : {args.headline}")
print(f"    Tone     : #{args.tone}")
print(f"    Lang     : {args.lang}")
print(f"    Output   : {RUN_DIR}")
print(f"{'='*55}")
start = datetime.now()

# ── STEP 1 — Variations ───────────────────────────────────────────────────────
step("STEP 1 — Generate 10 variasi script")
subprocess.run(["python", "variation_skill.py", args.headline])

if not Path("variations_output.json").exists():
    abort("variations_output.json tidak ada — cek error di atas")
copy_if_exists("variations_output.json", RUN_DIR / "variations_output.json")
print("[OK] Step 1 done")

# ── STEP 2 — Pick tone ────────────────────────────────────────────────────────
step(f"STEP 2 — Pick tone #{args.tone}")
subprocess.run(["python", "pick_variation.py", str(args.tone)])

if not Path("script_output.json").exists():
    abort("script_output.json tidak ada — cek pick_variation.py")
copy_if_exists("script_output.json", RUN_DIR / "script_output.json")
print("[OK] Step 2 done")

# ── STEP 3 — Voice ────────────────────────────────────────────────────────────
step(f"STEP 3 — Generate voice ({args.lang})")
subprocess.run(["python", "voice_skill.py", "script_output.json", args.lang])

if not Path("voice.mp3").exists():
    abort("voice.mp3 tidak ada — cek voice_skill.py")
copy_if_exists("voice.mp3", RUN_DIR / "voice.mp3")
print("[OK] Step 3 done")

# ── STEP 4 — Visuals ──────────────────────────────────────────────────────────
if not args.skip_visual:
    step("STEP 4 — Generate visuals")
    subprocess.run(["python", "visual_skill.py", "script_output.json"])

    scenes_ok = list(Path("scenes").glob("*.png"))
    if not scenes_ok:
        abort("Tidak ada scene PNG — cek visual_skill.py")
    for png in scenes_ok:
        shutil.copy(png, RUN_DIR / "scenes" / png.name)
    print(f"[OK] Step 4 done — {len(scenes_ok)} scenes")
else:
    print("[SKIP] Visual generation")

# ── STEP 5 — Edit ─────────────────────────────────────────────────────────────
step("STEP 5 — Assemble video")
subprocess.run(["python", "edit_skill.py", "script_output.json"])

if not Path("final_video.mp4").exists():
    abort("final_video.mp4 tidak ada — cek edit_skill.py")
copy_if_exists("final_video.mp4", RUN_DIR / "final_video.mp4")
print("[OK] Step 5 done")

# ── CLEANUP root generated files ──────────────────────────────────────────────
for f in ["variations_output.json", "script_output.json", "voice.mp3",
          "voice_log.json", "visual_log.json", "final_video.mp4"]:
    Path(f).unlink(missing_ok=True)

# ── DONE ──────────────────────────────────────────────────────────────────────
elapsed = (datetime.now() - start).seconds
log = {
    "run_id"   : RUN_ID,
    "headline" : args.headline,
    "tone"     : args.tone,
    "lang"     : args.lang,
    "elapsed_s": elapsed,
    "output"   : str(RUN_DIR)
}
with open(RUN_DIR / "run_log.json", "w") as f:
    json.dump(log, f, indent=2)

print(f"\n{'='*55}")
print(f"✅  DONE: {RUN_ID} ({elapsed}s)")
print(f"    📁 {RUN_DIR}/")
print(f"       ├── variations_output.json")
print(f"       ├── script_output.json")
print(f"       ├── voice.mp3")
print(f"       ├── final_video.mp4")
print(f"       └── scenes/")
print(f"{'='*55}")

import subprocess
subprocess.run(["bash", "/data/data/com.termux/files/home/kirim.sh"])
