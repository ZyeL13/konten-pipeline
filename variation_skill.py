"""
variation_skill.py
Input  : 1 headline berita
Output : 10 variasi script hook + caption dengan tone berbeda
Engine : Groq API (free)

Install: pip install requests
Run    : python variation_skill.py "Bitcoin naik 20% dalam 24 jam"
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
MAX_TOKENS   = 2048
OUTPUT_FILE  = "variations_output.json"
API_URL      = "https://api.groq.com/openai/v1/chat/completions"

# 10 tone yang berbeda
TONES = [
    "dark & mysterious",
    "urgent breaking news",
    "sarcastic & cynical",
    "storytelling narrative",
    "data-driven analyst",
    "conspiracy theory",
    "motivational hustle",
    "fear & warning",
    "poetic & philosophical",
    "casual Gen-Z slang"
]

SYSTEM_PROMPT = """
You are a viral short-form video scriptwriter for TikTok, Instagram Reels, and YouTube Shorts.
Given ONE news headline, generate 10 unique script variations — one per tone.

Rules:
- Each variation targets 61 seconds total video duration
- Hook: first 3 seconds, must create curiosity gap or emotional trigger
- 3-4 scenes per variation, each 10-15 seconds
- Language: match the input language (Indonesian or English)
- Scene ke-4 (CTA) HARUS spesifik, max 8 detik, bukan generic "Simak selengkapnya"
- CTA harus berupa aksi konkret: follow, komen pertanyaan, atau klaim sesuatu
- Hook harus memancing emosi spesifik: takut, penasaran, atau FOMO
- Output ONLY valid JSON, no markdown, no explanation

JSON format:
{
  "headline": "...",
  "generated_at": "...",
  "variations": [
    {
      "id": 1,
      "tone": "dark & mysterious",
      "hook": "...",
      "scenes": [
        {"id": 1, "text": "...", "visual": "...", "duration": 15},
        {"id": 2, "text": "...", "visual": "...", "duration": 15},
        {"id": 3, "text": "...", "visual": "...", "duration": 16},
        {"id": 4, "text": "...", "visual": "...", "duration": 15}
      ],
      "cta": "...",
      "caption": "...",
      "hashtags": ["...", "..."],
      "total_duration": 61
    }
  ]
}
"""

# ── MAIN ─────────────────────────────────────────────────────────────────────
def generate_variations(headline: str) -> dict:
    if not GROQ_API_KEY:
        print("ERROR: Set GROQ_API_KEY dulu.")
        print("  export GROQ_API_KEY='gsk_...'")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":  "application/json"
    }

    tones_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(TONES)])

    payload = {
        "model":       MODEL,
        "max_tokens":  MAX_TOKENS,
        "temperature": 0.85,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"Headline: {headline}\n\n"
                f"Generate 10 variations using these tones:\n{tones_list}"
            )}
        ]
    }

    print(f"\n[variation_skill] Headline : '{headline}'")
    print(f"[variation_skill] Tones    : {len(TONES)} variations")
    print(f"[variation_skill] Model    : {MODEL}")
    print("[variation_skill] Calling Groq API...\n")

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    except requests.exceptions.ConnectionError:
        print("[ERROR] No internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[ERROR] Timeout (>60s).")
        sys.exit(1)

    if resp.status_code != 200:
        print(f"[ERROR] API {resp.status_code}: {resp.text[:300]}")
        sys.exit(1)

    raw = resp.json()["choices"][0]["message"]["content"].strip()

    # Strip markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse failed: {e}")
        print(f"[RAW]\n{raw[:500]}")
        sys.exit(1)

    result["generated_at"] = datetime.utcnow().isoformat()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved → {OUTPUT_FILE}")
    return result


def preview(result: dict):
    print("\n" + "="*55)
    print("10 VARIASI SCRIPT")
    print("="*55)
    print(f"Headline : {result.get('headline', '')}")
    print(f"Generated: {result.get('generated_at', '')}\n")

    for v in result.get("variations", []):
        print(f"[{v['id']:02d}] TONE: {v['tone'].upper()}")
        print(f"     Hook    : {v['hook']}")
        print(f"     CTA     : {v['cta']}")
        print(f"     Caption : {v.get('caption', '')[:70]}...")
        print(f"     Hashtags: {' '.join(v.get('hashtags', [])[:5])}")
        total = sum(s.get('duration', 0) for s in v.get('scenes', []))
        print(f"     Duration: {total}s")
        print()

    print("="*55)
    print(f"Output file: {OUTPUT_FILE}")
    print("="*55)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python variation_skill.py \"headline berita kamu\"")
        print("Contoh:")
        print("  python variation_skill.py \"Bitcoin naik 20% dalam 24 jam\"")
        print("  python variation_skill.py \"AI agent bisa hasilkan $1000 per hari\"")
        sys.exit(1)

    headline = " ".join(sys.argv[1:])
    result   = generate_variations(headline)
    preview(result)

