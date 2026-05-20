---
slug: solution-assessment
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured evaluation of a solution's ability to meet business need and deliver expected value, covering four assessment types and producing a recommendation at 30/60/90 days post-deployment.
content_id: "5f84aa75055f6434"
tags: [solution-evaluation, business-value, post-implementation, assessment, metrics]
---
# Solution Assessment

## Summary

**One-sentence:** A structured evaluation of a solution's ability to meet business need and deliver expected value, covering four assessment types and producing a recommendation at 30/60/90 days post-deployment.

**One-paragraph:** A structured evaluation of a solution's ability to meet business need and deliver expected value, covering four assessment types and producing a recommendation at 30/60/90 days post-deployment.

## Applies If (ALL must hold)

- 30/60/90-day post-launch checkpoints when the business case promised quantified outcomes
- Pre-go-live deployment readiness gate: aggregate QA, ops, support, training, and security signals into a single accept/reject
- Phase-gate reviews on long programs (CRM, ERP, billing migrations) before funding the next phase
- Vendor/SaaS contract renewal — assess deployed solution against original requirements and SLA
- Compliance/audit cycles (SOX, ISO, HIPAA) requiring documented evaluation that requirements were met
- Post-incident assessment: was the failure a missed requirement, implementation gap, or unmeasured non-functional?

## Skip If (ANY kills it)

- Throwaway prototypes or internal tools with 5 or fewer users — run a 15-minute retrospective instead
- Pre-PMF early-stage startups where requirements change every sprint — use continuous discovery
- When there is no baseline: without a measured "before", variance cannot be computed and the report is meaningless
- As a substitute for ongoing monitoring — a one-shot report that sits until the next audit is the canonical anti-pattern
- When the assessor reports to the project sponsor whose bonus depends on the result — independence is required
- Pure technical performance tuning (latency, throughput) — use SRE/SLO frameworks instead

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
