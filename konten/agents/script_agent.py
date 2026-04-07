"""
agents/script_agent.py — Pure script generation logic.
SYNCED WITH LOCAL CLAWROUTER & FIXED FOR WORKER_EDIT
"""

import json
import logging
import random
import requests
from core.config import (
    GROQ_API_KEY,
    GROQ_URL_PRIMARY, GROQ_URL_FALLBACK,
    GROQ_MODEL_PRIMARY, GROQ_MODEL_FALLBACKS,
    SCRIPT_TEMPERATURE,
    SCRIPT_MIN_WORDS_TOTAL, SCRIPT_MIN_WORDS_SCENE
)

log = logging.getLogger("agent.script")

SYSTEM_PROMPT = """You are 'The Auditor'. A cold, technical, and sarcastic AI character.
Format: Return ONLY valid JSON with 'scenes' array containing 4 objects: {'scene': 1..4, 'text': '...'}.
Target total: 125-145 words."""

def _validate_word_count(result: dict) -> tuple[bool, int, list]:
    scenes = result.get("scenes", [])
    counts = [len(s.get("text", "").split()) for s in scenes]
    total = sum(counts)
    is_valid = (total >= SCRIPT_MIN_WORDS_TOTAL) and all(c >= SCRIPT_MIN_WORDS_SCENE for c in counts)
    return is_valid, total, counts

def _call_api(url: str, model_name: str, auth_key: str) -> dict | None:
    headers = {
        "Authorization": f"Bearer {auth_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "temperature": SCRIPT_TEMPERATURE,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Write a detailed 60-second technical script about the headline."}
        ]
    }

    try:
        resp = requests.post(f"{url}/chat/completions", headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            log.warning(f"  [{model_name}] HTTP {resp.status_code}")
            return None
        
        raw_content = resp.json()["choices"][0]["message"]["content"].strip()
        if "```" in raw_content:
            raw_content = raw_content.split("```")[1].replace("json", "").strip()
            
        result = json.loads(raw_content)
        is_valid, total_wc, scene_counts = _validate_word_count(result)
        
        log.info(f"  [{model_name}] {'✅' if is_valid else '⚠️'} {total_wc} words")
        return result if is_valid else None
        
    except Exception as e:
        log.warning(f"  [{model_name}] Error: {str(e)}")
        return None

def generate_script(headline: str) -> dict | None:
    log.info(f"Generating for: {headline[:60]}...")
    
    # 1. PRIMARY: ClawRouter Local
    res = _call_api(GROQ_URL_PRIMARY, GROQ_MODEL_PRIMARY, GROQ_API_KEY or "no-key")
    if res: return res
    
    # 2. FALLBACK: Groq Native
    if GROQ_API_KEY:
        res = _call_api(GROQ_URL_FALLBACK, GROQ_MODEL_FALLBACKS[0], GROQ_API_KEY)
        if res: return res

    return None

def to_script_output(raw_data: dict) -> dict:
    """
    FIX: Memastikan setiap scene punya 'id' (0-indexed) 
    untuk menghindari KeyError di worker_edit.
    """
    scenes = raw_data.get("scenes", [])
    formatted_scenes = []
    
    for i, s in enumerate(scenes):
        formatted_scenes.append({
            "id": i,              # Dibutuhkan oleh worker_edit
            "scene": i + 1,       # Untuk referensi manusia
            "text": s.get("text", ""),
            "emotion": s.get("emotion", "neutral") # Default jika refiner belum jalan
        })
    
    return {"scenes": formatted_scenes}
