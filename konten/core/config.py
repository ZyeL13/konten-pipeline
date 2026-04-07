"""
core/config.py — Single source of truth for all config.
Priority: Groq API → ClawRouter fallback
"""

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# ── BASE PATHS ────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR   = BASE_DIR / "data"
MEMORY_DIR = BASE_DIR / "memory"

OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)

# ── QUEUE ─────────────────────────────────────────────────────────────────────
QUEUE_FILE  = DATA_DIR / "queue.json"
TRENDS_FILE = DATA_DIR / "trends.json"

# ── MEMORY ────────────────────────────────────────────────────────────────────
BEST_PERFORMANCE_FILE = MEMORY_DIR / "best_performance.json"
FAILED_CASES_FILE     = MEMORY_DIR / "failed_cases.json"

# ── API KEYS ──────────────────────────────────────────────────────────────────
GROQ_API_KEY       = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY     = os.environ.get("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── API URLS ──────────────────────────────────────────────────────────────────
# Primary: Groq API (has Whisper, better models, but TPD limit)
GROQ_URL_PRIMARY  = "https://api.groq.com/openai/v1"
# Fallback: ClawRouter (unlimited free models, no Whisper)
GROQ_URL_FALLBACK = "http://127.0.0.1:8402/v1"
# Active URL — used by agents (auto-selected, do not edit manually)
GROQ_URL          = GROQ_URL_PRIMARY

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# ── MODELS ────────────────────────────────────────────────────────────────────
# Groq primary model
GROQ_MODEL_PRIMARY  = "llama-3.3-70b-versatile"
# ClawRouter fallback models (in priority order)
GROQ_MODEL_FALLBACKS = [
    "free/deepseek-v3.2",
    "free/mistral-large-3-675b",
    "free/glm-4.7",
    "free/llama-4-maverick",
]
# Active model
GROQ_MODEL         = GROQ_MODEL_PRIMARY
GROQ_WHISPER_MODEL = "whisper-large-v3-turbo"  # Groq only, no fallback

# ── SCRIPT ────────────────────────────────────────────────────────────────────
SCRIPT_TEMPERATURE = 0.69
TARGET_DURATION    = 61

# ── VOICE ─────────────────────────────────────────────────────────────────────
TTS_VOICE  = os.environ.get("TTS_VOICE", "en-US-AndrewNeural")
TTS_RATE   = os.environ.get("TTS_RATE",  "-5%")
TTS_VOLUME = os.environ.get("TTS_VOLUME", "+0%")

# ── VISUAL ────────────────────────────────────────────────────────────────────
IMAGE_WIDTH   = 720
IMAGE_HEIGHT  = 1280
IMAGE_MODEL   = "flux"
STYLE_PREFIX  = (
    "cinematic dark aesthetic, moody lighting, high contrast, "
    "digital art, 4k quality, no text, no watermark, "
)
AUDITOR_VISUAL_STYLE = (
    "forensic cold light, institutional spaces, long shadows, "
    "grain film texture, no people or blurred background figures only, "
)

# ── VIDEO ─────────────────────────────────────────────────────────────────────
VIDEO_WIDTH         = 720
VIDEO_HEIGHT        = 1280
VIDEO_FPS           = 30
SUBTITLE_FONT_SIZE  = 28
SUBTITLE_FONT_COLOR = "white"
SUBTITLE_BOX_COLOR  = "black@0.6"

# ── QC ────────────────────────────────────────────────────────────────────────
QC_N_FRAMES    = 1
QC_FRAME_DELAY = 60


# ── CHARACTER OVERLAY ─────────────────────────────────────────────────────────
CHAR_SCALE    = 220      # character width in pixels
CHAR_OPACITY  = 0.95     # 0.0 = invisible, 1.0 = fully opaque
CHAR_POSITION = "bottom-left"  # bottom-left | bottom-right | top-left | top-right

def validate():
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if missing:
        print(f"[config] WARNING: Missing env vars: {', '.join(missing)}")
    return len(missing) == 0

