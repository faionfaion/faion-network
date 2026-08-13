# Pair Programming

## Summary

**One-sentence:** Plans a pair session: picks style (driver-navigator / ping-pong / strong-style), sets 15-30 min role swap, defines agent's optional third role.

**One-paragraph:** Two developers sharing a workstation accelerate knowledge transfer and reduce bus-factor — but only with discipline: role swap interval, named style, single shared workstation (or shared cursor). This methodology emits a session plan: style choice, swap interval, agent role (test-writer / hint-provider / silent), retrospective metric (commit hygiene, defects-found). Output is the plan and post-session report.

**Ефективно для:**

- Onboarding: новачок як navigator, senior як driver — pace матерію за дні замість тижнів.
- Tricky algorithm / debug: дві голови ловлять помилки, які одна пропускає.
- Ping-pong TDD: один пише тест, інший — реалізацію — деталі балансом.
- Solo + agent: people-cost мінімальний; агент як silent navigator з пропозиціями.

## Applies If (ALL must hold)

- Two engineers available for ≥60 min focused work.
- Topic merits more than one viewpoint (debug / design / TDD).
- Workstation supports shared editing (Live Share / Tuple / shared screen).

## Skip If (ANY kills it)

- Pure clerical task (bumping deps).
- Async teams — pair needs synchronous time.
- One participant is mentally checked-out — pair without engagement is wasted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Topic | Markdown | session brief |
| Both participants | list of 2 | calendar |
| Style choice | enum | decision tree below |
| Agent role (optional) | enum | session policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: swap-interval, named-style, shared-workstation, agent-silent-by-default, retro-required | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for session plan + retro | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: silent-passenger, agent-spam, no-retro | 600 |
| `content/04-procedure.xml` | essential | 5-step pair-session procedure | 700 |
| `content/06-decision-tree.xml` | essential | Topic + style routing tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan_session` | haiku | Template-fill; deterministic. |
| `agent_during_session` | sonnet | Silent-by-default; reactive only. |
| `draft_retro` | sonnet | Synthesises metrics + lessons. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pingpong-prompt.txt` | Agent prompt for ping-pong TDD style |
| `templates/strong-style-prompt.txt` | Agent prompt for strong-style enforcement |
| `templates/pair-journal.sh` | Shell that logs swap timestamps + commit moments |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- - [[mob-programming]] — 3-4 person variant of the same family.
- - [[code-review]] — pair-produced PR still goes through review.

## Decision tree

See `content/06-decision-tree.xml`. Branches on topic shape: TDD-shaped → ping-pong; debug-shaped → driver-navigator; teaching-shaped → strong-style. Leaves reference rules from 01-core-rules.xml.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pingpong-prompt.txt`

```text
TDD ping-pong pairing. Turn order tracked in .pair-journal.md.

RULES:
- I write a failing test → you make it pass → you write the next failing test → I make it pass. Repeat.
- On your "make-it-pass" turn: Edit production code only. Never edit test files on this turn.
- On your "write-test" turn: Write one failing test only. Never edit production code on this turn.
- Write the simplest code that makes the test pass; refactor in a separate commit labeled "refactor:".
- After each green, commit: "test: <description>" for test turns, "feat: <description>" for pass turns.
- If you detect a turn violation, stop and report it before proceeding.

Start by reading {{TEST_FILE}}. Signal "YOUR TURN" when it is my turn.
```

### `templates/strong-style-prompt.txt`

```text
We are pairing in strong-style: I drive, you navigate.

HARD CONSTRAINTS:
- You may NOT use Edit, Write, or Bash tools. Output only English instructions or
  code snippets of at most 6 lines that I will type myself.
- Before any code, state your intent in one sentence.
- Ask me to confirm understanding when introducing a new concept.
- After every 25-minute block, suggest a 5-minute break and ask whether to switch styles.
- If I ask you a direct question, answer it; do not redirect to typing instructions.

Session goal: {{GOAL}}
Current file: {{FILE_PATH}}
```

### `templates/pair-journal.sh`

```bash
#!/usr/bin/env bash
# pair-journal.sh — log pair session events with timestamps.
# Survives agent compaction; re-read at session start to restore context.
# Usage:
#   pair-journal.sh start "Implement payment retry logic"
#   pair-journal.sh switch "driver=claude navigator=human"
#   pair-journal.sh note "Decided to use exponential backoff"
#   pair-journal.sh end
set -euo pipefail

JOURNAL="${PAIR_JOURNAL:-.pair-journal.md}"
EVENT="${1:?event required: start|switch|note|end}"
shift || true
MSG="${*:-}"
TS=$(date -u +%FT%TZ)

case "$EVENT" in
  start)
    echo "" >> "$JOURNAL"
    echo "## Session $(date -u +%F)" >> "$JOURNAL"
    echo "- $TS start goal=\"$MSG\"" >> "$JOURNAL"
    ;;
  switch|note)
    echo "- $TS $EVENT $MSG" >> "$JOURNAL"
    ;;
  end)
    echo "- $TS end" >> "$JOURNAL"
    git add "$JOURNAL" && git commit -m "chore: pair session $(date +%F)" || true
    ;;
  *)
    echo "Unknown event: $EVENT" >&2; exit 1
    ;;
esac
```
