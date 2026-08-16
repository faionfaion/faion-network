#!/usr/bin/env bash
#
# Corpus validators, in a form a pre-commit hook can gate on.
#
# The problem this solves: the corpus has KNOWN, pre-existing failures
# (9 methodologies with no `06-decision-tree.xml`, 2 templates with no
# 5-line header, 6 methodology dirs failing v2, and a
# `validate-playbook-v3.py` that fails 455/455 because the validator is
# broken, not the content). A hook that gated on "everything passes"
# would block every commit forever; a hook that gated on COUNTS would
# wave through a swap — one failure fixed, one introduced.
#
# So the gate is on the failure SET. Every validator's `FAIL <path>`
# lines are normalised to `<validator-id>\t<repo-relative-path>` and
# diffed against a committed baseline. A line that is present now and
# absent from the baseline is a NEW failure and blocks. A line in the
# baseline that no longer appears is a FIX: reported, never blocking,
# with the command to refresh the baseline.
#
# Usage:
#   check-validators.sh --fast                 the per-commit set (~6 s)
#   check-validators.sh --methodology DIR...   scoped v2, per changed slug
#   check-validators.sh --all                  fast + the full v2 sweep (~3.5 min)
#   check-validators.sh --write-baseline       --all, written to the baseline file
#   check-validators.sh --check-fast [DIR...]  --fast + scoped v2, diffed vs baseline
#   check-validators.sh --check-all            --all, diffed vs baseline
set -uo pipefail
cd "$(dirname "$0")/.."
ROOT=$PWD

# Fresh clone, first dev command: point git at the tracked hooks.
./scripts/install-hooks.sh --quiet 2>/dev/null || true

BASELINE=scripts/validator-baseline.txt

# The per-commit set. Every one of these runs the whole corpus and
# still finishes in about six seconds, so there is no reason to scope
# them — measured 2026-08-14:
#   domains-index 0.1s · domain-index 0.1s · decision-tree 2.1s ·
#   templates 0.8s · scripts 0.7s · lexicon 1.5s · recipes 0.7s ·
#   fragments 0.1s · tools 0.1s
#
# Deliberately NOT here:
#   * validate-methodology-v2 over the whole tree — 205 s, because the
#     runner spawns one python per slug over 2,639 slugs. It runs
#     SCOPED per commit (only the slugs the commit touched) and in full
#     only in the manual sweep.
#   * validate-playbook-v3.py — 0/455, and the finding is that the
#     validator wants YAML frontmatter no playbook AGENTS.md has ever
#     carried. Gating on a broken validator teaches people to ignore
#     the gate. It stays out until it is repaired.
FAST_IDS=(domains-index domain-index decision-tree templates scripts lexicon recipes fragments tools vars-dictionary crosslinks)
fast_cmd() {
  case "$1" in
    domains-index) echo "scripts/validate-domains-index.py" ;;
    domain-index)  echo "scripts/validate-domain-index.py --all" ;;
    decision-tree) echo "scripts/validate-methodology-decision-tree.py --all" ;;
    templates)     echo "scripts/validate-methodology-templates.py --all" ;;
    scripts)       echo "scripts/validate-methodology-scripts.py --all" ;;
    lexicon)       echo "scripts/validate-lexicon.py" ;;
    recipes)       echo "scripts/validate-recipes.py" ;;
    fragments)     echo "scripts/validate-fragments.py" ;;
    tools)         echo "scripts/validate-tools.py" ;;
    vars-dictionary) echo "scripts/validate-vars-dictionary.py" ;;
    crosslinks)    echo "scripts/sync-crosslinks-to-meta.py --check" ;;
  esac
}

# normalise turns one validator's stdout+stderr into baseline lines.
# Absolute paths become repo-relative so a baseline is portable between
# clones; a validator that fails without printing a single FAIL line
# still contributes one row, so a silent breakage cannot slip past a
# set comparison that only looks at FAIL.
normalise() {
  local id=$1 rc=$2 out=$3
  local fails
  fails=$(printf '%s\n' "$out" \
    | grep -E '^FAIL ' \
    | sed -e "s|^FAIL ||" -e "s|^$ROOT/||" -e 's|/*$||' \
    | sed "s|^|$id\t|" \
    | LC_ALL=C sort -u)
  if [[ -n "$fails" ]]; then
    printf '%s\n' "$fails"
  elif (( rc != 0 )); then
    printf '%s\tEXIT:%d\n' "$id" "$rc"
  fi
}

