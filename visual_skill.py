"""
visual_skill.py — Pollinations.ai Edition
Generate 1 image per scene dari script_output.json.
Engine: Pollinations.ai — GRATIS, NO API KEY, NO SIGNUP.

Install: pip install requests
Run    : python visual_skill.py
"""

import requests
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────────────────────
SCRIPT_FILE  = "script_output.json"
OUTPUT_DIR   = "scenes"
LOG_FILE     = "visual_log.json"

# Image spec — 9:16 vertical
IMAGE_WIDTH  = 720
IMAGE_HEIGHT = 1280
MODEL        = "flux"   # flux | turbo | flux-realism

# Style prefix
STYLE_PREFIX = (
    "cinematic dark aesthetic, moody lighting, high contrast, "
    "digital art, 4k quality, no text, no watermark, "
)

TONE_STYLE = {
    "dark & mysterious"      : "dark shadows, mysterious fog, ominous atmosphere, ",
    "urgent breaking news"   : "dramatic lighting, high tension, bold colors, ",
    "conspiracy theory"      : "red string board, surveillance, dark basement, ",
    "fear & warning"         : "horror cinematic, red warning lights, dystopian, ",
    "motivational hustle"    : "golden hour, success aesthetic, bright ambitious, ",
    "poetic & philosophical" : "ethereal dreamy, soft bokeh, contemplative, ",
    "casual Gen-Z slang"     : "vibrant neon, street aesthetic, modern trendy, ",
    "data-driven analyst"    : "clean minimal, charts, blue corporate tech, ",
    "sarcastic & cynical"    : "satirical illustration, dark humor, editorial, ",
    "storytelling narrative" : "cinematic storyboard, warm tones, narrative scene, ",
}

# ── HELPERS ───────────────────────────────────────────────────────────────────
def load_script(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] {path} tidak ada.")
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def build_prompt(visual_desc: str, tone: str = "") -> str:
    tone_style = TONE_STYLE.get(tone, "")
    return f"{STYLE_PREFIX}{tone_style}{visual_desc}"

def generate_image(prompt: str, scene_id: int) -> str | None:
    """
    Pollinations image API:
    GET https://image.pollinations.ai/prompt/{encoded_prompt}?width=W&height=H&model=flux&nologo=true
    Returns image bytes directly.
    """
    encoded = urllib.parse.quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}"
        f"&model={MODEL}&nologo=true&seed={scene_id * 42}"
    )

    print(f"  [scene_{scene_id}] Generating...")
    print(f"  Prompt: {prompt[:80]}...")

    try:
        resp = requests.get(url, timeout=90)
    except requests.exceptions.Timeout:
        print(f"  [ERROR] Timeout scene_{scene_id}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"  [ERROR] No internet scene_{scene_id}")
        return None

    if resp.status_code != 200:
        print(f"  [ERROR] HTTP {resp.status_code}")
        return None

    # Check kalau response bukan image
    content_type = resp.headers.get("content-type", "")
    if "image" not in content_type:
        print(f"  [ERROR] Response bukan image: {content_type}")
        return None

    filepath = os.path.join(OUTPUT_DIR, f"scene_{scene_id}.png")
    with open(filepath, "wb") as f:
        f.write(resp.content)

    size_kb = len(resp.content) / 1024
    print(f"  [OK] scene_{scene_id}.png ({size_kb:.0f} KB)")
    return filepath


# ── MAIN ─────────────────────────────────────────────────────────────────────
def run(script_path: str = SCRIPT_FILE):
    print("\n" + "="*55)
    print("🎨  VISUAL SKILL — Pollinations.ai (Free, No Key)")
    print("="*55)

    script = load_script(script_path)
    scenes = script.get("scenes", [])
    tone   = script.get("_source", {}).get("tone", "")

    if not scenes:
        print("[ERROR] Tidak ada scenes.")
        sys.exit(1)

    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    print(f"[visual_skill] Scenes  : {len(scenes)}")
    print(f"[visual_skill] Tone    : {tone or 'default'}")
    print(f"[visual_skill] Size    : {IMAGE_WIDTH}x{IMAGE_HEIGHT} (9:16)")
    print(f"[visual_skill] Model   : {MODEL}\n")

    log     = []
    success = 0

    for scene in scenes:
        sid    = scene.get("id", 0)
        visual = scene.get("visual", "")
        prompt = build_prompt(visual, tone)

        # Retry up to 3x
        result = None
        for attempt in range(3):
            result = generate_image(prompt, sid)
            if result:
                break
            print(f"  [retry {attempt+1}/3] waiting 30s...")
            time.sleep(30)

        log.append({
            "scene_id": sid,
            "visual"  : visual,
            "prompt"  : prompt,
            "output"  : result,
            "ok"      : result is not None
        })

        if result:
            success += 1

        time.sleep(20)  # jaga rate limit

    print(f"\n[visual_skill] Done: {success}/{len(scenes)} scenes")
    print(f"[visual_skill] Output: ./{OUTPUT_DIR}/")

    with open(LOG_FILE, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "model"       : MODEL,
            "scenes"      : log
        }, f, ensure_ascii=False, indent=2)

    print(f"[visual_skill] Log → {LOG_FILE}")
    print("="*55)

    if success == len(scenes):
        print("\n✅ Semua scene berhasil! Lanjut: python edit_skill.py")
    else:
        print(f"\n⚠️  {len(scenes)-success} scene gagal. Cek {LOG_FILE}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else SCRIPT_FILE
    run(path)

