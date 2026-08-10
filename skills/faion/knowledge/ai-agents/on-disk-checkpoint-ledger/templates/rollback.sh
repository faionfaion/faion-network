#!/usr/bin/env bash
# purpose: truncate-and-requeue a unit to a phase — the verb retry cannot express.
# consumes: an enrolled unit id, a lineage phase to return to, a reason.
# produces: markers at/after that phase removed, one rolled-back history line, unit requeued.
# depends-on: checkpoint-ledger-spec.yaml (lineage order); templates/mark.sh (same lock)
# token-budget-impact: none at run time; saves the re-dispatch of phases before <phase>.
#
# Retry re-runs a phase on top of what the failed attempt left behind — correct for a
# crash, wrong for an output that succeeded and was wrong, because downstream phases
# already consumed it. Rollback removes every marker at or after <phase> in LINEAGE
# order, records that it did so, and requeues there (r5-rollback-is-truncate-and-requeue).
#
# The rolled-back line is the point of the exercise: after this runs, a missing marker
# is a recorded outcome, not evidence the phase never started. Without the line the
# next tick re-derives "never started" and silently redoes finished work.
#
# Usage: rollback.sh <unit> <phase> <reason>
# Exit:  0 rolled back · 2 usage · 3 unknown unit · 4 unknown phase
set -euo pipefail

STATE_ROOT="${STATE_ROOT:-.pool/states}"
QUEUE="${QUEUE:-.pool/QUEUE}"
ARCHIVE="${ARCHIVE:-.pool/rollback}"
LINEAGE=(brief draft review publish)          # must match the spec, in order

[ $# -ge 3 ] || { echo "usage: rollback.sh <unit> <phase> <reason>" >&2; exit 2; }
unit=$1; phase=$2; reason=$3
dir="$STATE_ROOT/$unit"

# --- r1: verify identity before touching anything. ---
[ -d "$dir" ] || { echo "rollback.sh: unknown unit '$unit' — no state dir at $dir" >&2; exit 3; }

start=-1
for i in "${!LINEAGE[@]}"; do [ "${LINEAGE[$i]}" = "$phase" ] && start=$i; done
[ "$start" -ge 0 ] || { echo "rollback.sh: '$phase' is not in the lineage" >&2; exit 4; }

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)

exec 9>"$STATE_ROOT/.lock"
flock 9

# Keep the artefacts. A rollback that destroys the evidence makes the postmortem
# impossible, and the wrong output is usually the only copy of what went wrong.
mkdir -p "$ARCHIVE/$unit/$ts"
for ((i = start; i < ${#LINEAGE[@]}; i++)); do
  p=${LINEAGE[$i]}
  for m in "$dir/phase-$p."*; do
    [ -e "$m" ] || continue
    mv "$m" "$ARCHIVE/$unit/$ts/"
  done
done

# --- r3: append, never rewrite. This line is what makes the truncation legible. ---
printf '%s %s rolled-back %s\n' "$ts" "$phase" "$reason" >> "$dir/history.log"

# --- Requeue at the rolled-back phase. Amend the brief before the next tick picks it up. ---
printf '%s|%s\n' "$unit" "$phase" >> "$QUEUE"
echo "rolled back $unit to $phase; markers archived in $ARCHIVE/$unit/$ts"
