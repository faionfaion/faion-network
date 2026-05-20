---
slug: dora-metrics
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: DORA (DevOps Research and Assessment) metrics are four research-validated KPIs that measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore.
content_id: "b0d7d14c181a3387"
tags: [dora, metrics, devops, ci-cd, observability]
---
# DORA Metrics

## Summary

**One-sentence:** DORA (DevOps Research and Assessment) metrics are four research-validated KPIs that measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore.

**One-paragraph:** DORA (DevOps Research and Assessment) metrics are four research-validated KPIs that measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore. Elite teams deploy 208x more often and recover 2,604x faster than low performers. A fifth metric — Reliability (SLO achievement) — was added in 2025. AI-generated code reduces delivery stability by approximately 7%, so batch size must be monitored when using AI tools.

## Applies If (ALL must hold)

- Engineering org wants a baseline + improvement plan for software delivery performance.
- Quarterly/annual exec reporting: leadership needs a credible answer to "are we shipping faster?".
- Tracking AI-assistant adoption impact (DORA 2025 research shows AI affects stability/throughput; need data).
- Comparing teams' delivery health without falling into "lines of code" or "story points" anti-metrics.
- Justifying platform/CI investments — DORA metrics provide before/after evidence.
- Setting up engineering metrics for a team or service for the first time.
- Evaluating CI/CD pipeline health before a refactoring sprint.
- Connecting engineering output to business outcomes (revenue, churn, team wellbeing).
- Running quarterly DevOps performance reviews.
- Designing a metrics collection system backed by CI/CD + incident tools.

## Skip If (ANY kills it)

- Single-person / very small teams — the variance dominates the signal.
- As a stack-rank tool ("Team X is Elite, Team Y is Low — fire the manager"). Goodhart's Law applies hard.
- For non-software work (data pipelines, ML training, content) — definitions don't transfer cleanly.
- When the org doesn't yet have basic CI/CD — measure something else first (build pass rate, deploy automation %).
- As the only health metric — DORA + Reliability + SPACE + developer experience surveys complement each other.
- Comparing individual developers — metrics are team-level, not individual.
- Early-stage prototype projects with no production — no deployment signal to measure.
- When incident tooling (PagerDuty, Opsgenie) is not yet integrated — MTTR will be inaccurate.

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

- parent skill: `pro/infra/cicd-engineer/`
