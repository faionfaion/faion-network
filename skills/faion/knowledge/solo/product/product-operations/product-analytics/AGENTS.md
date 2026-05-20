---
slug: product-analytics
tier: solo
group: product
domain: product-operations
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Framework for measuring user behavior to drive product decisions.
content_id: "9f27252d25e50bd4"
tags: [product-analytics, metrics, tracking-plan, dashboards, instrumentation]
---
# Product Analytics

## Summary

**One-sentence:** Framework for measuring user behavior to drive product decisions.

**One-paragraph:** Framework for measuring user behavior to drive product decisions. Defines the questions analytics must answer before any tracking call, designs minimal tracking plans with max 12 events per feature using Object-Action naming, implements dashboards per audience, and establishes review rituals. Connects raw event data to actionable insights without tracking everything.

## Applies If (ALL must hold)

- Designing tracking plan for a new product or feature pre-launch.
- Auditing existing event taxonomy: detect duplicates, naming inconsistencies, undocumented properties.
- Generating SQL/cohort queries from natural-language questions.
- Weekly anomaly summaries from PostHog/Amplitude/Mixpanel exports.
- Stitching multiple analytics sources into one cohort view.

## Skip If (ANY kills it)

- Real-time alerting/SLO monitoring — use Prometheus/Grafana, not LLMs.
- Compliance-bound metrics (HIPAA, GDPR-deletion, SOX revenue) — agent-generated SQL needs lawyer-grade audit trail.
- High-volume operational dashboards — LLM-in-loop adds latency, breaks "glance" rituals.
- No user analytics instrumented yet — install before agentizing.

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

- parent skill: `solo/product/product-operations/`
