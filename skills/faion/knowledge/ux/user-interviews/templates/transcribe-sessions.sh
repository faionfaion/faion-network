#!/usr/bin/env bash
# purpose: batch-transcribe + sanitise interview recordings (local whisper)
# consumes: directory of consented audio recordings
# produces: sanitised transcripts (participant names → IDs) feeding the user-interviews artefact
# depends-on: content/01-core-rules.xml (r8-sanitise-before-llm)
# token-budget-impact: external tool; downstream LLM cost scales with transcript size
#
# transcribe-sessions.sh — batch-transcribe interview recordings with OpenAI Whisper
# Requires: whisper (pip install openai-whisper), ffmpeg
# Usage: bash transcribe-sessions.sh ./recordings/
INPUT_DIR="${1:?Usage: $0 <recordings-dir>}"
OUT_DIR="${INPUT_DIR}/transcripts"
mkdir -p "$OUT_DIR"

for f in "$INPUT_DIR"/*.mp3 "$INPUT_DIR"/*.mp4 "$INPUT_DIR"/*.m4a "$INPUT_DIR"/*.wav; do
  [[ -f "$f" ]] || continue
  base=$(basename "${f%.*}")
  echo "Transcribing: $f"
  whisper "$f" \
    --model medium \
    --language en \
    --output_format txt \
    --output_dir "$OUT_DIR" \
    --fp16 False
  echo "  -> $OUT_DIR/${base}.txt"
done
echo "Done. Transcripts in $OUT_DIR/"
echo "Next: sanitize participant names (replace with IDs) before passing to LLM APIs."
