---
slug: api-monitoring-alerting
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Define SLOs before writing any alert rules.
content_id: "3f1b94f0d9f4c6dd"
tags: [api-monitoring, alerting, slo, prometheus, burn-rate]
---
# API Alerting: SLOs, Burn-Rate Rules, and Dashboards

## Summary

**One-sentence:** Define SLOs before writing any alert rules.

**One-paragraph:** Define SLOs before writing any alert rules. All alert thresholds MUST derive from stated SLOs using multi-window multi-burn-rate PromQL (SRE Workbook ch.5). Simple threshold alerts ("5xx > 1%") are noise without an SLO anchor. Every alert MUST have a runbook_url annotation, a severity label (page|ticket), and a for: clause of at least 2 minutes.

## Applies If (ALL must hold)

- Any production API service that has defined SLOs and needs alert rules wired to PagerDuty, Opsgenie, or Squadcast.
- Establishing SLIs and error budgets before a planned launch or scale event.
- Migrating from threshold-based alert rules to burn-rate alert rules.
- Onboarding a new microservice into an existing Prometheus + Alertmanager stack.

## Skip If (ANY kills it)

- Pre-product-fit prototypes — alert overhead exceeds value; a single Slack webhook on 5xx is sufficient.
- Internal tools used by fewer than 10 people daily — alert fatigue from a full burn-rate setup exceeds the incident cost.
- Services without a defined SLO — do not write alert rules before defining what you are protecting. The SLO is the prerequisite.

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

- parent skill: `pro/dev/software-developer/`
