---
slug: elicitation-techniques
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A deterministic technique-selector for the 10 BABOK v3 elicitation techniques (interview, workshop, focus group, observation, survey, document analysis, prototyping, brainstorming, interface analysis, collaborative game).
content_id: "d86f3492ffac9a26"
tags: [elicitation, babok, requirements, techniques, stakeholder-engagement]
---
# Elicitation Techniques

## Summary

**One-sentence:** A deterministic technique-selector for the 10 BABOK v3 elicitation techniques (interview, workshop, focus group, observation, survey, document analysis, prototyping, brainstorming, interface analysis, collaborative game).

**One-paragraph:** A deterministic technique-selector for the 10 BABOK v3 elicitation techniques (interview, workshop, focus group, observation, survey, document analysis, prototyping, brainstorming, interface analysis, collaborative game). Select a ranked mix of 1-3 techniques based on concrete situation inputs — never a single technique in isolation. Always triangulate: pair at least two techniques where the second challenges the first.

## Applies If (ALL must hold)

- Early-discovery phase: choosing a technique mix from BABOK's 10 and justifying each pick
- Training or onboarding a junior BA or LLM agent needing a deterministic decision tree
- Mixed-method project where triangulation (interview + observation + document analysis) is needed on the same workflow
- Mid-project scope renegotiation: re-elicit only the changed area with the cheapest adequate technique
- Budget/time pressure: structured selector beats ad-hoc choice when sessions must be minimized

## Skip If (ANY kills it)

- The technique is already locked by org policy (e.g., regulated industry mandates signed workshops)
- Continuous-discovery shop on a stable product (Teresa Torres cadence) — that is its own pattern
- One-stakeholder, one-sitting situation — just run the interview; selector adds overhead
- Pure UX research with users (not stakeholders) — use ux-researcher/ techniques instead
- Hackathon or spike — prototype and time-box; no BABOK ceremony needed

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

- parent skill: `pro/ba/ba-core/`
