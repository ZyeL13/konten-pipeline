"""
agents/edit_agent.py — Final optimization to prevent "Invalid Argument" on long scripts.
"""

import textwrap
import subprocess
import logging
import os
from pathlib import Path
from core.config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
    SUBTITLE_FONT_SIZE, SUBTITLE_FONT_COLOR, SUBTITLE_BOX_COLOR
)

log = logging.getLogger("agent.edit")
FFMPEG_TIMEOUT = 300

def get_audio_duration(audio_path: str) -> float:
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", audio_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return 60.0

def make_scene_clip(img_path: str, duration: float, out_path: str) -> bool:
    zoom_speed = 0.0005
    total_frames = int(duration * VIDEO_FPS)
    vf = (
        f"scale={VIDEO_WIDTH*2}:{VIDEO_HEIGHT*2},"
        f"zoompan=z='min(zoom+{zoom_speed},1.05)':d={total_frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={VIDEO_FPS},format=yuv420p"
    )
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img_path, "-vf", vf, "-t", str(duration), out_path]
    return subprocess.run(cmd, capture_output=True, timeout=FFMPEG_TIMEOUT).returncode == 0

def add_subtitles(video_path: str, scenes: list, audio_dur: float, out_path: str, scene_durs: list = None) -> bool:
    """
    FIXED: Menggunakan file temporary untuk filter complex guna menghindari error 'Invalid Argument'.
    """
    filter_script_path = Path(video_path).parent / "sub_filter.txt"
    curr = 0.0
    wrapper = textwrap.TextWrapper(width=30)
    
    filters = []
    for i, scene in enumerate(scenes):
        dur = scene_durs[i] if (scene_durs and i < len(scene_durs)) else (audio_dur / len(scenes))
        text = scene.get("text", "").replace("'", "").replace(":", "")
        clean = "\\n".join(wrapper.wrap(text)) # Pakai double backslash untuk ffmpeg
        
        draw = (
            f"drawtext=text='{clean}':fontcolor={SUBTITLE_FONT_COLOR}:"
            f"fontsize={SUBTITLE_FONT_SIZE}:x=(w-text_w)/2:y=(h-text_h)-180:"
            f"box=1:boxcolor={SUBTITLE_BOX_COLOR}@0.6:enable='between(t,{curr},{curr+dur})'"
        )
        filters.append(draw)
        curr += dur

    # Tulis filter ke file agar tidak kena limit command line
    filter_str = ",".join(filters)
    with open(filter_script_path, "w") as f:
        f.write(filter_str)

    # Panggil FFmpeg dengan filter_script
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"filter_script={filter_script_path}",
        "-c:a", "copy",
        out_path
    ]
    
    try:
        log.info(f"Burning subtitles using filter script...")
        res = subprocess.run(cmd, capture_output=True, timeout=FFMPEG_TIMEOUT)
        if filter_script_path.exists(): filter_script_path.unlink()
        return res.returncode == 0
    except Exception as e:
        log.error(f"Subtitle error: {e}")
        return False

def concat_clips(clip_paths: list, list_file: str, out_path: str) -> bool:
    with open(list_file, "w") as f:
        for p in clip_paths: f.write(f"file '{Path(p).absolute()}'\n")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", out_path]
    res = subprocess.run(cmd, capture_output=True, timeout=FFMPEG_TIMEOUT)
    if Path(list_file).exists(): Path(list_file).unlink()
    return res.returncode == 0

def add_audio(video_path: str, audio_path: str, out_path: str) -> bool:
    cmd = ["ffmpeg", "-y", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", out_path]
    return subprocess.run(cmd, capture_output=True, timeout=FFMPEG_TIMEOUT).returncode == 0

def add_character_overlay_blended(video_path: str, character_path: str, out_path: str,
                                   position: str = "bottom-left", scale: int = 500,
                                   feather: int = 0, opacity: float = 1.0) -> bool:
    x_pos, y_pos = ("30", "H-h-30") if position == "bottom-left" else ("W-w-30", "H-h-30")
    filter_complex = (
        f"[1:v]scale={scale}:-1,format=rgba,colorchannelmixer=aa={opacity}[char];"
        f"[0:v][char]overlay={x_pos}:{y_pos}:format=auto"
    )
    cmd = [
        "ffmpeg", "-y", "-i", video_path, "-i", character_path,
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "copy", out_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=FFMPEG_TIMEOUT)
        return result.returncode == 0
    except:
        return False
