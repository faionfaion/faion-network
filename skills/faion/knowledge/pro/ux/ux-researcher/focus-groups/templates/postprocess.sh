#!/usr/bin/env bash
# postprocess.sh — focus group post-processing pipeline.
#
# Flow: MP4 recording → audio extract → WhisperX diarize → Claude theme extraction
#
# Usage: bash postprocess.sh path/to/session.mp4
# Requires: ffmpeg, whisperx, python3, anthropic SDK
# Set: HF_TOKEN (HuggingFace token for diarization model)
#       ANTHROPIC_API_KEY

set -euo pipefail

SESSION="$1"
WORK="out/$(basename "$SESSION" .mp4)"
PROMPTS_DIR="$(dirname "$0")"
mkdir -p "$WORK"

echo "Step 1: Extract audio"
ffmpeg -i "$SESSION" -vn -ac 1 -ar 16000 "$WORK/audio.wav" -y

echo "Step 2: Transcribe + diarize"
whisperx "$WORK/audio.wav" \
  --model large-v3 \
  --diarize \
  --hf_token "${HF_TOKEN}" \
  --output_dir "$WORK"

echo "Step 3: Extract themes via Claude"
python3 - <<'PYEOF'
import json, anthropic, pathlib, sys, os

work = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("WORK")
transcript_path = pathlib.Path(work) / "audio.json"
transcript = transcript_path.read_text()

client = anthropic.Anthropic()
theme_prompt = (
    "Transcript (speaker-labeled): {transcript}\n\n"
    "Extract 3-7 themes. For each:\n"
    "- theme_name: string\n"
    "- supporting_quotes: list of {speaker_id, verbatim_quote}\n"
    "- consensus: unanimous|majority|split|minority\n"
    "- dominance_flag: true if one speaker drives this theme alone\n\n"
    "Also produce a 'dissent' section: list any disagreements or tensions with quote evidence.\n"
    "Return JSON only."
).format(transcript=transcript[:40000])

msg = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4000,
    temperature=0,
    messages=[{"role": "user", "content": theme_prompt}],
)
pathlib.Path(work, "themes.json").write_text(msg.content[0].text)
print(f"Themes written to {work}/themes.json")
PYEOF

echo "Done. Review: $WORK/themes.json"
