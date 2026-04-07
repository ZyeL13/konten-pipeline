"""
agents/edit_agent.py — Pure FFmpeg video assembly logic.
FIXED: Match function names for worker_edit.py and removed ghost blur.
"""

import re
import textwrap
import subprocess
from pathlib import Path
from core.config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
    SUBTITLE_FONT_SIZE, SUBTITLE_FONT_COLOR, SUBTITLE_BOX_COLOR
)


def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except Exception:
        return 61.0


def make_scene_clip(img_path: str, duration: float, out_path: str) -> bool:
    zoom_speed   = 0.0005
    total_frames = int(duration * VIDEO_FPS)

    vf = (
        f"scale={VIDEO_WIDTH*2}:{VIDEO_HEIGHT*2},"
        f"zoompan=z='min(zoom+{zoom_speed},1.05)':"
        f"d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={VIDEO_FPS},"
        f"format=yuv420p"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img_path,
        "-vf", vf,
        "-t", str(duration),
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def add_subtitles(video_path: str, text: str, out_path: str) -> bool:
    wrapper = textwrap.TextWrapper(width=32)
    lines   = wrapper.wrap(text)
    clean   = "\n".join(lines).replace("'", "'\\''").replace(":", "\\:")

    # H-h-180 supaya teks tidak tertutup kaki Auditor
    vf = (
        f"drawtext=text='{clean}':fontcolor={SUBTITLE_FONT_COLOR}:"
        f"fontsize={SUBTITLE_FONT_SIZE}:x=(w-text_w)/2:y=(h-text_h)-180:"
        f"box=1:boxcolor={SUBTITLE_BOX_COLOR}@0.6:boxborderw=15"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", vf,
        "-c:a", "copy",
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def concat_clips(clip_paths: list, list_file: str, out_path: str) -> bool:
    """
    Menggabungkan klip video.
    Menerima 3 argumen sesuai kebutuhan worker_edit.py
    """
    if not clip_paths:
        return False
    
    txt_path = Path(list_file)
    with txt_path.open("w") as f:
        for p in clip_paths:
            # Pastikan path absolut biar FFmpeg gak bingung di Termux
            f.write(f"file '{Path(p).absolute()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(txt_path),
        "-c", "copy",
        out_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    # Hapus file list sementara setelah dipake
    if txt_path.exists():
        txt_path.unlink()
        
    return result.returncode == 0



def add_audio(video_path: str, audio_path: str, out_path: str) -> bool:
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def add_character_overlay_blended(video_path: str, character_path: str, out_path: str,
                                   position: str = "bottom-left", scale: int = 500,
                                   feather: int = 0, opacity: float = 1.0) -> bool:
    """
    FIXED: Nama fungsi disamakan dengan worker_edit.py.
    Removed gblur to ensure sharp visuals.
    """
    if position == "bottom-left":
        x_pos, y_pos = "30", "H-h-30"
    elif position == "bottom-right":
        x_pos, y_pos = "W-w-30", "H-h-30"
    else:
        x_pos, y_pos = "30", "30"
    
    # Filter tanpa gblur
    filter_complex = (
        f"[1:v]scale={scale}:-1,format=rgba,"
        f"colorchannelmixer=aa={opacity}[char];"
        f"[0:v][char]overlay={x_pos}:{y_pos}:format=auto"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", character_path,
        "-filter_complex", filter_complex,
        "-c:a", "copy",
        out_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    return result.returncode == 0
