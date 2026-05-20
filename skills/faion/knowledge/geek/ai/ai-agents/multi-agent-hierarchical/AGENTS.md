---
slug: multi-agent-hierarchical
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A manager agent receives a top-level task, creates a JSON assignment plan by querying available workers and their roles, dispatches each subtask to the matching worker, and finally synthesizes all worker results into one response.
content_id: "d5efbc70529c8033"
tags: [multi-agent, hierarchical, orchestration, delegation, task-decomposition]
---
# Hierarchical Manager-Worker Multi-Agent Pattern

## Summary

**One-sentence:** A manager agent receives a top-level task, creates a JSON assignment plan by querying available workers and their roles, dispatches each subtask to the matching worker, and finally synthesizes all worker results into one response.

**One-paragraph:** A manager agent receives a top-level task, creates a JSON assignment plan by querying available workers and their roles, dispatches each subtask to the matching worker, and finally synthesizes all worker results into one response. Workers are stateless specialists; only the manager holds the overall task context.

## Applies If (ALL must hold)

- Complex project work where different agents have genuinely different roles (researcher, coder, reviewer) — role overlap must be minimal.
- Tasks that decompose into sequential but dependent subtasks: each worker's output feeds the synthesis step.
- Production systems requiring auditability: hierarchical delegation produces a traceable assignment log.
- When the top-level task scope exceeds a single context window but can be partitioned clearly.

## Skip If (ANY kills it)

- Simple tasks that fit in a single context window — manager overhead (plan call + synthesis call) adds cost without value.
- When agent roles overlap significantly — workers with redundant roles echo each other rather than contribute.
- Tight latency budgets: hierarchical delegation adds at minimum 2 extra LLM round-trips (plan + synthesis) on top of worker calls.
- Tasks requiring fine-grained shared mutable state between workers — pass-by-message is the only inter-agent channel.

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
