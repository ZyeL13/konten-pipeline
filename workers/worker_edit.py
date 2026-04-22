"""
workers/worker_edit.py — Video assembly.
"""
import logging
import shutil
from pathlib import Path
from agents.edit_agent import get_audio_duration, make_scene_clip, concat_clips, add_audio
log = logging.getLogger("worker.edit")

def run(script_data: dict, run_dir: Path) -> bool:
    scenes_dir = run_dir / "scenes"
    voice = run_dir / "voice.mp3"
    out = run_dir / "final_video.mp4"
    tmp = run_dir / "tmp_edit"
    tmp.mkdir(exist_ok=True)
    scenes = script_data.get("scenes", [])

    missing = [s for s in scenes if not (scenes_dir / f"scene_{s.get('id',0)}.png").exists()]
    if missing or not voice.exists():
        log.error(f"Missing assets: {missing or ['voice.mp3']}"); return False

    dur = get_audio_duration(str(voice))
    log.info(f"Audio: {dur:.1f}s | Scenes: {len(scenes)}")

    words = [len(s.get("text", "").split()) for s in scenes]
    total_w = sum(words) or len(scenes)
    durs = [dur * (w/total_w) for w in words]
    min_d = 2.0  # FIX: dari 12.0 → 2.0
    durs = [max(d, min_d) for d in durs]
    if sum(durs) > dur:
        scale = dur / sum(durs)
        durs = [d*scale for d in durs]

    clips = []
    for i, sc in enumerate(scenes):
        sid = sc.get("id", i+1)
        img = str(scenes_dir / f"scene_{sid}.png")
        cpath = str(tmp / f"clip_{sid}.mp4")
        if make_scene_clip(img, durs[i], cpath):
            clips.append(cpath); log.info(f"  clip_{sid}.mp4 ({durs[i]:.1f}s)")

    if not clips: return False

    list_f = str(tmp / "clips.txt")
    concat = str(tmp / "concat.mp4")
    if not concat_clips(clips, list_f, concat): return False

    with_vid = str(tmp / "with_audio.mp4")
    if not add_audio(concat, str(voice), with_vid): return False

    shutil.move(with_vid, str(out))
    shutil.rmtree(tmp, ignore_errors=True)
    log.info(f"✅ final_video.mp4 ({out.stat().st_size/1024/1024:.1f}MB)")
    return True
