---
slug: handoff-id-payload
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When agent A hands off to agent B in a multi-agent topology, the handoff payload is a structured `{task_id, target_agent, decision_metadata}` object — never the conversation history, never the raw input.
content_id: "d2bfcdbff456b2a4"
tags: [agents, multi-agent, handoffs, routing, context-management]
---
# Handoff Payload — ID + Minimal Metadata

## Summary

**One-sentence:** When agent A hands off to agent B in a multi-agent topology, the handoff payload is a structured `{task_id, target_agent, decision_metadata}` object — never the conversation history, never the raw input.

**One-paragraph:** When agent A hands off to agent B in a multi-agent topology, the handoff payload is a structured `{task_id, target_agent, decision_metadata}` object — never the conversation history, never the raw input. Agent B reads the actual task state from a shared store (file, queue, DB) keyed by `task_id`. The supervising router returns `SupervisorDecision` objects, not message threads. Each agent's context is sized to its job, not to the cumulative conversation.

## Applies If (ALL must hold)

- Multi-agent meshes with role-specialized agents (researcher → writer → editor; classifier → worker).
- Supervisor/worker topologies where the supervisor's only job is routing.
- Long pipelines where each step's relevant context is a small subset of cumulative state.
- Cron-triggered or event-driven agents where the trigger has no conversation to pass on.

## Skip If (ANY kills it)

- Single-agent loops — the "handoff" is a no-op; adding a store is pure overhead.
- Tightly-coupled co-reasoning where two agents must see each other's intermediate thoughts (use a fork/shared context instead).
- Throwaway prototypes where setting up a task store is more work than the agent itself.

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
