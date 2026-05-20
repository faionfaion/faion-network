---
slug: quality-management
tier: pro
group: pm
domain: pm-traditional
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three-process quality discipline: Plan Quality (define standards and measurable thresholds), Manage Quality / Assurance (ensure processes produce quality), and Control Quality (verify deliverables meet standards via deterministic gates).
content_id: "d318ef649fa64829"
tags: [quality-management, quality-gates, definition-of-done, cost-of-quality, defect-triage]
---
# Quality Management

## Summary

**One-sentence:** Three-process quality discipline: Plan Quality (define standards and measurable thresholds), Manage Quality / Assurance (ensure processes produce quality), and Control Quality (verify deliverables meet standards via deterministic gates).

**One-paragraph:** Three-process quality discipline: Plan Quality (define standards and measurable thresholds), Manage Quality / Assurance (ensure processes produce quality), and Control Quality (verify deliverables meet standards via deterministic gates). Quality gates are computed from CI artifacts and threshold files — never from narrative opinion. Every gate decision (release / hold / abort) requires human approval; agents emit recommendations only.

## Applies If (ALL must hold)

- Software programs with external acceptance criteria (UAT sign-off, FDA/EMA submission, ISO 9001 audits)
- Multi-team programs where Definition of Done drift creates integration defects
- Regulated domains needing a documented Quality Plan and QC records
- Programs with SLA/SLO obligations where escape defect rates are contractual
- Quality gates in CI/CD pipelines that block merges, releases, and deployments

## Skip If (ANY kills it)

- Pre-PMF startups iterating on prototypes — heavy quality plans slow learning; use basic CI checks and code-quality
- Throwaway spikes or POCs where the deliverable is "demo runs once"
- One-person side projects — checklist overhead exceeds defect cost
- When the real bottleneck is requirements clarity — fix scope and requirements first

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

- parent skill: `pro/pm/pm-traditional/`
