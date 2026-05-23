#!/usr/bin/env bash
# check_tags_fresh.sh — CI gate. Regenerates the symbol index in a temp file,
# diffs against the committed `tags` file, exits non-zero on drift.
#
# Input : repo root with `.ctags.d/default.ctags` and committed `tags`.
# Output: non-zero exit + unified diff on drift; zero exit silent on match.

set -euo pipefail

CONFIG="${CTAGS_CONFIG:-.ctags.d/default.ctags}"
COMMITTED="${TAGS_FILE:-tags}"
FRESH="$(mktemp -t tags.fresh.XXXXXX)"
trap 'rm -f "$FRESH"' EXIT

if [[ ! -f "$CONFIG" ]]; then
  echo "FAIL: missing ctags config at $CONFIG" >&2
  exit 2
fi
if [[ ! -f "$COMMITTED" ]]; then
  echo "FAIL: missing committed tags file at $COMMITTED" >&2
  exit 2
fi

ctags --options="$CONFIG" -f "$FRESH" -R .

# Strip metadata lines (which include timestamps) before comparing.
strip_meta() { grep -v '^!_TAG_' "$1" | sort; }

if ! diff -u <(strip_meta "$COMMITTED") <(strip_meta "$FRESH") > /tmp/tags.drift.diff; then
  echo "FAIL: symbol index drift (committed != fresh)" >&2
  cat /tmp/tags.drift.diff >&2
  exit 1
fi

echo "OK: symbol index is fresh"
