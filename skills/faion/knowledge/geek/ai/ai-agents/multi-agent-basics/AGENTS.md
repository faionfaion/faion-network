---
slug: multi-agent-basics
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Multi-agent systems coordinate multiple specialized AI agents to solve complex problems collaboratively.
content_id: "f9eaa8fca61aa392"
tags: [multi-agent, orchestration, coordination, specialization, collaboration]
---
# Multi-Agent Systems Basics

## Summary

**One-sentence:** Multi-agent systems coordinate multiple specialized AI agents to solve complex problems collaboratively.

**One-paragraph:** Multi-agent systems coordinate multiple specialized AI agents to solve complex problems collaboratively. By dividing tasks among experts and enabling communication, these systems can tackle challenges beyond single-agent capabilities.

## Applies If (ALL must hold)

- Complex tasks requiring diverse expertise — problems with natural role divisions (research, writing, review).
- Single agent struggles with scope — task requires more context than one conversation can hold.
- Debate and verification scenarios — adversarial review needed to catch errors a single agent would miss.
- Simulation and role-playing — multiple viewpoints or actors must be modeled.
- Building reusable agent infrastructure — will serve many different task types over time.

## Skip If (ANY kills it)

- Simple question-answering or single-step data transformation — orchestration overhead exceeds value.
- Environments without reliable message persistence — agents lose context on failure.
- When role definitions cannot be made non-overlapping — overlapping roles produce conflicting outputs.
- Proof-of-concept stages — debugging a multi-agent system is harder than building it.

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
