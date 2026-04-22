"""
workers/worker_qc.py — QC execution layer.
"""
import json
import logging
import subprocess
import tempfile
import time
from pathlib import Path
import requests
from agents.qc_agent import analyze_frame, synthesize_report
from core.config import GROQ_URL, GROQ_API_KEY, QC_N_FRAMES, QC_FRAME_DELAY, QC_PASS_SCORE, TARGET_DURATION, LLM_TIMEOUT

log = logging.getLogger("worker.qc")

def _get_video_info(video_path: str) -> dict:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if not res.stdout: return {}
    data = json.loads(res.stdout)
    fmt = data.get("format", {})
    vid = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    aud = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), {})
    return {"duration": round(float(fmt.get("duration", 0)), 2), "width": vid.get("width", 0), "height": vid.get("height", 0), "has_audio": bool(aud), "audio_codec": aud.get("codec_name", "none"), "aspect": f"{vid.get('width',0)}x{vid.get('height',0)}"}

def _extract_frames(video_path: str, tmpdir: str, n: int) -> list:
    info = _get_video_info(video_path)
    dur = info.get("duration", 0)
    if dur == 0: return []
    frames = []
    for i in range(n):
        ts = round((dur / (n + 1)) * (i + 1), 2)
        out = f"{tmpdir}/frame_{i+1}.jpg"
        subprocess.run(["ffmpeg", "-y", "-ss", str(ts), "-i", video_path, "-vframes", "1", "-q:v", "2", out], capture_output=True)
        if Path(out).exists():
            frames.append({"path": out, "bytes": Path(out).read_bytes(), "timestamp": ts, "index": i+1})
    return frames

def _transcribe(audio_path: str) -> dict:
    if not Path(audio_path).exists(): return {"text": "", "word_count": 0, "words_per_min": 0, "error": "no_audio"}
    try:
        with open(audio_path, "rb") as f:
            resp = requests.post(f"{GROQ_URL}/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                files={"file": ("audio.wav", f, "audio/wav")},
                data={"model": "whisper-large-v3-turbo", "response_format": "verbose_json", "language": "id"}, timeout=60)
    except Exception as e:
        return {"text": "", "word_count": 0, "words_per_min": 0, "error": str(e)}
    if resp.status_code != 200: return {"text": "", "word_count": 0, "words_per_min": 0, "error": f"Whisper {resp.status_code}"}
    d = resp.json()
    t = d.get("text", "").strip()
    dur = d.get("duration", 0)
    return {"text": t, "duration": round(dur, 2), "word_count": len(t.split()), "words_per_min": round((len(t.split())/dur)*60) if dur>0 else 0}

def run(run_dir: Path) -> bool:
    video = run_dir / "final_video.mp4"
    if not video.exists(): log.error("Video not found"); return False
    log.info(f"QC start — {video}")

    with tempfile.TemporaryDirectory() as tmp:
        info = _get_video_info(str(video))
        audio = f"{tmp}/audio.wav"
        subprocess.run(["ffmpeg", "-y", "-i", str(video), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", audio], capture_output=True)
        transcript = _transcribe(audio)

        frames = _extract_frames(str(video), tmp, QC_N_FRAMES)
        analyses = []
        for f in frames:
            res = analyze_frame(f["bytes"], f["timestamp"], f["index"])
            analyses.append(res)
            if i < len(frames)-1: time.sleep(QC_FRAME_DELAY)

        script_data = None
        if (run_dir / "script_output.json").exists():
            try: script_data = json.loads((run_dir / "script_output.json").read_text())
            except: pass

        report = synthesize_report(info, transcript, analyses, script_data)
        (run_dir / "qc_report.json").write_text(json.dumps(report, indent=2))
        
        overall = report.get("overall_score", 0)
        verdict = report.get("verdict", "unknown")
        log.info(f"QC done — verdict={verdict} score={overall}/10")
        
        # Print simple summary
        print(f"\n📊 QC: {verdict.upper()} | Score: {overall}/10")
        if "top_issues" in report:
            for i in report["top_issues"]: print(f"  • {i}")
        return verdict in ("publish", "fix_minor") and float(overall) >= QC_PASS_SCORE
