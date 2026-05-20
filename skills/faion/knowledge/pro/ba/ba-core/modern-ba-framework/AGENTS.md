---
slug: modern-ba-framework
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Select one primary BA reference framework (BABOK v3, BA Standard 2025, IREB CPRE, PMI-PBA, BCS Diploma, SAFe BA, Agile Extension to BABOK v2, SWEBOK v4) for an engagement before producing any artifact.
content_id: "2eca489bf32c2da9"
tags: [ba-framework, babok, requirements, selection, governance]
---
# Modern BA Framework

## Summary

**One-sentence:** Select one primary BA reference framework (BABOK v3, BA Standard 2025, IREB CPRE, PMI-PBA, BCS Diploma, SAFe BA, Agile Extension to BABOK v2, SWEBOK v4) for an engagement before producing any artifact.

**One-paragraph:** Select one primary BA reference framework (BABOK v3, BA Standard 2025, IREB CPRE, PMI-PBA, BCS Diploma, SAFe BA, Agile Extension to BABOK v2, SWEBOK v4) for an engagement before producing any artifact. Score candidates on regulatory fit, team maturity, vocabulary overlap, tooling support, and agile friendliness. Persist the decision as ba-framework-decision.md with a vocabulary glossary. This selection is upstream of all routing decisions — pick the rulebook before picking the plays.

## Applies If (ALL must hold)

- Onboarding a BA or agent into an unfamiliar org where the "BA standard" is unclear or contested
- Procurement or RFP responses naming a specific standard — deliverable vocabulary must match exactly
- Regulated industries (pharma GxP, banking BCBS 239, automotive ASPICE) where requirements artifacts are auditable
- Multi-vendor programs where each vendor uses a different BA dialect — normalize to one canonical vocabulary
- Hybrid agile/waterfall portfolios requiring a documented bridge between BABOK and Scrum/SAFe ceremonies
- Building an internal BA competency matrix or training curriculum anchored to a published syllabus

## Skip If (ANY kills it)

- Team already has a working BA practice with a known reference — re-selection is rework theatre
- Solo founder or 1-2 person product — continuous discovery + plain user stories beats any framework overhead
- Pure UX or growth work — use ux-researcher and conversion-optimizer methodologies
- One-shot tactical analysis (single ticket clarification) — overhead not justified
- Org explicitly anti-IIBA — pick Agile Extension or skip to product-discovery methodologies

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
