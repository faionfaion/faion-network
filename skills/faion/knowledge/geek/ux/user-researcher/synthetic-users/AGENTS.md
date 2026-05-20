---
slug: synthetic-users
tier: geek
group: ux
domain: user-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for using AI-generated research participants to produce directional feedback during early ideation — covering persona simulation, interview analysis, and the mandatory gate of validating key findings with at least 3 real users before any product decision.
content_id: "d6f934fd273d52f5"
tags: [synthetic-research, ai-agents, user-simulation, rapid-testing]
---
# Synthetic Users

## Summary

**One-sentence:** Methodology for using AI-generated research participants to produce directional feedback during early ideation — covering persona simulation, interview analysis, and the mandatory gate of validating key findings with at least 3 real users before any product decision.

**One-paragraph:** Methodology for using AI-generated research participants to produce directional feedback during early ideation — covering persona simulation, interview analysis, and the mandatory gate of validating key findings with at least 3 real users before any product decision. Synthetic users are directional tools, never confirmatory evidence.

## Applies If (ALL must hold)

- Early ideation: generating directional feedback on concepts before recruiting real participants
- Hypothesis generation: stress-testing assumptions with AI-simulated user archetypes
- Rapid concept testing at zero research budget when timeline is days, not weeks
- Producing illustrative failure scenarios for edge-case personas (low-literacy, non-native speakers)
- Supplementing thin real-user datasets when recruitment would delay a critical decision

## Skip If (ANY kills it)

- Go/no-go product decisions — synthetic feedback is directional only, never confirmatory
- Demand forecasting or willingness-to-pay studies — AI is trained on text, not economic behavior
- Sensitive population research (healthcare, legal, financial) — bias and hallucination risk is unacceptable
- Any study output presented to investors or regulators as real user evidence
- When you already have access to real users — synthetic users do not improve on real data

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

- parent skill: `geek/ux/user-researcher/`
