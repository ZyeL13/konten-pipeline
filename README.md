# openclaw-pipeline 🎬

Autonomous AI video pipeline — runs fully from Android Termux.  
**$0/month. No GPU. No laptop.**

## Stack
| Step | Tool | Cost |
|------|------|------|
| Script gen | Groq API (LLaMA 3.3 70B) | Free |
| Voice | Edge TTS (Microsoft Neural) | Free |
| Images | Pollinations.ai (FLUX) | Free |
| Video edit | FFmpeg | Free |

## Output
- 9:16 vertical video (720×1280)
- 61 seconds (YouTube Shorts monetization threshold)
- 10 tone variations per headline
- Ready for TikTok / IG Reels / YouTube Shorts

## Setup

```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg -y
pip install requests edge-tts gtts
```

Add ke `.env`:
```
GROQ_API_KEY=gsk_...
```

## Run

```bash
source .env

# Full pipeline
python run_pipeline.py "your headline here" --lang id --tone 1

# English, conspiracy tone
python run_pipeline.py "AI replaced 1 million jobs" --lang en --tone 6
```

## Tones (1-10)
1. Dark & mysterious
2. Urgent breaking news
3. Sarcastic & cynical
4. Storytelling narrative
5. Data-driven analyst
6. Conspiracy theory
7. Motivational hustle
8. Fear & warning
9. Poetic & philosophical
10. Casual Gen-Z slang

## Output Structure
```
output/
└── 20260331_105840/
    ├── variations_output.json
    ├── script_output.json
    ├── voice.mp3
    ├── final_video.mp4
    └── scenes/
```

## Skills
- `variation_skill.py` — 10 script variations from 1 headline
- `pick_variation.py` — select tone → export script
- `script_skill.py` — single script generator
- `voice_skill.py` — Edge TTS bilingual (id/en)
- `visual_skill.py` — Pollinations FLUX image gen
- `edit_skill.py` — FFmpeg assembly (Ken Burns + subtitle + audio)
- `run_pipeline.py` — one-command orchestrator

