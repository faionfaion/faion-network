---
slug: multi-agent-design-patterns
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Eight essential design patterns enable orchestration of multi-agent systems in enterprise workflows.
content_id: "327445e5c4bf55f6"
tags: [design-patterns, orchestration, enterprise, workflows, adk]
---
# Multi-Agent Design Patterns

## Summary

**One-sentence:** Eight essential design patterns enable orchestration of multi-agent systems in enterprise workflows.

**One-paragraph:** Eight essential design patterns enable orchestration of multi-agent systems in enterprise workflows. These patterns — Sequential Pipeline, Parallel Fan-Out/Gather, Hierarchical Decomposition, Generator-Critic, Loop Pattern, Human-in-the-Loop, Router Pattern, and Blackboard Pattern — provide reusable solutions for different coordination and quality requirements.

## Applies If (ALL must hold)

- Enterprise workflow automation where no single agent has all required expertise — use Hierarchical Decomposition.
- Content or code quality checks that must catch every error, not just obvious ones — use Generator-Critic.
- Multi-dimensional analysis tasks where independent perspectives reduce blind spots — use Parallel Fan-Out/Gather.
- Long-horizon tasks that require iterative refinement with feedback loops — use Loop Pattern.
- Workflows requiring human sign-off before irreversible steps — use Human-in-the-Loop.
- Dynamic routing across multiple knowledge domains based on query content — use Router Pattern.
- Knowledge synthesis tasks where agents share a common workspace — use Blackboard Pattern.

## Skip If (ANY kills it)

- Simple retrieval or single-step generation — pattern overhead adds cost with no quality gain.
- Latency-critical paths where multiple sequential agent calls are unacceptable.
- Tasks without clear decomposition axes — forcing patterns onto unstructured tasks creates artificial fragmentation.
- Early prototyping phases where debugging orchestration complexity is not yet warranted.
- Single-domain problems where one specialized agent is sufficient.

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
