---
slug: headless-cli-four-guards
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every non-interactive run of an agent CLI (Claude Code, OpenAI Codex, Aider, opencode) MUST set four guards: (1) print/headless flag to disable the TUI, (2) explicit allowedTools allowlist (NEVER --dangerously-skip-permissions in prod), (3) --max-turns cap, (4) closed stdin via < /dev/null so the agent cannot block waiting on user input.
content_id: "11b9c78c3043d2ba"
tags: [headless, agents, ci, production, safety]
---
# Headless CLI — Four Guards Against Mystery Hangs

## Summary

**One-sentence:** Every non-interactive run of an agent CLI (Claude Code, OpenAI Codex, Aider, opencode) MUST set four guards: (1) print/headless flag to disable the TUI, (2) explicit allowedTools allowlist (NEVER --dangerously-skip-permissions in prod), (3) --max-turns cap, (4) closed stdin via < /dev/null so the agent cannot block waiting on user input.

**One-paragraph:** Every non-interactive run of an agent CLI (Claude Code, OpenAI Codex, Aider, opencode) MUST set four guards: (1) print/headless flag to disable the TUI, (2) explicit allowedTools allowlist (NEVER --dangerously-skip-permissions in prod), (3) --max-turns cap, (4) closed stdin via < /dev/null so the agent cannot block waiting on user input. Missing any one of the four turns into a mystery hang or runaway-loop incident in production.

## Applies If (ALL must hold)

- ANY cron/CI/GitHub Actions/queue/scheduled-agent invocation of claude, codex, aider, or opencode.
- Multi-agent pipelines where one agent shells out to another.
- Background pool subagents (e.g. /faion, claude --print workers).
- Self-healing scripts that run unattended on a server.

## Skip If (ANY kills it)

- Interactive developer sessions — the TUI and prompt-on-demand UX are the whole point; no guards required.
- One-shot smoke tests where the operator is watching the terminal and will Ctrl-C on a hang.
- Local prototyping where you actively want the model to stop and ask.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
