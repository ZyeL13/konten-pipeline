"""
edit_skill.py
Assembles scenes + voice → final video menggunakan FFmpeg.
- Ken Burns zoom effect per scene
- Voice sync
- Subtitle overlay dari script text
- Output: final_video.mp4 (720x1280, 9:16)

Requires: pkg install ffmpeg
Run     : python edit_skill.py
"""

import subprocess
import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────────────────────
SCRIPT_FILE  = "script_output.json"
SCENES_DIR   = "scenes"
VOICE_FILE   = "voice.mp3"
OUTPUT_FILE  = "final_video.mp4"
TEMP_DIR     = "tmp_edit"

WIDTH        = 720
HEIGHT       = 1280
FPS          = 30

# Subtitle style
FONT_SIZE    = 22
FONT_COLOR   = "white"
BOX_COLOR    = "black@0.5"  # semi-transparent background

# ── HELPERS ───────────────────────────────────────────────────────────────────
def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("[ERROR] FFmpeg tidak ada.")
        print("  pkg install ffmpeg")
        sys.exit(1)
    print("[OK] FFmpeg found")

def load_script(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] {path} tidak ada.")
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def check_assets(scenes: list) -> bool:
    ok = True
    for s in scenes:
        sid  = s.get("id")
        path = os.path.join(SCENES_DIR, f"scene_{sid}.png")
        if not Path(path).exists():
            print(f"[ERROR] Missing: {path}")
            ok = False
    if not Path(VOICE_FILE).exists():
        print(f"[ERROR] Missing: {VOICE_FILE}")
        ok = False
    return ok

