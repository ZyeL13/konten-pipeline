"""
pick_variation.py
Pilih 1 variasi dari variations_output.json → simpan sebagai script_output.json
Siap untuk diproses voice_skill.py

Run: python pick_variation.py        ← interactive, tampil semua pilihan
     python pick_variation.py 1      ← langsung pilih variasi #1
"""

import json
import sys
from pathlib import Path

VARIATIONS_FILE = "variations_output.json"
OUTPUT_FILE     = "script_output.json"

def load_variations() -> dict:
    p = Path(VARIATIONS_FILE)
    if not p.exists():
        print(f"[ERROR] {VARIATIONS_FILE} tidak ada.")
        print("  Jalankan variation_skill.py dulu.")
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def show_menu(data: dict):
    print("\n" + "="*55)
    print("PILIH VARIASI SCRIPT")
    print("="*55)
    print(f"Headline: {data.get('headline', '')}\n")
    for v in data.get("variations", []):
        total = sum(s.get("duration", 0) for s in v.get("scenes", []))
        print(f"  [{v['id']:02d}] {v['tone'].upper()}")
        print(f"       Hook: {v['hook'][:65]}...")
        print(f"       Dur : {total}s | Hashtags: {' '.join(v.get('hashtags', [])[:3])}")
        print()
    print("="*55)

def pick(data: dict, choice: int) -> dict:
    variations = data.get("variations", [])
    match = next((v for v in variations if v["id"] == choice), None)
    if not match:
        print(f"[ERROR] Variasi #{choice} tidak ada.")
        sys.exit(1)

    # Format ulang supaya kompatibel dengan voice_skill.py
    script = {
        "topic"          : data.get("headline", ""),
        "platform"       : ["tiktok", "ig_reels", "yt_shorts"],
        "total_duration" : match.get("total_duration", 61),
        "hook"           : match.get("hook", ""),
        "scenes"         : match.get("scenes", []),
        "cta"            : match.get("cta", ""),
        "caption"        : {
            "tiktok"   : match.get("caption", ""),
            "ig_reels" : match.get("caption", ""),
            "yt_shorts": match.get("caption", "")
        },
        "hashtags"       : match.get("hashtags", []),
        "_source"        : {
            "tone"      : match.get("tone", ""),
            "variation" : choice
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Variasi #{choice} ({match['tone']}) → {OUTPUT_FILE}")
    print(f"     Hook : {match['hook']}")
    print(f"\nLanjut generate voice:")
    print(f"  python voice_skill.py")
    return script

# ── ENTRY POINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    data = load_variations()

    if len(sys.argv) > 1:
        try:
            choice = int(sys.argv[1])
        except ValueError:
            print("[ERROR] Masukkan nomor variasi (1-10)")
            sys.exit(1)
    else:
        show_menu(data)
        try:
            choice = int(input("Pilih nomor variasi (1-10): ").strip())
        except (ValueError, KeyboardInterrupt):
            print("\n[CANCEL]")
            sys.exit(0)

    pick(data, choice)

