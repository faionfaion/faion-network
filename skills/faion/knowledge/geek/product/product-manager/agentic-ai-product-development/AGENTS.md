---
slug: agentic-ai-product-development
tier: geek
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A product methodology for designing and shipping autonomous AI systems — agents that act toward a goal without user-triggering each step.
content_id: "724546098006c3d7"
tags: [agentic-ai, product-spec, mvi, goal-achievement, autonomous-systems]
---
# Agentic AI Product Development

## Summary

**One-sentence:** A product methodology for designing and shipping autonomous AI systems — agents that act toward a goal without user-triggering each step.

**One-paragraph:** A product methodology for designing and shipping autonomous AI systems — agents that act toward a goal without user-triggering each step. Replaces the MVP (Minimum Viable Product) frame with MVI (Minimum Viable Intelligence): scope is determined by the intelligence level the system must achieve, not by feature count. Every spec must enumerate autonomous actions explicitly, define machine-verifiable goal states, and document the human-in-the-loop model before engineering starts.

## Applies If (ALL must hold)

- Writing a product spec where the core delivery mechanism is an autonomous agent (not a user-triggered model call)
- Defining MVI scope: which capabilities are core intelligence vs deferred to v2
- Choosing success metrics for an agentic feature (goal achievement rate, escalation rate, autonomy ratio, cost-per-task)
- Documenting the human-in-the-loop model for stakeholders
- Deciding which use cases have sufficient goal clarity and data access to support autonomous action

## Skip If (ANY kills it)

- The use case is a conversational assistant or copilot — use ai-native-product-development instead
- Success criteria require a human judge ("does this feel good?") — agentic systems need machine-verifiable success conditions
- Organization lacks engineering maturity to build and monitor agentic pipelines
- Regulatory constraints require human review of every AI-generated output before it reaches users

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

- parent skill: `geek/product/product-manager/`
