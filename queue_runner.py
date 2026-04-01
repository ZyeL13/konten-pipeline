"""
queue_runner.py — Baca headline_queue.json, jalankan pipeline per item
Run: python queue_runner.py
     python queue_runner.py --max 3 --tone auto
"""

import json
import subprocess
import argparse
import sys
from pathlib import Path
from datetime import datetime

QUEUE_FILE = "headline_queue.json"

# Auto-tone logic: mapping keyword → tone number (dari TONES baru)
TONE_MAP = {
    "bitcoin"    : 1,   # the observer
    "crypto"     : 1,
    "collapse"   : 1,
    "fed"        : 4,   # the farmer (cyclical)
    "layoff"     : 8,   # the deserter
    "startup"    : 7,   # the last optimist
    "ai"         : 3,   # the archaeologist
    "model"      : 3,
    "openai"     : 3,
    "regulation" : 6,   # the witness
    "hack"       : 6,
    "war"        : 2,   # the inheritor
    "ipo"        : 5,   # the cartographer
    "data"       : 5,
}

def pick_tone_auto(headline: str) -> int:
    h = headline.lower()
    for keyword, tone_id in TONE_MAP.items():
        if keyword in h:
            return tone_id
    return 3  # default: the archaeologist

def load_queue() -> list:
    if not Path(QUEUE_FILE).exists():
        print(f"[ERROR] {QUEUE_FILE} not found. Run news_scanner.py --mode queue first.")
        sys.exit(1)
    with open(QUEUE_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_queue(queue: list):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max",  default=3, type=int,
                    help="Berapa headline yang diproses (default: 3)")
    ap.add_argument("--tone", default="auto",
                    help="Nomor tone 1-10, atau 'auto'")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--skip-visual", action="store_true")
    args = ap.parse_args()

    queue = load_queue()
    pending = [item for item in queue if not item.get("used")]

    if not pending:
        print("[INFO] Queue kosong atau semua sudah diproses.")
        print("[INFO] Jalankan: python news_scanner.py --mode queue")
        sys.exit(0)

    to_process = pending[:args.max]
    print(f"\n[queue_runner] {len(to_process)} headlines akan diproses\n")

    for i, item in enumerate(to_process, 1):
        headline = item["headline"]
        tone = pick_tone_auto(headline) if args.tone == "auto" else int(args.tone)

        print(f"\n{'='*55}")
        print(f"[{i}/{len(to_process)}] {headline[:70]}")
        print(f"  Source : {item['source']}")
        print(f"  Tone   : #{tone}")
        print(f"{'='*55}")

        cmd = [
            "python", "run_pipeline.py",
            headline,
            "--lang",  args.lang,
            "--tone",  str(tone),
        ]
        if args.skip_visual:
            cmd.append("--skip-visual")

        result = subprocess.run(cmd)

        # Tandai sebagai used regardless sukses/gagal
        item["used"] = True
        item["processed_at"] = datetime.now().isoformat()
        item["tone_used"] = tone
        item["exit_code"] = result.returncode
        save_queue(queue)

        if result.returncode != 0:
            print(f"[WARN] Pipeline exit {result.returncode} untuk headline ini — lanjut ke berikutnya")

    print(f"\n[queue_runner] Done. {len(to_process)} processed.")

if __name__ == "__main__":
    main()
