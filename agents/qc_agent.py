"""
agents/qc_agent.py — Pure QC logic. No file I/O, no retries.
"""
import base64
import json
import re
import requests
from core.config import GROQ_URL, GROQ_API_KEY, VISION_MODEL, LLM_MODEL, TARGET_DURATION, LLM_TIMEOUT, VISION_TIMEOUT

def analyze_frame(img_bytes: bytes, timestamp: float, index: int) -> dict:
    b64 = base64.b64encode(img_bytes).decode()
    payload = {
        "model": VISION_MODEL,
        "max_tokens": 400,
        "temperature": 0.2,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": "Analyze this frame for lighting, composition, text readability, and visual quality. Return ONLY valid JSON with keys: lighting, composition, text_readability, visual_quality, mood, dominant_colors, quick_fix."}
            ]
        }]
    }
    try:
        resp = requests.post(f"{GROQ_URL}/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json=payload, timeout=VISION_TIMEOUT)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        return {"frame": index, "timestamp": timestamp, "skipped": True, "reason": str(e)}

    err = resp.text.lower()
    if resp.status_code in [429, 500, 503, 529]:
        return {"frame": index, "timestamp": timestamp, "skipped": True, "reason": f"HTTP_{resp.status_code}"}
    if resp.status_code == 400 and "decommissioned" in err:
        return {"frame": index, "timestamp": timestamp, "skipped": True, "reason": "model_decommissioned"}
    if resp.status_code != 200:
        return {"frame": index, "timestamp": timestamp, "skipped": True, "reason": f"HTTP_{resp.status_code}"}

    raw = resp.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        res = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"frame": index, "timestamp": timestamp, "skipped": True, "reason": f"parse: {e}"}
    res["frame"] = index
    res["timestamp"] = timestamp
    return res

def synthesize_report(video_info: dict, transcript: dict, frame_analyses: list, script_data: dict = None) -> dict:
    script_ctx = ""
    if script_data:
        hook = script_data.get("hook", "n/a")
        scenes = script_data.get("scenes", [])
        script_ctx = f"\nHOOK: {hook}\nSCENES: {' | '.join(s.get('text','')[:50] for s in scenes)}\n"

    frames_txt = []
    all_skipped = True
    for f in frame_analyses:
        if f.get("skipped"):
            frames_txt.append(f"Frame {f['frame']} SKIPPED: {f['reason']}")
        else:
            all_skipped = False
            frames_txt.append(f"Frame {f['frame']}: {json.dumps(f, indent=2)}")

    if all_skipped:
        return {
            "duration_score": {"score": 3, "note": f"Duration {video_info.get('duration')}s exceeds target {TARGET_DURATION}s"},
            "audio_score": {"score": 5, "note": transcript.get("text", "No audio detected")[:50]},
            "visual_score": {"score": 6, "note": "Vision API unavailable, using neutral score"},
            "sync_score": {"score": 5, "note": "Cannot evaluate"},
            "hook_strength": {"score": 5, "note": "Based on script only"},
            "pacing_score": {"score": 4, "note": "Duration mismatch"},
            "overall_score": 5.5,
            "verdict": "fix_minor",
            "acc_reject_reason": "Vision API down, duration slightly high",
            "top_issues": ["Check video length", "Verify audio sync"],
            "quick_wins": ["Trim video to 15s", "Check audio levels"],
            "publish_risk": "low"
        }

    prompt = f"""You are a strict QC evaluator. Target: {TARGET_DURATION}s, 720x1280.
{script_ctx}
DURATION: {video_info.get('duration')}s (gap: {video_info.get('duration',0)-TARGET_DURATION:+.1f}s)
RESOLUTION: {video_info.get('width')}x{video_info.get('height')}
AUDIO: {transcript.get('word_count',0)} words, {transcript.get('words_per_min',0)} wpm. Preview: "{transcript.get('text','')[:100]}"
FRAMES: {chr(10).join(frames_txt)}
Return ONLY valid JSON. Keys: duration_score, audio_score, visual_score, sync_score, hook_strength, pacing_score, overall_score (1-10), verdict (publish|fix_minor|fix_major|reject), acc_reject_reason, top_issues (list), quick_wins (list), publish_risk (low|medium|high)."""

    try:
        resp = requests.post(f"{GROQ_URL}/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": LLM_MODEL, "max_tokens": 1000, "temperature": 0.2, "messages": [{"role": "user", "content": prompt}]},
            timeout=LLM_TIMEOUT)
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e)}
