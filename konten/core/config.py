"""
core/config.py — Single source of truth for all config.
Priority (2026-04-07): ClawRouter (free/deepseek-v3.2) → Groq fallback
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── BASE PATHS ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"
MEMORY_DIR = BASE_DIR / "memory"
for d in (OUTPUT_DIR, DATA_DIR, MEMORY_DIR):
    d.mkdir(exist_ok=True)

# ── QUEUE & MEMORY ────────────────────────────────────────────────────────────
QUEUE_FILE = DATA_DIR / "queue.json"
TRENDS_FILE = DATA_DIR / "trends.json"
BEST_PERFORMANCE_FILE = MEMORY_DIR / "best_performance.json"
FAILED_CASES_FILE = MEMORY_DIR / "failed_cases.json"

# ── API KEYS ──────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── API URLS ──────────────────────────────────────────────────────────────────
GROQ_URL_PRIMARY = "http://127.0.0.1:8402/v1"   # ClawRouter local
GROQ_URL_FALLBACK = "https://api.groq.com/openai/v1"
GROQ_URL = GROQ_URL_PRIMARY
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# ── MODELS ────────────────────────────────────────────────────────────────────
GROQ_MODEL_PRIMARY = "free/deepseek-v3.2"
GROQ_MODEL_QC = "llama-3.3-70b-versatile"
GROQ_MODEL_FALLBACKS = [
    "llama-3.3-70b-versatile",
    "free/mistral-large-3-675b",
    "free/glm-4.7",
]
GROQ_MODEL = GROQ_MODEL_PRIMARY
GROQ_WHISPER_MODEL = "whisper-large-v3-turbo"

# ── VALIDATION THRESHOLDS ─────────────────────────────────────────────────────
SCRIPT_MIN_WORDS_TOTAL = 80
SCRIPT_MIN_WORDS_SCENE = 20
SCRIPT_TARGET_WORDS = 125

# ── SCRIPT GENERATION ─────────────────────────────────────────────────────────
SCRIPT_TEMPERATURE = 0.85
TARGET_DURATION = 61

# ── VOICE ─────────────────────────────────────────────────────────────────────
TTS_VOICE = os.environ.get("TTS_VOICE", "en-US-AndrewNeural")
TTS_RATE = os.environ.get("TTS_RATE", "-5%")
TTS_VOLUME = os.environ.get("TTS_VOLUME", "+0%")

# ── VISUAL ────────────────────────────────────────────────────────────────────
IMAGE_WIDTH = 720
IMAGE_HEIGHT = 1280
IMAGE_MODEL = "flux"
STYLE_PREFIX = (
    "cinematic dark aesthetic, moody lighting, high contrast, "
    "digital art, 4k quality, no text, no watermark, "
)
AUDITOR_VISUAL_STYLE = (
    "forensic cold light, institutional spaces, long shadows, "
    "grain film texture, no people or blurred background figures only, "
)

# ── VIDEO ─────────────────────────────────────────────────────────────────────
VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280
VIDEO_FPS = 30
SUBTITLE_FONT_SIZE = 28
SUBTITLE_FONT_COLOR = "white"
SUBTITLE_BOX_COLOR = "black@0.6"

# ── QC ────────────────────────────────────────────────────────────────────────
QC_N_FRAMES = 1
QC_FRAME_DELAY = 60

# ── CHARACTER OVERLAY ─────────────────────────────────────────────────────────
CHAR_SCALE = 280
CHAR_OPACITY = 0.95
CHAR_POSITION = "bottom-left"

def validate():
    missing = [k for k, v in {
        "GROQ_API_KEY": GROQ_API_KEY,
        "GEMINI_API_KEY": GEMINI_API_KEY,
    }.items() if not v]
    if missing:
        print(f"[config] WARNING: Missing env vars: {', '.join(missing)}")
    return len(missing) == 0
