# On-Disk Checkpoint Ledger

## Summary

**One-sentence:** Produces a Checkpoint Ledger Spec that gives a bash-and-cron agent orchestrator durable resume, per-unit history and real rollback — using a state directory, marker files and `flock`, with no framework, no database and no runtime Python.

**One-paragraph:** Durable checkpointing is the one capability the orchestration frameworks genuinely added: a run that survives a crash, a history you can replay to any earlier point, and a human gate that can stay open indefinitely without holding a process. None of that requires their runtime. The mechanism is four things on disk — an identity that is verified before any write, a marker written *before* dispatch rather than after, an append-only per-unit history, and a rollback that truncates that history and requeues instead of retrying on top of a bad state. This methodology specifies those four for an orchestrator you already have. The sharp edges are all in the ordering: a marker written after dispatch turns a crash into silence, a state directory created implicitly turns a typo into a phantom unit, and a missing marker read as "not started" quietly redoes finished work. Each is a real defect that has been observed, and each is closed by one rule.

**Ефективно для:**

- A queue, pool or cron orchestrator that dispatches agents and today records only `QUEUE / ACTIVE / DONE` — status, no history.
- Long multi-phase runs where a crash currently means "restart the unit" because nobody can tell how far it got.
- Anyone being told they need a durable-execution framework to get resume and time-travel replay.
- Runs with human approval gates that must survive hours or days without a process waiting on them.

## Applies If (ALL must hold)

- An orchestrator dispatches units of work to agents or subprocesses and can crash, be killed, or be rate-limited mid-run.
- A unit of work has more than one phase, and redoing a completed phase costs real money or real time.
- The orchestrator and its workers share one filesystem, or one they can both lock.

## Skip If (ANY kills it)

- Every unit is a single idempotent step — re-running it costs nothing, so a checkpoint buys nothing.
- Workers are distributed across hosts with no shared filesystem and no lock service; this specifies file-based state and `flock`, and neither survives that.
- A durable-execution engine already owns run state end to end. Two checkpoint authorities is worse than one, whichever one it is.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Six testable rules. R1 and R2 are the ordering rules that cause the observed defects; R5 separates rollback from retry. |
| `content/02-output-contract.xml` | The Checkpoint Ledger Spec: the state-directory layout, the four record fields, write boundaries, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six failure modes, four of them observed in production runs, each with the rule that prevents it. |
| `content/06-decision-tree.xml` | Routing from an observed state on disk to resume / dead-letter / roll back / do nothing. |
| `scripts/validate-on-disk-checkpoint-ledger.py` | Validates a spec: lineage ordering, marker vocabulary, boundaries, dead-letter policy. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/checkpoint-ledger-spec.yaml` | Fill-in spec; ships valid against the contract. |
| `templates/mark.sh` | The single creation path. Identity-checked, `flock`-guarded, appends to history. Exits non-zero on an unknown unit. |
| `templates/rollback.sh` | Truncate-and-requeue: removes markers at or after a phase in lineage order, records `rolled-back`, requeues. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `agent-rollback-button-design` — reverts an agent *release*. This reverts one *run* to one *phase*; the two operate on different objects and both can be needed.
- `agent-replay-harness-cookbook` — replays a captured failure deterministically for debugging. The ledger resumes a live run; the harness reproduces a dead one.
- `subagent-as-context-firewall` — what a dispatched unit is allowed to see. The ledger records that a dispatch happened; that methodology bounds what it costs.
- `idempotent-write-tools` — the property that makes a resumed phase safe to re-run. Where it cannot be achieved, R4's non-idempotent boundary is the fallback.
- `context-graph-engineering` — unrelated object, adjacent vocabulary: that is the knowledge graph, this is run state.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/checkpoint-ledger-spec.yaml`

```yaml
#
# Validate:  validate-on-disk-checkpoint-ledger.py checkpoint-ledger-spec.yaml
#
# Five fields below have exactly one permitted value. They are fields, not
# assumptions, so the guard is reviewable and the validator can enforce it.

system: "cron-driven agent pool over an on-disk task queue"

# --- Layout. One directory per unit under state_root; never in version control. ---
state_root: ".pool/states"
gitignored: true                       # must be true

# --- Identity (r1). One creation path; every other writer verifies and exits. ---
unit_id_pattern: "^[a-z0-9][a-z0-9-]{2,63}$"
enrol_command: "scripts/enrol.sh <unit>"
mark_command: "scripts/mark.sh <unit> <phase> <status> [reason]"
mark_creates_dirs: false               # must be false — this is the ghost-state guard

# --- Lineage. Ordered, earliest first. Rollback truncates "at or after" in THIS order. ---
lineage:
  - brief
  - draft
  - review
  - publish

# --- Markers (r2, r5). Exactly three states; rolled-back is a history verb. ---
marker_states: [in-flight, done, failed]
in_flight_written: before_dispatch     # must be before_dispatch

# --- History (r3). Append-only, one line per transition, under a lock. ---
history_file: "history.log"
history_line_format: "<iso_ts> <phase> <status> <commit-or-reason>"
lock: "flock on .pool/states/.lock"
record_fields: [identity, snapshot, provenance, status]

# --- Write boundaries (r4). model_call always; the others follow the flags. ---
write_boundaries:
  - model_call                         # after each expensive-to-reproduce model call
  - non_idempotent_side_effect         # after each commit / push / publish / send
  - risky_step                         # before each step with a known failure mode
  - human_gate                         # at each gate, so it can stay open for days
has_non_idempotent_side_effects: true
has_human_gate: true

# --- Recovery (r5, r6). Rollback takes a unit AND a phase. ---
rollback_command: "scripts/rollback.sh <unit> <phase> <reason>"
dead_letter_after_minutes: 180         # set against the LONGEST phase, not the average
liveness_check: "pid in the marker is checked with kill -0 before any sweep action"
auto_redispatch_on_stale: false        # must be false — dead-letter, then an operator decides

# --- Boundary (r7). A packaged tool may scaffold and unpack; it may not advance a run. ---
cli_writes_checkpoints: false          # must be false
```

### `templates/mark.sh`

```bash
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
```

### `templates/rollback.sh`

```bash
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
```
