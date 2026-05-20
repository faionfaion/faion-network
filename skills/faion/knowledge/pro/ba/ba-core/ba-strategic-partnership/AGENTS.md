---
slug: ba-strategic-partnership
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A per-artifact stance reviewer that scores requirements documents on six axes (problem_clarity, outcome_orientation, evidence_grounding, enterprise_scope, partner_voice, kill_criterion) and rewrites order-taker language as outcome statements tied to a named OKR.
content_id: "3b8b89b4a3c30f9b"
tags: [ba, strategic-partnership, stance-review, requirements, outcome-focus]
---
# BA Strategic Partnership

## Summary

**One-sentence:** A per-artifact stance reviewer that scores requirements documents on six axes (problem_clarity, outcome_orientation, evidence_grounding, enterprise_scope, partner_voice, kill_criterion) and rewrites order-taker language as outcome statements tied to a named OKR.

**One-paragraph:** A per-artifact stance reviewer that scores requirements documents on six axes (problem_clarity, outcome_orientation, evidence_grounding, enterprise_scope, partner_voice, kill_criterion) and rewrites order-taker language as outcome statements tied to a named OKR. Auto-blocks any artifact where any axis scores below 2 or kill_criterion scores below 1. This is a per-engagement behavior pattern — run it at intake and at spec-review gates, not as a quarterly portfolio loop.

## Applies If (ALL must hold)

- Intake of a new requirement or "can you just add X" request — reframe as outcome before scope is locked.
- Re-reading an existing requirements doc, user story, or PRD to detect order-taker language.
- Onboarding a junior BA: run the stance rubric on their last 5 artifacts and produce coaching deltas.
- Pre-meeting framing for stakeholder calls: draft 3 strategic questions to ask before accepting the stated requirement.
- Spec review gate before a ticket goes to engineering — block if no problem statement, no outcome metric, no kill criterion.

## Skip If (ANY kills it)

- Quarterly portfolio-level opportunity mining — use the sibling `business-analyst/ba-strategic-partnership/`.
- Modeling work (BPMN, use-case decomposition, traceability matrices) — wrong tool.
- Live stakeholder dialogue — agent prepares, never speaks for the BA.
- Trivial maintenance tickets (copy edits, dependency bumps) — overhead not justified.

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
