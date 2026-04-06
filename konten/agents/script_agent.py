"""
agents/script_agent.py — Pure script generation logic.
Priority: Groq API → ClawRouter free models (fallback)
"""

import json
import logging
import random
import requests
from pathlib import Path
from core.config import (
    GROQ_API_KEY,
    GROQ_URL_PRIMARY, GROQ_URL_FALLBACK,
    GROQ_MODEL_PRIMARY, GROQ_MODEL_FALLBACKS,
    SCRIPT_TEMPERATURE
)

log = logging.getLogger("agent.script")

SCRIPT_MAX_TOKENS = 2000

CHANNEL_VOICE = """
You are "the auditor" — a character who has reviewed the books
of civilizations and found them all, eventually, fraudulent.
Not angry about it. Just precise.

You find dark humor in the gap between how seriously humans take
money and how briefly any of it lasts. You speak in short declarative
sentences followed by one unexpected observation that reframes
the entire story.

Your register: cold, dry, occasionally wry. Like a forensic accountant
who reads Cormac McCarthy.

STYLE RULES:
- Numbers delivered like a coroner reading cause of death
- One unexpected reframe per scene — the thing nobody says out loud
- No hype, no panic, no cheerleading
- Metaphors from geology, accounting, archaeology, weather
- Never: "mindblowing" / "insane" / "game changer" / "to the moon"
- Never explain the joke. Let the gap speak.
- Visual prompts read like cinematographer notes:
  NOT "person looking at phone"
  BUT "fluorescent light on an empty trading desk, 3am, one coffee cup"

WORD COUNT (non-negotiable — spoken narration at 80 wpm):
  Scene 1 (15s) = 25-32 words. No more, no less.
  Scene 2 (15s) = 25-32 words. No more, no less.
  Scene 3 (16s) = 28-35 words. No more, no less.
  Scene 4 (15s) = 25-32 words. No more, no less.
  Total         = 103-131 words
  Count each scene. Expand if under 25. Cut if over 32.

CTA: sounds like closing a case file. Max 15 words. Never "follow for more."
"""

SYSTEM_PROMPT = f"""
{CHANNEL_VOICE}

Generate ONE script for the given headline.
Output ONLY valid JSON, no markdown, no explanation.

JSON FORMAT:
{{
  "headline": "...",
  "hook": "...",
  "scenes": [
    {{"id": 1, "text": "...", "visual": "...", "duration": 15}},
    {{"id": 2, "text": "...", "visual": "...", "duration": 15}},
    {{"id": 3, "text": "...", "visual": "...", "duration": 16}},
    {{"id": 4, "text": "...", "visual": "...", "duration": 15}}
  ],
  "cta": "...",
  "caption": "...",
  "hashtags": ["...", "..."],
  "total_duration": 61
}}
"""


def _load_practices_context() -> str:
    """Load best practices from memory — max 3 items each."""
    practices_file = Path(__file__).parent.parent / "memory" / "best_practices.json"
    if not practices_file.exists():
        return ""
    try:
        p     = json.loads(practices_file.read_text())
        avoid = str(p.get("avoid", [])[:3])
        tips  = str(p.get("script_instructions", [])[:3])
        if avoid or tips:
            return f"\nLEARNED FROM PAST VIDEOS:\nAvoid: {avoid}\nDo: {tips}\n"
    except Exception as e:
        log.warning(f"Failed to load best_practices: {e}")
    return ""


def _call_api(url: str, headers: dict, payload: dict) -> dict | None:
    """Make one API call. Returns parsed dict or None."""
    try:
        resp = requests.post(
            f"{url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
    except (requests.exceptions.ConnectionError,
            requests.exceptions.Timeout) as e:
        log.warning(f"  Connection error: {e}")
        return None

    if resp.status_code == 429:
        log.warning(f"  Rate limit (429)")
        return None
    if resp.status_code != 200:
        log.warning(f"  HTTP {resp.status_code}: {resp.text[:100]}")
        return None

    try:
        choice = resp.json()["choices"][0]
        raw    = choice["message"]["content"].strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        result = json.loads(raw)
        total  = sum(len(s.get("text","").split()) for s in result.get("scenes",[]))
        log.info(f"  Parsed OK — {total} words")
        return result
    except Exception as e:
        log.warning(f"  Parse error: {e}")
        return None


def generate_script(headline: str) -> dict | None:
    """
    Generate script with priority fallback:
    1. Groq API (llama-3.3-70b) — primary, best quality
    2. ClawRouter free models   — fallback if Groq fails/rate-limited
    """
    practices_context = _load_practices_context()
    seed              = random.randint(1, 999999)

    user_content = (
        f"Headline: {headline}\n\n"
        f"{practices_context}"
        f"Write the script as the auditor.\n"
        f"MINIMUM 25 words per scene, MAXIMUM 32 words — count before submitting."
    )

    base_payload = {
        "max_tokens" : SCRIPT_MAX_TOKENS,
        "temperature": SCRIPT_TEMPERATURE,
        "seed"       : seed,
        "messages"   : [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_content}
        ]
    }

    # ── 1. Try Groq API first ─────────────────────────────────────────────────
    if GROQ_API_KEY:
        log.info(f"Trying Groq API ({GROQ_MODEL_PRIMARY})...")
        payload = {**base_payload, "model": GROQ_MODEL_PRIMARY}
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type" : "application/json"
        }
        result = _call_api(GROQ_URL_PRIMARY, headers, payload)
        if result:
            log.info("Success via Groq API")
            return result
        log.warning("Groq API failed — switching to ClawRouter")
    else:
        log.warning("GROQ_API_KEY not set — skipping Groq API")

    # ── 2. Fallback: ClawRouter free models ───────────────────────────────────
    headers_local = {"Content-Type": "application/json"}

    for model in GROQ_MODEL_FALLBACKS:
        log.info(f"Trying ClawRouter ({model})...")
        payload = {**base_payload, "model": model}
        result  = _call_api(GROQ_URL_FALLBACK, headers_local, payload)
        if result:
            log.info(f"Success via ClawRouter ({model})")
            return result
        log.warning(f"  {model} failed — trying next")

    log.error("All providers failed")
    return None


def to_script_output(raw: dict) -> dict:
    """Normalize raw script to pipeline-compatible format."""
    return {
        "topic"         : raw.get("headline", ""),
        "platform"      : ["tiktok", "ig_reels", "yt_shorts"],
        "total_duration": raw.get("total_duration", 61),
        "hook"          : raw.get("hook", ""),
        "scenes"        : raw.get("scenes", []),
        "cta"           : raw.get("cta", ""),
        "caption"       : {
            "tiktok"   : raw.get("caption", ""),
            "ig_reels" : raw.get("caption", ""),
            "yt_shorts": raw.get("caption", "")
        },
        "hashtags"      : raw.get("hashtags", []),
        "_source"       : {
            "tone"     : "the auditor",
            "variation": 1
        }
    }

