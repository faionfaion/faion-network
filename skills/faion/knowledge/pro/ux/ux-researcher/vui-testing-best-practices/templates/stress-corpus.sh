#!/usr/bin/env bash
# stress-corpus.sh — mix clean utterance fixtures with ambient noise stems at 3 SNR levels.
#
# Usage: bash stress-corpus.sh
# Requires: ffmpeg (apt install ffmpeg / brew install ffmpeg)
#
# Inputs:
#   fixtures/clean/   — WAV utterances (16kHz mono)
#   fixtures/noise/   — ambient noise stems: cafe.wav, traffic.wav, tv.wav
# Outputs:
#   fixtures/mixed/   — name: <utterance>_<noise>_<SNR>dB.wav

set -euo pipefail

CLEAN_DIR=fixtures/clean
NOISE_DIR=fixtures/noise
OUT=fixtures/mixed
mkdir -p "$OUT"

for u in "$CLEAN_DIR"/*.wav; do
  for n in "$NOISE_DIR"/*.wav; do
    for snr in 20 10 5; do
      base="$(basename "$u" .wav)_$(basename "$n" .wav)_${snr}dB.wav"
      ffmpeg -y -i "$u" -i "$n" \
        -filter_complex "[1:a]volume=-${snr}dB[bg];[0:a][bg]amix=inputs=2:duration=first" \
        "$OUT/$base" 2>/dev/null
    done
  done
done

echo "Mixed fixtures written to $OUT"
find "$OUT" -name "*.wav" | wc -l | xargs echo "Total files:"
