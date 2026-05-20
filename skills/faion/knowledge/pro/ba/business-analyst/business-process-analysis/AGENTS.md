---
slug: business-process-analysis
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A five-stage methodology for documenting how work actually flows through an organization (current state), classifying each step as value-adding, business-necessary, or non-value-adding, and designing a measurable future state.
content_id: "aeace75b0feeb5c3"
tags: [business-process, bpa, process-improvement, enterprise, governance]
---
# Business Process Analysis - Enterprise Scale and Governance

## Summary

**One-sentence:** A five-stage methodology for documenting how work actually flows through an organization (current state), classifying each step as value-adding, business-necessary, or non-value-adding, and designing a measurable future state.

**One-paragraph:** A five-stage methodology for documenting how work actually flows through an organization (current state), classifying each step as value-adding, business-necessary, or non-value-adding, and designing a measurable future state. At enterprise scale (M&A, ERP rollout, digital transformation), a portfolio agent maintains the process inventory while per-process agents apply the 5-stage loop against APQC PCF or SCOR reference frameworks.

## Applies If (ALL must hold)

- M&A integration requiring a Day-1/Day-100/target-state process comparison across two organizations' inventories.
- ERP/CRM/HCM rollout (SAP S/4HANA, Oracle Fusion, Workday) - gap-fit analysis against vendor reference processes.
- Digital transformation programme: 100-500 processes scored on maturity, automation readiness, and customer impact.
- Pre-IPO/pre-acquisition due diligence (SOX 404, ISO 9001) requiring auditor-grade process narratives with control points.
- Shared-services/GBS design consolidating multiple business units into one process model.

## Skip If (ANY kills it)

- Single-team local workflow - use the ba-modeling/business-process-analysis variant; enterprise governance overhead is unjustified.
- Greenfield startup with no installed process estate - jump to use-case-modeling or user-story-mapping.
- Pure customer-experience redesign - use customer-journey-mapping; BPA is a downstream consequence.
- Single broken process instance requiring root-cause analysis - use 5-whys/fishbone instead.

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
