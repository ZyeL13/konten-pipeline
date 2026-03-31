#!/data/data/com.termux/files/usr/bin/bash
# setup_piper.sh
# One-shot setup Piper TTS di Termux Android (ARM64/aarch64)
# Jalankan sekali saja: bash setup_piper.sh

set -e

echo ""
echo "================================================"
echo "  PIPER TTS SETUP — Termux Android"
echo "================================================"

# ── 1. Install dependencies ─────────────────────────────────────────────────
echo "[1/5] Install packages..."
pkg update -y -q
pkg install -y wget ffmpeg

# ── 2. Download Piper binary (aarch64 = ARM64 Android) ─────────────────────
echo "[2/5] Download Piper binary..."
mkdir -p ~/piper
cd ~/piper

PIPER_URL="https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz"

if [ ! -f "piper" ]; then
    wget -q --show-progress "$PIPER_URL" -O piper_aarch64.tar.gz
    tar -xzf piper_aarch64.tar.gz
    rm piper_aarch64.tar.gz
    chmod +x piper
    echo "[OK] Piper binary ready → ~/piper/piper"
else
    echo "[SKIP] Piper binary sudah ada"
fi

# ── 3. Download Voice Models ────────────────────────────────────────────────
echo "[3/5] Download voice models..."
mkdir -p ~/piper/models
cd ~/piper/models

BASE_URL="https://huggingface.co/rhasspy/piper-voices/resolve/main"

download_model() {
    local lang_path=$1
    local model_name=$2
    if [ ! -f "${model_name}.onnx" ]; then
        echo "  → Downloading ${model_name}..."
        wget -q --show-progress "${BASE_URL}/${lang_path}/${model_name}.onnx" -O "${model_name}.onnx"
        wget -q "${BASE_URL}/${lang_path}/${model_name}.onnx.json" -O "${model_name}.onnx.json"
        echo "  [OK] ${model_name}"
    else
        echo "  [SKIP] ${model_name} sudah ada"
    fi
}

# Indonesian female voice (~67MB)
download_model "id/id_ID/argapati/medium" "id_ID-argapati-medium"

# English male deep voice (~67MB) — untuk konten English
download_model "en/en_US/ryan/medium" "en_US-ryan-medium"

# ── 4. Test Piper ───────────────────────────────────────────────────────────
echo "[4/5] Testing Piper..."
cd ~/piper

TEST_TEXT="Sistem aktif. Pipeline siap dijalankan."
echo "$TEST_TEXT" | ./piper \
    --model models/id_ID-argapati-medium.onnx \
    --output_file test_voice.wav \
    --length_scale 1.25 2>/dev/null

if [ -f "test_voice.wav" ]; then
    SIZE=$(wc -c < test_voice.wav)
    echo "[OK] Test WAV generated (${SIZE} bytes) → ~/piper/test_voice.wav"
    # Convert to MP3 untuk cek
    ffmpeg -y -i test_voice.wav -q:a 2 test_voice.mp3 2>/dev/null
    echo "[OK] Test MP3 → ~/piper/test_voice.mp3"
    echo ""
    echo "  Coba dengarkan:"
    echo "  termux-media-player play ~/piper/test_voice.mp3"
else
    echo "[WARN] Test gagal. Cek binary compatibility."
fi

# ── 5. Summary ──────────────────────────────────────────────────────────────
echo ""
echo "[5/5] Setup complete!"
echo "================================================"
echo "  Binary : ~/piper/piper"
echo "  Models :"
ls ~/piper/models/*.onnx 2>/dev/null | while read f; do
    echo "    - $(basename $f)"
done
echo ""
echo "  Voices tersedia di voice_skill.py:"
echo "    id_female  → id_ID-argapati-medium (Indonesian)"
echo "    en_male    → en_US-ryan-medium (English deep)"
echo ""
echo "  Ganti voice:"
echo "    export PIPER_VOICE=en_male"
echo ""
echo "  Ganti kecepatan (default 1.25 = cinematic slow):"
echo "    export PIPER_SPEED=1.0   # normal"
echo "    export PIPER_SPEED=1.4   # lebih lambat"
echo ""
echo "  Run pipeline:"
echo "    python script_skill.py 'topik kamu' && python voice_skill.py"
echo "================================================"

