#!/usr/bin/env python3
"""
Test refiner_agent.py tanpa render video.
"""

import json
from agents.refiner_agent import refine_script

# Sample script dengan typo
test_script = {
    "scenes": [
        {"id": 1, "text": "Bitcoin miners found cheap power. The sig n al is n t strong."},
        {"id": 2, "text": "Sola n a blockchain processes thousands of transactions."},
        {"id": 3, "text": "Customizatio nis not anfeature, it s the future."},
        {"id": 4, "text": "Binance an nounced new partnership with Chainlink."}
    ],
    "hook": "isnstructural?",
    "cta": "follow for more"
}

print("=" * 50)
print("BEFORE REFINEMENT:")
print("-" * 50)
for scene in test_script["scenes"]:
    print(f"Scene {scene['id']}: {scene['text']}")
print(f"Hook: {test_script['hook']}")

# Jalankan refinement
print("\n" + "=" * 50)
print("REFINING...")
print("=" * 50)

refined = refine_script(test_script)

print("\n" + "=" * 50)
print("AFTER REFINEMENT:")
print("-" * 50)
for scene in refined["scenes"]:
    print(f"Scene {scene['id']}: {scene['text']}")
print(f"Hook: {refined['hook']}")