def get_audio_duration(path: str) -> float:
    """Get MP3 duration via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0", path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 61.0  # fallback

def make_scene_clip(scene: dict, audio_duration: float, total_scenes: int) -> str:
    """
    Convert PNG → video clip dengan Ken Burns zoom effect.
    Duration = audio_duration / total_scenes (equal split)
    """
    sid       = scene.get("id")
    duration  = audio_duration / total_scenes
    img_path  = os.path.join(SCENES_DIR, f"scene_{sid}.png")
    out_path  = os.path.join(TEMP_DIR, f"clip_{sid}.mp4")

    # Ken Burns: slow zoom in dari 1.0 ke 1.05
    # zoompan filter: zoom tiap frame naik 0.0005, max 1.05x
    zoom_speed = 0.0005
    total_frames = int(duration * FPS)

    vf = (
        f"scale={WIDTH*2}:{HEIGHT*2},"
        f"zoompan=z='min(zoom+{zoom_speed},1.05)':"
        f"d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={WIDTH}x{HEIGHT}:fps={FPS},"
        f"format=yuv420p"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", img_path,
        "-vf", vf,
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        out_path
    ]

    print(f"  [clip_{sid}] {duration:.1f}s Ken Burns zoom...")
    result = subprocess.run(cmd, capture_output=True, timeout=120)

    if result.returncode != 0:
        print(f"  [ERROR] clip_{sid} failed:")
        print(result.stderr.decode()[-300:])
        return None

    print(f"  [OK] clip_{sid}.mp4")
    return out_path

def concat_clips(clip_paths: list) -> str:
    """Gabung semua clip jadi satu video."""
    list_file = os.path.join(TEMP_DIR, "clips.txt")
    with open(list_file, "w") as f:
        for p in clip_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")

    concat_path = os.path.join(TEMP_DIR, "concat.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        concat_path
    ]
    print("\n  [concat] Joining clips...")
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    if result.returncode != 0:
        print("[ERROR] Concat failed:")
        print(result.stderr.decode()[-300:])
        return None
    print("  [OK] concat.mp4")
    return concat_path

def add_audio(video_path: str, audio_path: str) -> str:
    """Merge video + voice audio."""
    out_path = os.path.join(TEMP_DIR, "with_audio.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        out_path
    ]
    print("  [audio] Adding voice...")
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    if result.returncode != 0:
        print("[ERROR] Audio merge failed:")
        print(result.stderr.decode()[-300:])
        return None
    print("  [OK] with_audio.mp4")
    return out_path

def add_subtitles(video_path: str, scenes: list, audio_duration: float) -> str:
    """
    Burn subtitle text per scene menggunakan drawtext filter.
    Setiap scene: text muncul di bawah tengah layar.
    """
    total_scenes = len(scenes)
    scene_dur    = audio_duration / total_scenes

    # Build drawtext chain
    filters = []
    for i, scene in enumerate(scenes):
        start  = i * scene_dur
        end    = start + scene_dur - 0.3  # fade out sedikit sebelum scene end
        text   = scene.get("text", "").replace("'", "\\'").replace(":", "\\:")
        if not text:
            continue

        # Wrap text kalau panjang (max ~35 char per baris)
        if len(text) > 35:
            words  = text.split()
            mid    = len(words) // 2
            line1  = " ".join(words[:mid]).replace("'", "\\'")
            line2  = " ".join(words[mid:]).replace("'", "\\'")
            text   = f"{line1}\\n{line2}"

        dt = (
            f"drawtext=text='{text}':"
            f"fontsize={FONT_SIZE}:"
            f"fontcolor={FONT_COLOR}:"
            f"box=1:boxcolor={BOX_COLOR}:boxborderw=8:"
            f"x=(w-text_w)/2:"
            f"y=h-text_h-80:"
            f"enable='between(t,{start:.2f},{end:.2f})'"
        )
        filters.append(dt)

    vf = ",".join(filters) if filters else "null"

    out_path = OUTPUT_FILE
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "copy",
        out_path
    ]
    print("  [subtitle] Burning text overlays...")
    result = subprocess.run(cmd, capture_output=True, timeout=180)
    if result.returncode != 0:
        print("[ERROR] Subtitle failed:")
        print(result.stderr.decode()[-500:])
        # Fallback: output tanpa subtitle
        shutil.copy(video_path, out_path)
        print("  [FALLBACK] Output tanpa subtitle")
    else:
        print(f"  [OK] Subtitles burned")

    return out_path


# ── MAIN ─────────────────────────────────────────────────────────────────────
def run(script_path: str = SCRIPT_FILE):
    print("\n" + "="*55)
    print("🎬  EDIT SKILL — FFmpeg Video Assembly")
    print("="*55)

    check_ffmpeg()
    script = load_script(script_path)
    scenes = script.get("scenes", [])

    if not scenes:
        print("[ERROR] Tidak ada scenes.")
        sys.exit(1)

    if not check_assets(scenes):
        print("[ERROR] Assets tidak lengkap. Jalankan visual_skill.py dulu.")
        sys.exit(1)

    Path(TEMP_DIR).mkdir(exist_ok=True)

    # Step 1 — Get audio duration
    audio_dur = get_audio_duration(VOICE_FILE)
    print(f"\n[edit_skill] Audio duration : {audio_dur:.1f}s")
    print(f"[edit_skill] Scenes         : {len(scenes)}")
    print(f"[edit_skill] Per scene      : {audio_dur/len(scenes):.1f}s")
    print(f"[edit_skill] Output         : {OUTPUT_FILE}\n")

    # Step 2 — Make scene clips (Ken Burns)
    print("[1/4] Generating scene clips...")
    clip_paths = []
    for scene in scenes:
        clip = make_scene_clip(scene, audio_dur, len(scenes))
        if clip:
            clip_paths.append(clip)
        else:
            print(f"[WARN] scene_{scene['id']} skip")

    if not clip_paths:
        print("[ERROR] Semua clip gagal.")
        sys.exit(1)

    # Step 3 — Concat
    print("\n[2/4] Concatenating clips...")
    concat = concat_clips(clip_paths)
    if not concat:
        sys.exit(1)

    # Step 4 — Add audio
    print("\n[3/4] Adding voice...")
    with_audio = add_audio(concat, VOICE_FILE)
    if not with_audio:
        sys.exit(1)

    # Step 5 — Burn subtitles
    print("\n[4/4] Adding subtitles...")
    final = add_subtitles(with_audio, scenes, audio_dur)

    # Cleanup temp
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

    # Result
    size_mb = Path(final).stat().st_size / (1024*1024)
    print(f"\n{'='*55}")
    print(f"✅  FINAL VIDEO: {final}")
    print(f"    Size    : {size_mb:.1f} MB")
    print(f"    Duration: {audio_dur:.1f}s")
    print(f"    Format  : {WIDTH}x{HEIGHT} @ {FPS}fps (9:16)")
    print(f"{'='*55}")
    print(f"\nUpload ke:")
    print(f"  TikTok   → caption: {script.get('caption',{}).get('tiktok','')[:50]}...")
    print(f"  IG Reels → same file")
    print(f"  YT Short → same file")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else SCRIPT_FILE
    run(path)

