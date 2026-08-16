# Claude Code Headless As Default Agent Runtime

## Summary

**One-sentence:** For coding / devops / research tasks the first implementation is `claude -p` headless invocation — not a custom Agent SDK loop. The CLI already ships filesystem, bash, git, MCP, plan mode, sub-agents, hooks, compaction; drop down to the SDK only on documented switch-triggers.

**One-paragraph:** Teams reflexively reach for the Claude Agent SDK to build an autonomous agent and re-implement what the CLI already gives them — and ship a fragile version. This methodology produces a per-task decision record: default to `claude -p` with `--allowedTools`, `--max-turns`, `--output-format stream-json --verbose`; allow custom SDK loop ONLY on one of four switch-triggers (non-coding domain, custom tools beyond MCP, programmatic inner-loop control, SaaS embed that cannot shell out).

**Ефективно для:** Команд, які за тиждень намагаються повторити Claude Code SDK і отримують гірший продукт; одна сторінка decision record економить тиждень розробки і дає більш надійний agent.

## Applies If (ALL must hold)

- Task is coding, devops, research, or content authoring on a machine with shell.
- Claude Code CLI is installable (Anthropic API credentials available).
- The orchestrator can parse stream-json events.
- Task is not embedded inside a SaaS product that cannot shell out.
- A named eng owner can review the decision record.

## Skip If (ANY kills it)

- Task is non-coding domain with no shell affinity (pure structured-output extraction at scale).
- Custom tools required beyond MCP coverage.
- Inner-loop programmatic control needed (e.g. step-by-step state in a graph).
- SaaS product cannot shell out (regulatory / sandbox constraint).

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Task brief | natural language | Operator |
| Tool requirements list | inventory | Tech lead |
| Allowed-tools policy | enum list | Sec/Ops |
| Iteration budget | int (max_turns) | Tech lead |
| Named owner | handle | Eng |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/headless-cli-four-guards/AGENTS.md` | Four CLI guards (-p, --allowedTools, --max-turns, stream-json). |
| `geek/ai/ai-agents/stream-json-orchestration/AGENTS.md` | Event-by-event orchestration pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: CLI default, four guards, switch-triggers, log line-by-line | ~800 |
| `content/01-cli-vs-sdk-decision.xml` | essential | Companion narrative for the switch-triggers | ~400 |
| `content/02-output-contract.xml` | essential | JSON Schema for the CLI-vs-SDK decision record | ~700 |
| `content/02-invocation-shape.xml` | essential | Canonical argv shape for `claude -p` headless | ~400 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: coding-ish? → tools fit MCP? → shell ok? → CLI/SDK | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task_for_cli_fit` | haiku | Mechanical. |
| `compose_decision_record` | sonnet | Per-instance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the decision record. |
| `templates/output.example.json` | Filled example. |
| `templates/run-headless.sh` | Shell wrapper showing the canonical argv. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the decision record. | Before kickoff. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[headless-cli-four-guards]], [[stream-json-orchestration]].

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is the task coding/devops/research with shell affinity? (2) do tool requirements fit MCP catalogue? (3) is shell-out permitted? (4) is inner-loop control required? Leaves point to "use claude-code-headless" or "drop to SDK with named trigger".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/claude-code-headless-default/output.json",
  "title": "Claude Code Headless Default Output",
  "description": "purpose=schema; consumes=brief+context; produces=artefact; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "version",
    "version_stamp",
    "produced_at",
    "rationale",
    "inputs_used"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "version_stamp": {
      "type": "string"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "fields": {
      "type": "object"
    },
    "rationale": {
      "type": "string",
      "minLength": 20
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  }
}
```

### `templates/output.example.json`

```json
{
  "artefact_id": "claude-code-headless-default-example-001",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "version_stamp": "claude-code-headless-default@1.0.0",
  "produced_at": "2026-05-22T12:00:00Z",
  "fields": {
    "placeholder_field": "filled-by-author"
  },
  "rationale": "Example output for Claude Code Headless Default; references at least one named input.",
  "inputs_used": [
    "docs/brief.md"
  ]
}
```

### `templates/run-headless.sh`

```bash
# run-headless.sh — canonical headless `claude -p` wrapper.
#
# Usage:
#   ./run-headless.sh "<task prompt>" [allowlist] [max_turns]
#
# Defaults:
#   allowlist  = "Read,Edit,Bash(pytest:*),Bash(git:status)"
#   max_turns  = 20
#
# Stdout: stream-json events, one per line.
# Exit:   non-zero if claude returns non-zero or wall-clock timeout fires.

set -euo pipefail

TASK="${1:?task prompt required}"
ALLOWED="${2:-Read,Edit,Bash(pytest:*),Bash(git:status)}"
MAX_TURNS="${3:-20}"
WALL_TIMEOUT="${WALL_TIMEOUT:-600}"

exec timeout "$WALL_TIMEOUT" \
  claude -p "$TASK" \
    --output-format stream-json --verbose \
    --allowedTools "$ALLOWED" \
    --max-turns "$MAX_TURNS" \
    < /dev/null
```
