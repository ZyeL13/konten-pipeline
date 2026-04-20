#!/bin/bash

# kirim.sh — Upload final video content to destination
# Usage: ./kirim.sh /path/to/run_dir

RUN_DIR="$1"
JOB_ID=$(basename "$RUN_DIR" | cut -d'_' -f2)

if [ -z "$RUN_DIR" ]; then
    echo "Usage: $0 <run_dir_path>"
    exit 1
fi

if [ ! -d "$RUN_DIR" ]; then
    echo "Error: Directory $RUN_DIR does not exist"
    exit 1
fi

echo "=== KIRIM.SH START ==="
echo "Job ID: $JOB_ID"
echo "Run Dir: $RUN_DIR"
echo "Timestamp: $(date)"

# Find the final video file (assuming .mp4 extension)
VIDEO_FILE=$(find "$RUN_DIR" -name "*.mp4" -type f | head -1)

if [ -z "$VIDEO_FILE" ]; then
    echo "Warning: No .mp4 file found in $RUN_DIR"
    exit 1
fi

echo "Video file: $VIDEO_FILE"
echo "Video size: $(du -h "$VIDEO_FILE" | cut -f1)"

# === UPLOAD LOGIC ===
# Replace this section with your actual upload command
# Examples:
# - YouTube upload: youtube-upload --title="Content" "$VIDEO_FILE"
# - Rclone to cloud: rclone copy "$VIDEO_FILE" remote:folder/
# - SCP to server: scp "$VIDEO_FILE" user@server:/path/
# - Custom API upload

echo "=== UPLOAD SIMULATION ==="
echo "This is a template. Replace with actual upload command."
echo "Example commands:"
echo "  youtube-upload --title=\"AI News $JOB_ID\" \"$VIDEO_FILE\""
echo "  rclone copy \"$VIDEO_FILE\" gdrive:/videos/"
echo "  scp \"$VIDEO_FILE\" user@server:/var/www/videos/"
echo ""
echo "Video would be uploaded: $VIDEO_FILE"

# Uncomment and modify one of these:
# youtube-upload --title="AI Content $JOB_ID" "$VIDEO_FILE"
# rclone copy "$VIDEO_FILE" your-remote:/videos/
# scp "$VIDEO_FILE" your-server:/path/to/videos/

echo "=== KIRIM.SH COMPLETE ==="
echo "Job $JOB_ID processing finished"