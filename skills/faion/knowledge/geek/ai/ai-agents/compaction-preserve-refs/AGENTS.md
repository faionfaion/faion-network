---
slug: compaction-preserve-refs
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When a long-running agent must compact its conversation to free context, the compaction prompt must hard-code which fields survive and which are dropped.
content_id: "1e7792d5cd912e76"
tags: [context-window, compaction, agents, state-management, schemas]
---
# Compaction Templates That Preserve References

## Summary

**One-sentence:** When a long-running agent must compact its conversation to free context, the compaction prompt must hard-code which fields survive and which are dropped.

**One-paragraph:** When a long-running agent must compact its conversation to free context, the compaction prompt must hard-code which fields survive and which are dropped. Always preserve: file paths, function names, error messages, decisions, URLs, IDs. Always drop: intermediate reasoning chains and verbatim tool output. The compacted summary is itself a manifest of references — not a narrative — so the agent can re-fetch any dropped detail by path or ID instead of re-reasoning from scratch.

## Applies If (ALL must hold)

- Any agent loop expected to exceed approximately 30 turns or its context window — compaction will trigger.
- Multi-session SDD work where the next session reads the compacted output and resumes.
- Pipelines where compaction is automated by middleware (opencode, Claude Code auto-compaction).
- Whenever the agent depends on file paths, error texts, or external IDs to make progress.

## Skip If (ANY kills it)

- Stateless single-turn agents — there is no later step that needs the references.
- Conversations that compact only the user-facing answer for display, not for the agent's own continuation.
- Agents whose only "state" is a closed-form result (a number, a yes/no) — references add noise.

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
