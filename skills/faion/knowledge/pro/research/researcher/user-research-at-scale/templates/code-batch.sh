# purpose: Bash launcher: coding-frozen-book agent over a batch of transcripts
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
#!/usr/bin/env bash
# code-batch.sh — run theme-coder agent over a transcript directory
# Input: transcripts/*.json (one file per session)
# Output: .aidocs/research/coded/*.jsonl + coded.parquet
# Skips already-coded transcripts (idempotent via output file check).
set -euo pipefail

CODEBOOK=.aidocs/research/codebook.yaml
PROMPTS=prompts/theme-coder.xml
OUT=.aidocs/research/coded
mkdir -p "$OUT"

for f in transcripts/*.json; do
  base=$(basename "$f" .json)
  if [ -f "$OUT/$base.jsonl" ]; then
    echo "skip: $base (already coded)"
    continue
  fi
  echo "coding: $base"
  claude -p "$(cat "$PROMPTS")" \
    --input-file "$f" \
    --context-file "$CODEBOOK" \
    --output-file "$OUT/$base.jsonl" \
    --model claude-sonnet-4-5
done

# Aggregate coded JSONL into parquet for analysis
duckdb -c "COPY (SELECT * FROM read_json_auto('$OUT/*.jsonl')) TO 'coded.parquet'"
echo "Parquet written: coded.parquet"
