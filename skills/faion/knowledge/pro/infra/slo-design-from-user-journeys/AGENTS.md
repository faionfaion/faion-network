---
slug: slo-design-from-user-journeys
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: SLO Design From User Journeys — how to pick SLIs and SLO targets that anchor on real user journeys (not infra metrics) before the first production deploy.
content_id: "4560c2d9324be786"
tags: [slo-design-from-user-journeys, infra, pro]
---
# SLO Design From User Journeys

## Summary

**One-sentence:** A method for deriving Service Level Indicators (SLIs) and Service Level Objectives (SLOs) from real user journeys — the critical-path actions a user takes — before the first production deploy, so dashboards measure outcomes instead of infra noise.

**One-paragraph:** Faion has Prometheus, Grafana, and the observability-architecture corpus but zero content on how to actually pick SLIs/SLOs from real user journeys. This is the foundational SRE skill — without it the dashboards are decoration and on-call gets paged on CPU spikes that customers never feel. The methodology walks from "list the 3 user journeys that produce revenue" → "pick the failure mode that journey notices" → "express that as an SLI ratio" → "set an SLO from current performance + business tolerance".

## Applies If (ALL must hold)

- a service is about to enter production OR is in production with no defined SLOs
- the service maps to identifiable user journeys (HTTP requests, async jobs, etc.)
- there is an instrumentation path (Prometheus, OTel, logs) that can express ratios
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the service is purely internal infrastructure with no user-visible journey (use platform-internal SLOs instead)
- there is already a working SLO grounded in journeys — extend, don't redesign
- the team has no on-call coverage and no plan to act on SLO breaches

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: SLI ratio form, ≤3 journeys, current-perf baseline, business-tolerance gate, single-owner |

## Related

- upstream playbook: `role-devops-engineer/Design SLOs + error budgets before first deploy`
- parent skill: `pro/infra/`
- related methodologies: `pro/infra/burn-rate-multi-window-alerting`, `pro/infra/error-budget-policy-and-freeze-rules`
