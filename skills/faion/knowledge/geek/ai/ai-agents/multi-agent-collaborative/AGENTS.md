---
slug: multi-agent-collaborative
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Each agent in the group produces an initial contribution to the task, then iteratively reads and builds on other agents' contributions recorded in a shared workspace.
content_id: "84f26d5d55efb0ce"
tags: [multi-agent, collaborative, shared-workspace, iterative-refinement, brainstorm]
---
# Collaborative Agents with Shared Workspace

## Summary

**One-sentence:** Each agent in the group produces an initial contribution to the task, then iteratively reads and builds on other agents' contributions recorded in a shared workspace.

**One-paragraph:** Each agent in the group produces an initial contribution to the task, then iteratively reads and builds on other agents' contributions recorded in a shared workspace. After a fixed number of iterations, a coordinator (separate LLM call) synthesizes the best elements from all agent contributions into a final result.

## Applies If (ALL must hold)

- Creative or strategy work where diverse perspectives from collaborating agents add genuine value — design, narrative, technical architecture decisions.
- Problems with no single correct answer where multiple angles improve quality — brainstorming, risk identification, content ideation.
- Quality-critical outputs that benefit from agents critiquing and building on each other's work over multiple rounds.
- Tasks where the solution space is wide and convergence speed is less important than coverage.

## Skip If (ANY kills it)

- Tight latency budgets: N agents × M iterations = N×M LLM calls; without token budgets, costs spike unexpectedly.
- Tasks with a single correct answer — agents with similar training data converge on the same (possibly wrong) answer even after multiple iterations (echo chamber risk).
- Fully deterministic pipelines where sequential execution is simpler and cheaper.
- Tasks requiring fine-grained shared mutable state — the shared workspace is append-only; write conflicts in async settings cause race conditions.

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
