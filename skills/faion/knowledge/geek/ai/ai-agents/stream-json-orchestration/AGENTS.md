---
slug: stream-json-orchestration
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When wrapping an agent CLI (Claude Code, Codex, Aider, opencode) as a subprocess inside a larger orchestrator, use the stream-json output format so the orchestrator can react MID-RUN — apply budget caps, hand off to another agent, chain conditional steps, kill on safety violations — instead of waiting for final output.
content_id: "84a4b69e7d28fa9e"
tags: [stream-json, orchestration, cli, subprocess, safety]
---
# Stream-JSON Orchestration

## Summary

**One-sentence:** When wrapping an agent CLI (Claude Code, Codex, Aider, opencode) as a subprocess inside a larger orchestrator, use the stream-json output format so the orchestrator can react MID-RUN — apply budget caps, hand off to another agent, chain conditional steps, kill on safety violations — instead of waiting for final output.

**One-paragraph:** When wrapping an agent CLI (Claude Code, Codex, Aider, opencode) as a subprocess inside a larger orchestrator, use the stream-json output format so the orchestrator can react MID-RUN — apply budget caps, hand off to another agent, chain conditional steps, kill on safety violations — instead of waiting for final output. A line-delimited JSON stream is the load-bearing format for CLI-as-subprocess orchestration. Each event (model_message, tool_use, tool_result, status) arrives as a JSON object on stdout the moment it happens. The orchestrator parses each line as-it-lands.

## Applies If (ALL must hold)

- Orchestrator spawns Claude Code or Codex CLI as a subprocess (most common 2026 pattern).
- Long-running agent tasks (greater than 30 sec) where you want feedback.
- Multi-step pipelines where step N+1 depends on signals from step N's progress.
- Production agents where you want telemetry per event.
- Safety/policy enforcement that must intervene mid-run.

## Skip If (ANY kills it)

- One-shot, short tasks (less than 5 sec) — overhead of parsing is not worth it.
- When the SDK is available and gives you the same hooks more cleanly (use SDK directly).
- When you are piping stdout to a human user — pretty-print mode is more readable for direct interaction.

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
