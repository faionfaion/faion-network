---
slug: data-driven-requirements
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An evidence-based approach to requirements definition that replaces opinion-driven prioritization with data analytics.
content_id: "b45eb25f7aa0f50e"
tags: [requirements, data-driven, prioritization, analytics, success-metrics]
---
# Data-Driven Requirements Engineering

## Summary

**One-sentence:** An evidence-based approach to requirements definition that replaces opinion-driven prioritization with data analytics.

**One-paragraph:** An evidence-based approach to requirements definition that replaces opinion-driven prioritization with data analytics. Each requirement is anchored to a business question, quantified baseline metrics, and a measurable success target. Prioritization uses usage data, performance data, business metrics, and customer feedback rather than stakeholder seniority or gut feel.

## Applies If (ALL must hold)

- Prioritizing a backlog where features compete for limited capacity and ROI data is available.
- Feature validation before investment when analytics (usage, conversion, error rate) can answer the business question.
- Post-MVP iteration where product analytics reveal which flows users actually take.
- A/B test design where the requirement specifies what hypothesis is being tested and what outcome declares success.
- AI/ML feature scoping where business impact measurement (cycle time, CSAT, error rate) must be defined before model training.

## Skip If (ANY kills it)

- Greenfield products with no users and no baseline — hypothesis-driven development (Lean Startup) applies before data exists.
- Requirements driven by compliance or legal obligation where the mandate, not ROI, is the reason to build.
- One-off internal tooling with a known, small user group where analytics instrumentation cost exceeds value.
- When the organization has no analytics tooling and instrumenting is out of scope — gather qualitative evidence instead.

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

- parent skill: `pro/ba/business-analyst/`
