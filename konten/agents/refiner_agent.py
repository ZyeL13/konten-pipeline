"""
agents/refiner_agent.py — Script refinement + emotion labeling.
Fixes typos AND assigns emotion per scene for character overlay.
"""

import json
import re
import requests
from core.config import GROQ_URL, GROQ_MODEL

# Emotion → asset filename mapping
EMOTION_ASSETS = {
    "serious"  : "fullbody.png",
    "focused"  : "focused.png",
    "neutral"  : "neutral.png",
    "smirk"    : "smirk.png",
    "talk"     : "talk.png",
    "halfbody" : "halfbody.png",
}
DEFAULT_EMOTION = "neutral"


def _extract_json(raw: str) -> dict:
    raw = re.sub(r'```json|```', '', raw).strip()
    return json.loads(raw)


def _final_polish(text: str) -> str:
    """Fix common word-splitting errors from LLM."""
    fixes = {
        r'\bSola\s+n\s+a\b'       : 'Solana',
        r'\bsig\s+n\s+al\b'       : 'signal',
        r'\bbi\s+n\s+ance\b'       : 'Binance',
        r'\bana\s+l\s+ysis\b'      : 'analysis',
        r'\ban\s+other\b'          : 'another',
        r'\btech\s+n\s+ology\b'    : 'technology',
        r'\bdigit\s+a\s+l\b'       : 'digital',
        r'\bBit\s+coin\b'          : 'Bitcoin',
        r'\bEther\s+eum\b'         : 'Ethereum',
        r'\bblock\s+chain\b'       : 'blockchain',
    }
    for pattern, repl in fixes.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    text = re.sub(r'\s+n\'t\b', "n't", text)
    return text


def refine_script(script_data: dict) -> dict:
    """
    Fix typos AND assign emotion label per scene.
    Returns same structure with cleaned text + emotion fields.
    Falls back to original if API fails.
    """
    scenes = script_data.get("scenes", [])
    if not scenes:
        return script_data

    texts    = [s.get("text", "") for s in scenes]
    combined = "\n".join([f"[SCENE {i+1}]: {t}" for i, t in enumerate(texts)])

    # Emotion guide — map "the auditor" tone patterns to expressions
    emotion_guide = """
EMOTION ASSIGNMENT GUIDE for "the auditor" character:
- serious  : factual statements, data delivery, market analysis
- focused  : cause-effect analysis, connecting dots, pattern recognition
- neutral  : scene transitions, establishing context, background info
- smirk    : dark humor, ironic observations, gap between expectation and reality
- talk     : direct address, CTA, closing statement
- halfbody : dramatic pause, single short impactful sentence

Pick the BEST emotion for each scene based on content and tone.
"""

    prompt = f"""You are a professional script editor for AI and crypto news videos.
{emotion_guide}

INPUT SCENES:
{combined}

TASKS:
1. Fix ALL typos, merged words, spacing errors, punctuation issues
2. Keep technical terms capitalized: GPT, LLM, ETH, BTC, Bitcoin, Ethereum, etc.
3. Do NOT change meaning or "the auditor" cold/dry tone
4. Assign one emotion label per scene from: serious, focused, neutral, smirk, talk, halfbody
5. Remove "[SCENE X]:" labels from output

OUTPUT ONLY VALID JSON:
{{"scenes": [
  {{"text": "fixed text for scene 1", "emotion": "serious"}},
  {{"text": "fixed text for scene 2", "emotion": "smirk"}},
  {{"text": "fixed text for scene 3", "emotion": "focused"}},
  {{"text": "fixed text for scene 4", "emotion": "talk"}}
]}}"""

    try:
        resp = requests.post(
            f"{GROQ_URL}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model"      : GROQ_MODEL,
                "messages"   : [{"role": "user", "content": prompt}],
                "max_tokens" : 1000,
                "temperature": 0.2,
            },
            timeout=30
        )

        if resp.status_code != 200:
            return _apply_default_emotions(script_data)

        raw    = resp.json()["choices"][0]["message"]["content"]
        fixed  = _extract_json(raw)
        result = fixed.get("scenes", [])

        for i, scene in enumerate(scenes):
            if i < len(result) and result[i]:
                clean_text = re.sub(r'^\[SCENE \d+\]:\s*', '', result[i].get("text", ""))
                scene["text"]    = _final_polish(clean_text)
                scene["emotion"] = result[i].get("emotion", DEFAULT_EMOTION)

        # Clean hook too
        hook = script_data.get("hook", "")
        if hook:
            script_data["hook"] = _final_polish(hook)

        return script_data

    except Exception as e:
        return _apply_default_emotions(script_data)


def _apply_default_emotions(script_data: dict) -> dict:
    """
    Fallback: assign default emotions without LLM.
    Pattern: serious → smirk → focused → talk
    """
    defaults = ["serious", "smirk", "focused", "talk"]
    for i, scene in enumerate(script_data.get("scenes", [])):
        if "emotion" not in scene:
            scene["emotion"] = defaults[i % len(defaults)]
    return script_data


def get_asset_for_emotion(emotion: str, assets_dir: str) -> str:
    """
    Return full path to character asset for given emotion.
    Falls back to neutral if file not found.
    """
    from pathlib import Path
    base    = Path(assets_dir)
    filename = EMOTION_ASSETS.get(emotion, EMOTION_ASSETS[DEFAULT_EMOTION])
    path    = base / filename

    if path.exists():
        return str(path)

    # Fallback chain
    for fallback in ["neutral.png", "fullbody.png"]:
        fb = base / fallback
        if fb.exists():
            return str(fb)

    return ""

