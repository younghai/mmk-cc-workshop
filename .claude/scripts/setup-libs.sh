#!/bin/sh
# Install libraries needed for this project
# Runs at SessionStart — always exits 0 so it never blocks the session

echo "=== Installing Libraries ==="

# yt-dlp: download YouTube transcripts
if command -v yt-dlp >/dev/null 2>&1; then
  echo "yt-dlp    : $(yt-dlp --version) (already installed)"
else
  echo "yt-dlp    : installing..."
  pip install -q yt-dlp 2>/dev/null || pip3 install -q yt-dlp 2>/dev/null || {
    echo "yt-dlp    : FAILED (pip not available)"
    echo "=== Done ==="
    exit 0
  }
  echo "yt-dlp    : $(yt-dlp --version) (installed)"
fi

echo "=== Done ==="
exit 0