run_fast() {
  local id out rc
  for id in "${FAST_IDS[@]}"; do
    # shellcheck disable=SC2046  # word splitting is the point: cmd + flags
    out=$(python3 $(fast_cmd "$id") 2>&1); rc=$?
    normalise "$id" "$rc" "$out"
  done
}

# run_methodology validates the given slug directories with v2. Callers
# pass only the dirs a commit touched; the full sweep passes all of them.
run_methodology() {
  local dir out rc
  for dir in "$@"; do
    [[ -d "$dir" ]] || continue
    out=$(python3 scripts/validate-methodology-v2.py "$dir" 2>&1); rc=$?
    normalise "methodology-v2" "$rc" "$out"
  done
}

all_methodology_dirs() {
  find skills/faion/knowledge -name AGENTS.md -printf '%h\n' | LC_ALL=C sort
}

# compare blocks on lines present now and absent from the baseline.
compare() {
  local current=$1 scope=$2
  if [[ ! -f "$BASELINE" ]]; then
    echo "check-validators: $BASELINE is missing — run: scripts/check-validators.sh --write-baseline" >&2
    return 1
  fi

  # The baseline is a data file with a comment header; only its rows
  # take part in the comparison.
  baseline_rows() { grep -v '^#' "$BASELINE" | grep -v '^[[:space:]]*$' | LC_ALL=C sort -u; }

  local new
  new=$(LC_ALL=C comm -23 <(LC_ALL=C sort -u "$current") <(baseline_rows))
  if [[ -n "$new" ]]; then
    echo "check-validators: NEW validator failures (not in the baseline):" >&2
    printf '%s\n' "$new" | sed 's/^/    /' >&2
    return 1
  fi

  # Fixes are reported, never blocking — a commit that repairs corpus
  # content should not have to also curate a baseline file to land.
  if [[ "$scope" == "all" ]]; then
    local fixed
    fixed=$(LC_ALL=C comm -13 <(LC_ALL=C sort -u "$current") <(baseline_rows))
    if [[ -n "$fixed" ]]; then
      echo "check-validators: baseline failures no longer reproduce:" >&2
      printf '%s\n' "$fixed" | sed 's/^/    /' >&2
      echo "  refresh with: scripts/check-validators.sh --write-baseline" >&2
    fi
  fi
  return 0
}

MODE=${1:---fast}
shift || true
TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT

case "$MODE" in
  --fast)
    run_fast
    ;;
  --methodology)
    run_methodology "$@"
    ;;
  --all)
    { run_fast; run_methodology $(all_methodology_dirs); } | LC_ALL=C sort -u
    ;;
  --write-baseline)
    { run_fast; run_methodology $(all_methodology_dirs); } | LC_ALL=C sort -u >"$TMP"
    {
      echo "# Known, pre-existing corpus validator failures."
      echo "# Format: <validator-id>\t<repo-relative-path>"
      echo "# The pre-commit hook blocks on lines NOT in this file."
      echo "# Regenerate: scripts/check-validators.sh --write-baseline"
      cat "$TMP"
    } >"$BASELINE"
    echo "check-validators: wrote $(grep -cv '^#' "$BASELINE") baseline entries to $BASELINE"
    ;;
  --check-fast)
    { run_fast; run_methodology "$@"; } | LC_ALL=C sort -u >"$TMP"
    compare "$TMP" fast
    ;;
  --check-all)
    { run_fast; run_methodology $(all_methodology_dirs); } | LC_ALL=C sort -u >"$TMP"
    compare "$TMP" all
    ;;
  *)
    echo "check-validators: unknown mode $MODE" >&2
    exit 2
    ;;
esac
