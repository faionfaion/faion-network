---
slug: agentic-ai-product-development
tier: geek
group: product
domain: product-operations
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for designing autonomous agentic AI systems in products where the core value proposition is autonomous action (auto-triage, auto-scheduling, auto-publishing).
content_id: "724546098006c3d7"
tags: [agentic-ai, autonomous-systems, human-in-loop, goal-achievement, mvi-scope]
---
# Agentic AI Product Development

## Summary

**One-sentence:** Methodology for designing autonomous agentic AI systems in products where the core value proposition is autonomous action (auto-triage, auto-scheduling, auto-publishing).

**One-paragraph:** Methodology for designing autonomous agentic AI systems in products where the core value proposition is autonomous action (auto-triage, auto-scheduling, auto-publishing). Covers goal state definition, autonomous action enumeration, human-in-the-loop checkpoints, escalation design, and production monitoring. Emphasizes Minimum Viable Intelligence (MVI) scope over MVP and tracks goal achievement rate and autonomy ratio.

## Applies If (ALL must hold)

- Designing a new product feature where the core value proposition is autonomous action (e.g., auto-triage, auto-scheduling, auto-publishing)
- Shifting an existing reactive AI feature (user submits → model responds) to a proactive agentic one (agent monitors → acts without prompt)
- Defining acceptance criteria for agentic products: goal achievement rate, escalation rate, autonomy ratio
- Evaluating whether a candidate product use case justifies the cost and risk of agentic autonomy vs. a simpler assistant pattern
- Planning the human-in-the-loop model: which decisions the agent makes autonomously, which require human approval, and what triggers escalation
- Creating MVI (Minimum Viable Intelligence) scope instead of MVP when the product's core is an AI capability

## Skip If (ANY kills it)

- Building a simple AI-augmented tool where the user always initiates and reviews each step — use the standard AI-native product development pattern instead
- Agentic autonomy has no clear success metric — if you cannot define "did the agent achieve the goal?", do not build agentic
- Regulatory environment prohibits autonomous action (e.g., healthcare diagnosis, financial order execution without human approval) — use assistant pattern with mandatory human confirmation
- Team lacks observability infrastructure: without agent tracing, monitoring, and logging, production incidents are undebuggable
- Cost model does not support inference-heavy loops — agentic systems that call multiple models per task can cost 10–50x more than single-call AI features

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

- parent skill: `geek/product/product-operations/`
