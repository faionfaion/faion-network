#!/usr/bin/env bash
# purpose: the ONLY marker writer. Identity-checked, flock-guarded, appends to history.
# consumes: an already-enrolled unit id, a lineage phase, a marker state, a reason.
# produces: phase-<phase>.<state> under the unit dir + one append-only history line.
# depends-on: checkpoint-ledger-spec.yaml (state_root, lineage, marker_states)
# token-budget-impact: none — pure filesystem.
#
# It does NOT create state directories. That is scripts/enrol.sh, and only enrol.sh
# (r1-identity-checked-before-write). A mistyped unit id must be an error here, not
# a new directory: the observed defect was a phantom unit that the dispatcher then
# offered to run from phase zero while the real unit was four of seven phases done.
#
# Usage: mark.sh <unit> <phase> <in-flight|done|failed> [reason]
# Exit:  0 written · 2 usage · 3 unknown unit · 4 unknown phase or state
set -euo pipefail

STATE_ROOT="${STATE_ROOT:-.pool/states}"
LINEAGE=(brief draft review publish)          # must match the spec, in order
STATES=(in-flight done failed)                # rolled-back is written by rollback.sh only

usage() { echo "usage: mark.sh <unit> <phase> <in-flight|done|failed> [reason]" >&2; exit 2; }
[ $# -ge 3 ] || usage

unit=$1; phase=$2; state=$3; reason=${4:-}
dir="$STATE_ROOT/$unit"

# --- r1: verify, never create. Loudly. ---
if [ ! -d "$dir" ]; then
  echo "mark.sh: unknown unit '$unit' — no state dir at $dir." >&2
  echo "         This is a typo or a missing enrol. Run: scripts/enrol.sh '$unit'" >&2
  exit 3
fi

contains() { local n=$1; shift; for x in "$@"; do [ "$x" = "$n" ] && return 0; done; return 1; }
contains "$phase" "${LINEAGE[@]}" || { echo "mark.sh: '$phase' is not in the lineage" >&2; exit 4; }
contains "$state" "${STATES[@]}"  || { echo "mark.sh: '$state' is not a marker state" >&2; exit 4; }

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# --- r3: one lock for the whole transition, so marker and history cannot diverge. ---
exec 9>"$STATE_ROOT/.lock"
flock 9

# in-flight is written BEFORE dispatch (r2), so refuse a second one: a live marker
# means the phase is already out, and re-dispatching it pays twice for one result.
if [ "$state" = "in-flight" ] && [ -e "$dir/phase-$phase.in-flight" ]; then
  echo "mark.sh: $unit/$phase already in-flight since $(cat "$dir/phase-$phase.in-flight")" >&2
  exit 4
fi

# A terminal state supersedes the in-flight marker for the same phase.
if [ "$state" != "in-flight" ]; then
  rm -f "$dir/phase-$phase.in-flight"
fi

if [ "$state" = "in-flight" ]; then
  printf '%s pid=%s %s\n' "$ts" "$$" "$reason" > "$dir/phase-$phase.in-flight"
else
  printf '%s %s\n' "$ts" "$reason" > "$dir/phase-$phase.$state"
fi

printf '%s %s %s %s\n' "$ts" "$phase" "$state" "${reason:--}" >> "$dir/history.log"
