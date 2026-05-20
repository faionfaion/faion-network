---
slug: slo-burn-rate-review-protocol
tier: geek
group: software-developer
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "063ff3b83b649b9e"
summary: Weekly 30-minute architecture ritual that converts the past week's SLO burn data into named ADR-worthy decisions, paired with the burn-decision matrix, so error budgets become a live architectural input rather than wallpaper.
tags: [slo, error-budget, architecture, weekly-review, adr, burn-rate]
---

# SLO Burn-Rate Review Protocol

## Summary

**One-sentence:** Weekly 30-minute architect-led ritual converting the past week's SLO burn data + matrix-triggered actions into named ADR-worthy decisions, so error budgets drive architecture rather than decorate dashboards.

**One-paragraph:** Reliability-architecture methodology covers patterns; the burn-rate decision matrix covers in-the-moment actions. Between them is a missing ritual: a regular forum where architecture absorbs what burn-rate is telling it. Without the review, error budgets become a passive metric — burn happens, mitigations happen, but the underlying architecture does not change. This methodology pins a weekly 30-minute review with five named items: (1) last week's burn-rate trace per SLO, (2) matrix-triggered actions and overrides, (3) postmortem actions due, (4) architectural decisions invited by burn pattern, (5) recontract candidates (SLOs that no longer match user pain). The review's output is a decision log entry, NOT a slack thread. Mechanism: data prep → 30-min review → decision log → ADR if needed. Primary output: a `burn-review-YYYY-WW.md` weekly note + ADRs spawned from named decisions.

## Applies If (ALL must hold)

- SLOs in use with burn-rate alerting (`pro/infra/devops-engineer/slo-definition-template-per-service-class`)
- burn decision matrix in use (`pro/infra/devops-engineer/slo-burn-decision-matrix`)
- architect or tech lead with authority to drive architectural decisions
- ≥1 production service for ≥3 months (enough history)

## Skip If (ANY kills it)

- no SLOs OR no burn-rate alerts in use — burn-rate review is built on the data those produce
- single-service shop with no architectural decisions to make — overhead exceeds value
- the team meets daily already and absorbs burn signals there — no new ritual needed
- architecture changes are politically blocked — the review will surface decisions that go unactioned, breeding cynicism

## Prerequisites

- access to burn-rate dashboards (Grafana / Honeycomb / Datadog)
- audit log of matrix-triggered actions from `slo-burn-decision-matrix`
- postmortem tracking system
- 30-minute weekly slot with the required attendees (architect, on-call lead, product representative)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/slo-definition-template-per-service-class` | Defines the SLOs being reviewed |
| `pro/infra/devops-engineer/slo-burn-decision-matrix` | Supplies the actions log this review aggregates |
| `pro/dev/software-architect/retro-adr-workflow` | Captures decisions arising from the review |
| `pro/dev/software-architect/architecture-fitness-functions` | Where systemic fixes attach |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: weekly cadence, fixed agenda, decision-output not discussion-output, attendee minimum, written log | ~1000 |
| `content/02-output-contract.xml` | essential | Review-note shape, decision-log entry schema, ADR spawning rule | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: meeting without decisions, attendee drift, blame surface, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `data_prep_burn_trace` | n/a | Deterministic data pull |
| `agenda_pre_brief` | sonnet | Compose the 5-item brief with current week's evidence |
| `decision_capture_drafting` | sonnet | Write the post-review decision log from notes |
| `adr_spawn_check` | sonnet | Decide whether the decision rises to ADR weight |

## Templates

| File | Purpose |
|------|---------|
| `templates/burn-review.md` | Review note template (5 sections) |
| `templates/decision-log-entry.md` | Decision-log entry shape |
| `templates/agenda-pre-brief.md` | 1-page brief sent 24h pre-meeting |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/prep-burn-review.py` | Pull last week's burn data, matrix audit log, postmortem actions; render brief | 24h pre-meeting |
| `scripts/lint-review-note.py` | Verify all five sections + decision log entry present | Post-meeting |

## Related

- parent skill: `geek/dev/software-developer/`
- peer methodologies: `slo-definition-template-per-service-class`, `slo-burn-decision-matrix`, `architecture-fitness-functions`, `retro-adr-workflow`
- external: [Google SRE Workbook — Implementing SLOs](https://sre.google/workbook/implementing-slos/) · [DORA Accelerate](https://dora.dev/) · [Charity Majors — Honeycomb on observability](https://charity.wtf/)
