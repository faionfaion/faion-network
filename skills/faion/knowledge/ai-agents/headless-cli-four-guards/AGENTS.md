# Headless CLI — Four Guards Against Mystery Hangs

## Summary

**One-sentence:** Requires every non-interactive agent-CLI invocation (Claude Code, Codex, Aider, opencode) to set four guards — headless flag, explicit allowedTools, --max-turns cap, and `< /dev/null` stdin — eliminating the four documented production failure modes (TUI hang, permission stall, runaway loop, garbage stdin).

**One-paragraph:** Every non-interactive run of an agent CLI MUST set four guards: (1) print/headless flag to disable the TUI, (2) explicit `--allowedTools` allowlist (NEVER `--dangerously-skip-permissions` in prod), (3) `--max-turns` cap tied to a real workflow length, (4) closed stdin via `< /dev/null` so the agent cannot block waiting on user input. Missing any one turns into a mystery hang or runaway-loop incident.

**Ефективно для:** будь-якого cron / CI / черги / scheduled-agent виклику CLI-агента — там, де немає TTY і немає людини, щоб натиснути "Ctrl-C".

## Applies If (ALL must hold)

- ANY cron/CI/GitHub Actions/queue/scheduled-agent invocation of claude, codex, aider, or opencode.
- Multi-agent pipelines where one agent shells out to another.
- Background pool subagents.
- Self-healing scripts running unattended on a server.

## Skip If (ANY kills it)

- Interactive developer sessions — TUI is the point.
- One-shot smoke tests where the operator watches the terminal.
- Local prototyping where the agent should pause to ask.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task prompt | String passed as positional arg | Caller |
| Allowlist | Comma-separated `Tool` or `Bash(prog:*)` patterns | Engineering review |
| Turn cap | Integer tied to workflow length | Workflow author |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `idempotent-write-tools` | Headless agents that mutate state need idempotency keys for safe retry. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: all-four-required, no-dangerously-skip, cap-tied-to-workflow, per-CLI mapping, lint-in-CI | ~1000 |
| `content/02-output-contract.xml` | essential | The four-guard invocation pattern and per-CLI flag table | ~900 |
| `content/03-failure-modes.xml` | essential | Each missing guard → its documented failure mode | ~900 |
| `content/06-decision-tree.xml` | essential | Per-CLI mapping for the four guards | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate guarded invocation for a new script | haiku | Mechanical template fill |
| Audit existing cron scripts | sonnet | Pattern detection across many files |
| Design narrow allowlist for new workflow | sonnet | Requires understanding of needed tools |

## Templates

| File | Purpose |
|------|---------|
| `templates/headless-guards.sh` | Reusable guarded invocation wrapper for Claude Code, Codex, Aider, opencode |
| `templates/_smoke-test.sh` | Minimum invocation for self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-headless-cli-four-guards.py` | Lints a shell script for missing guards | Pre-commit on any cron/CI script that calls an agent CLI |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[idempotent-write-tools]]
- [[generator-critic-bounded-loop]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the invocation runs in an interactive TTY. If not, the tree enforces all four guards and maps them to the correct flag per CLI (Claude Code uses `-p`, Codex uses `codex exec`, etc.).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/headless-guards.sh`

```bash
# headless-guards.sh — apply the four guards for Claude Code, Codex, Aider, opencode.
#
# Usage:
#   ./headless-guards.sh <claude|codex|aider|opencode> "<task>" [allowlist]
#
# Each branch sets: print/headless flag, allowlist (where supported),
# max-turns (or wall-clock timeout when no native cap), and closes stdin.

set -euo pipefail

TOOL="${1:?tool name required}"
TASK="${2:?task required}"
ALLOWED="${3:-Read,Edit,Bash(pytest:*)}"
MAX_TURNS="${MAX_TURNS:-20}"
WALL="${WALL:-600}"

case "$TOOL" in
  claude)
    timeout "$WALL" claude -p "$TASK" \
      --output-format stream-json --verbose \
      --allowedTools "$ALLOWED" \
      --max-turns "$MAX_TURNS" \
      < /dev/null
    ;;
  codex)
    timeout "$WALL" codex exec --sandbox workspace-write "$TASK" \
      < /dev/null
    ;;
  aider)
    timeout "$WALL" aider --yes --no-auto-test \
      --max-chat-history-tokens 8000 \
      --message "$TASK" \
      < /dev/null
    ;;
  opencode)
    timeout "$WALL" opencode --headless --max-turns "$MAX_TURNS" "$TASK" \
      < /dev/null
    ;;
  *)
    echo "unknown tool: $TOOL" >&2
    exit 2
    ;;
esac
```

### `templates/_smoke-test.sh`

```bash
set -euo pipefail
TASK="smoke task"
claude -p "$TASK" \
  --allowedTools "Read,Edit,Bash(pytest:*)" \
  --max-turns 20 \
  < /dev/null
```
