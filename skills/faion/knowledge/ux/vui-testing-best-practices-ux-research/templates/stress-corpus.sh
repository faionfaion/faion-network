#!/usr/bin/env bash
# purpose: Generate stress fixtures via SNR mixing
# consumes: clean utterances + noise stems
# produces: mixed WAV at 20/10/5dB
# depends-on: ffmpeg
# token-budget-impact: ~150
set -euo pipefail
CLEAN_DIR=${1:-fixtures/clean}
NOISE_DIR=${2:-fixtures/noise}
OUT=${3:-fixtures/mixed}
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
