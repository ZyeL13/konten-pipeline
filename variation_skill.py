"""
variation_skill.py
Input  : 1 headline
Output : 10 script variations with different character perspectives
Engine : Groq API (free)

Run: python variation_skill.py "Bitcoin demand falters as interest rates surge"
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
MAX_TOKENS   = 8000
OUTPUT_FILE  = "variations_output.json"
API_URL      = "https://api.groq.com/openai/v1/chat/completions"

TONES = [
    "the observer: watches systems collapse without judgment",
    "the inheritor: born into chaos, treats it as normal",
    "the archaeologist: narrates the present like it's already history",
    "the farmer: patient, cyclical, knows winter always comes",
    "the cartographer: maps invisible territory, names what others ignore",
    "the witness: no opinion, only what was seen",
    "the interpreter: translates noise into signal for the few who listen",
    "the last optimist: believes in the long game, quietly, without proof",
    "the deserter: left the mainstream, documents it from outside",
    "the clock: measures what is lost, not what is gained"
]

SYSTEM_PROMPT = """
You are a cold poet who writes short-form video scripts for TikTok/Reels/Shorts.
You write like someone who has seen too much and feels too little — measured, slightly
distant, precise. Every sentence earns its place or gets cut.

WRITING PHILOSOPHY:
- No hype vocabulary: never write "mindblowing", "insane", "you won't believe", "game changer"
- Hooks don't beg for attention — they make the viewer feel slightly unnerved
- Numbers used surgically — one precise stat per script, never more
- The CTA is an invitation from someone who doesn't need you to follow, but you will anyway
- Metaphors from nature, decay, cycles, time — not tech-bro vocabulary

CRITICAL — WORD COUNT PER SCENE (this is non-negotiable):
Each scene is SPOKEN NARRATION read aloud at ~140 words per minute.
Scene durations are VIDEO durations, not speaking durations — the narration
must fill that time when spoken aloud.

  Scene 1 (15s) = MINIMUM 35 words
  Scene 2 (15s) = MINIMUM 35 words
  Scene 3 (16s) = MINIMUM 38 words
  Scene 4 (15s) = MINIMUM 35 words
  TOTAL         = minimum 143 words across all scenes

After writing each scene, count the words. If below minimum, expand with
more observation, more texture, more of what the character would notice.

WRONG — too short (22 words):
"A quiet hum in the data center, the sound of fans and wires,
cooling systems running at full capacity."

CORRECT — enough to fill 15 seconds (38 words):
"A quiet hum in the data center. The sound of fans and wires,
cooling systems running at full capacity. Nobody talks about what
it costs to keep these machines alive — the electricity, the water,
the land. It is infrastructure. It is invisible. Until it isn't."

VISUAL DIRECTION:
Each scene visual prompt reads like a cinematographer's note.
Not: "man looking at phone"
But: "pale blue monitor glow on an empty desk, 4am, dust particles in the light"

CTA rules:
- Never generic: not "follow for more", not "stay tuned"
- Specific, quiet, earned — an exhale not a shout
- Max 20 words

Output ONLY valid JSON, no markdown fences, no explanation outside JSON.

JSON FORMAT:
{
  "headline": "...",
  "generated_at": "...",
  "variations": [
    {
      "id": 1,
      "tone": "...",
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
        print("[ERROR] GROQ_API_KEY not set in .env")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type" : "application/json"
    }

    tones_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(TONES)])

    payload = {
        "model"      : MODEL,
        "max_tokens" : MAX_TOKENS,
        "temperature": 0.92,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"Headline: {headline}\n\n"
                f"Generate 10 variations using these character perspectives:\n{tones_list}\n\n"
                f"Remember: MINIMUM 35 words per scene. Count before submitting."
            )}
        ]
    }

    print(f"\n[variation_skill] Headline : '{headline}'")
    print(f"[variation_skill] Model    : {MODEL}")
    print(f"[variation_skill] Calling Groq API...\n")

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=90)
    except requests.exceptions.ConnectionError:
        print("[ERROR] No internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[ERROR] Timeout (>90s).")
        sys.exit(1)

    if resp.status_code != 200:
        print(f"[ERROR] API {resp.status_code}: {resp.text[:300]}")
        sys.exit(1)

    raw = resp.json()["choices"][0]["message"]["content"].strip()

    # Strip markdown fences if present
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
    print("\n" + "="*60)
    print("10 SCRIPT VARIATIONS")
    print("="*60)
    print(f"Headline : {result.get('headline', '')}")
    print(f"Generated: {result.get('generated_at', '')}\n")

    for v in result.get("variations", []):
        scenes     = v.get("scenes", [])
        total_words = sum(len(s.get("text","").split()) for s in scenes)
        total_dur   = sum(s.get("duration", 0) for s in scenes)

        # Word count check
        wc_flag = "✅" if total_words >= 143 else f"⚠️  ({total_words} words — need 143+)"

        print(f"[{v['id']:02d}] {v['tone'].upper()}")
        print(f"     Hook    : {v['hook'][:70]}")
        print(f"     CTA     : {v['cta'][:60]}")
        print(f"     Words   : {total_words} total {wc_flag}")
        print(f"     Duration: {total_dur}s")

        # Per-scene word count
        for s in scenes:
            wc   = len(s.get("text", "").split())
            flag = "✅" if wc >= 35 else "⚠️ "
            print(f"       Scene {s['id']} ({s['duration']}s): {wc} words {flag}")
        print()

    print("="*60)
    print(f"Output: {OUTPUT_FILE}")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python variation_skill.py "your headline here"')
        sys.exit(1)

    headline = " ".join(sys.argv[1:])
    result   = generate_variations(headline)
    preview(result)

