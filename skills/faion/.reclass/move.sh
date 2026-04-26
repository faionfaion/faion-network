#!/usr/bin/env bash
# Apply moves from candidates.safe.tsv via git mv.
# Each line: current \t guess \t MOVE \t source_path
# Destination: knowledge/<guess>/<group>/<domain>/<methodology>
# Creates destination domain folder if needed.

set -euo pipefail

REPO_ROOT=/home/nero/workspace/projects/faion-net/faion-network
SCRIPT_DIR=$REPO_ROOT/skills/faion/.reclass
cd "$REPO_ROOT"

SAFE="$SCRIPT_DIR/candidates.safe.tsv"
LOG="$SCRIPT_DIR/decisions.log"
APPLIED="$SCRIPT_DIR/candidates.applied.tsv"

: >"$APPLIED"

count=0
while IFS=$'\t' read -r current guess verdict src; do
  [[ "$verdict" == "MOVE" ]] || continue
  # src: skills/faion/knowledge/<current>/<group>/<domain>/<methodology>
  rel=${src#skills/faion/knowledge/}
  # rel: <current>/<group>/<domain>/<methodology>
  IFS='/' read -r _cur group domain methodology <<<"$rel"
  dst="skills/faion/knowledge/$guess/$group/$domain/$methodology"

  if [[ ! -d "$src" ]]; then
    printf 'SKIP_missing\t%s\n' "$src" >>"$LOG"
    continue
  fi
  if [[ -e "$dst" ]]; then
    printf 'SKIP_exists\t%s -> %s\n' "$src" "$dst" >>"$LOG"
    continue
  fi

  mkdir -p "$(dirname "$dst")"
  git mv "$src" "$dst" 2>/dev/null || { printf 'FAIL\t%s -> %s\n' "$src" "$dst" >>"$LOG"; continue; }
  printf 'MOVED\t%s -> %s\n' "$src" "$dst" >>"$LOG"
  printf '%s\t%s\t%s\t%s\n' "$current" "$guess" "APPLIED" "$dst" >>"$APPLIED"
  count=$((count+1))
done <"$SAFE"

echo "Applied: $count moves"
echo "Log: $LOG"
