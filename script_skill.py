"""
script_skill.py
Generates a 15-second cinematic video script for TikTok, IG Reels & YT Shorts.
Uses Groq API (free tier, OpenAI-compatible).

Install: pip install requests
Run    : python script_skill.py
         python script_skill.py "topik custom kamu"
"""

import requests
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MODEL        = "llama-3.3-70b-versatile"
MAX_TOKENS   = 1024
OUTPUT_FILE  = "script_output.json"
API_URL      = "https://api.groq.com/openai/v1/chat/completions"

DEFAULT_TOPIC = "AI agent yang bisa cari uang sendiri"

# ── PROMPT ────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a viral short-form video scriptwriter specializing in crypto, AI, and tech.
Your scripts are cinematic, punchy, and optimized for watch time.

Rules:
- Total duration: EXACTLY 61 seconds
- Hook must land in first 2 seconds (curiosity gap or shock)
- 4 scenes
- Each scene: 12-16 seconds
- Language: match user's input (Indonesian or English)
- Tone: dark, mysterious, data-driven. Not hype. Not corporate.
- Output ONLY valid JSON, no markdown, no explanation

JSON format:
{
  "topic": "...",
  "platform": ["tiktok", "ig_reels", "yt_shorts"],
  "total_duration": 61,
  "hook": "...",
  "scenes": [
    {
      "id": 1,
      "text": "...",
      "visual": "...",
      "duration": 5
    }
  ],
  "cta": "...",
  "caption": {
    "tiktok": "...",
    "ig_reels": "...",
    "yt_shorts": "..."
  },
  "hashtags": ["...", "..."]
}
"""

# ── MAIN ─────────────────────────────────────────────────────────────────────
def generate_script(topic: str = DEFAULT_TOPIC) -> dict:
    if not GROQ_API_KEY:
        print("ERROR: Set GROQ_API_KEY dulu.")
        print("  1. Daftar gratis: https://console.groq.com")
        print("  2. Buat API key di menu 'API Keys'")
        print("  3. export GROQ_API_KEY='gsk_...'")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":  "application/json"
    }

    payload = {
        "model":       MODEL,
        "max_tokens":  MAX_TOKENS,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Generate a 61-second video script about: {topic}"}
        ]
    }

    print(f"\n[script_skill] Topic : '{topic}'")
    print(f"[script_skill] Model : {MODEL}")
    print("[script_skill] Calling Groq API...")

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    except requests.exceptions.ConnectionError:
        print("[ERROR] No internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[ERROR] Request timeout (>30s).")
        sys.exit(1)

    if resp.status_code != 200:
        print(f"[ERROR] API {resp.status_code}: {resp.text[:300]}")
        sys.exit(1)

    raw = resp.json()["choices"][0]["message"]["content"].strip()

    # Strip markdown fences kalau ada
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        script = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse failed: {e}")
        print(f"[RAW]\n{raw}")
        sys.exit(1)

    # Validasi durasi
    total = sum(s.get("duration", 0) for s in script.get("scenes", []))
    script["_meta"] = {
        "generated_at": datetime.utcnow().isoformat(),
        "model":        MODEL,
        "total_sec":    total,
        "duration_ok":  total <= 61
    }

    if total > 61:
        print(f"[WARN] Total {total}s — melebihi 61s target.")
    else:
        print(f"[OK] Duration: {total}s ✓")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    print(f"[script_skill] Saved → {OUTPUT_FILE}")
    return script


def preview(script: dict):
    print("\n" + "="*50)
    print("SCRIPT PREVIEW")
    print("="*50)
    print(f"Topic : {script.get('topic')}")
    print(f"Hook  : {script.get('hook')}")
    print(f"CTA   : {script.get('cta')}")
    print(f"\nScenes ({len(script.get('scenes', []))}):")
    for s in script.get("scenes", []):
        print(f"  [{s['id']}] {s['duration']}s | {s['text']}")
        print(f"       visual: {s['visual']}")
    print(f"\nCaption TikTok : {script.get('caption', {}).get('tiktok', '')[:80]}...")
    print(f"Hashtags       : {' '.join(script.get('hashtags', []))}")
    print("="*50)


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_TOPIC
    result = generate_script(topic)
    preview(result)

