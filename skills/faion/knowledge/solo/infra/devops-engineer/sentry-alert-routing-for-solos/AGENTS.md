---
slug: sentry-alert-routing-for-solos
tier: solo
group: devops-engineer
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "8619c2ea25720d83"
summary: Solo-operator pattern for routing Sentry + Plausible + transactional-email + uptime alerts through filters, digests, and quiet-hours so a single human gets paged only for real, actionable, on-call incidents.
tags: [sentry, alerting, solo, plausible, uptime, quiet-hours, on-call]
---

# Sentry Alert Routing for Solos

## Summary

**One-sentence:** Filter + digest + quiet-hours pattern for solo operators to route Sentry, Plausible, transactional-email bounces, and uptime alerts so one human is paged only for real, actionable, on-call incidents.

**One-paragraph:** Generic alerting methodology assumes a multi-person on-call rotation that can absorb noise; a solo operator cannot. The dominant solo failure is alarm fatigue: 200 Sentry events/day, three Plausible threshold alerts, two email-bounce notifications, one uptime flap — the operator silences the channel and misses the one event that matters. This methodology pins solo-scale routing: rule-based filters at the source (Sentry filter rules, Plausible cooldown), batching into digests (hourly low-priority, daily summary), quiet-hours with hard escalation cut-off (no Sentry pages 22:00-08:00 unless ≥100 events/min OR uptime down ≥10min), and a single named pager channel (one Telegram chat, one email inbox, one SMS path). Mechanism: rule-based source-side filtering → digest aggregation → quiet-hours gate → single delivery channel. Primary output: a `solo-alerting.yaml` config + per-source rule sets.

## Applies If (ALL must hold)

- single operator running production (no on-call rotation)
- production system has Sentry / Plausible / transactional email / uptime monitor (all four typical)
- the operator has the ability to set rules in each tool's UI / API
- the operator has at least one explicit channel they read (Telegram, email, SMS)

## Skip If (ANY kills it)

- multi-person on-call rotation — use standard PagerDuty / Opsgenie methodology
- no uptime monitor configured — install one first (UptimeRobot, Better Stack, Pingdom — even the free tier suffices)
- regulated business with mandatory immediate alerting on any error — use compliance methodology, not this one
- no Sentry / Plausible / mail bounce — the routing pattern still applies, adapt the source filters

## Prerequisites

- Sentry project (or equivalent: Rollbar, Bugsnag, Honeybadger)
- Plausible Analytics (or equivalent: Fathom, Simple Analytics)
- Uptime monitor (UptimeRobot or Better Stack)
- One pager channel (Telegram bot, email inbox, or SMS endpoint)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/devops-engineer/docker-compose` | Production deployment context |
| `pro/infra/devops-engineer/slo-burn-rate-review-protocol` | Higher-tier counterpart for multi-operator setups |
| `solo/pm/project-manager/solo-launch-day-runbook` | Launch-day complements daily alerting |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: source-side filtering first, digest by default, quiet-hours hard cut, single pager channel, escalation matrix | ~1100 |
| `content/02-output-contract.xml` | essential | solo-alerting.yaml schema, per-source rule taxonomy, channel config | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: alarm fatigue, missed real alert, quiet-hours blind spot, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sentry_rule_generator` | sonnet | Generate filter expressions from operator's described patterns |
| `digest_summary_drafter` | sonnet | Produce hourly/daily readable digest from raw events |
| `quiet_hours_evaluator` | n/a | Pure deterministic clock check |
| `escalation_decider` | sonnet | Decide whether to break quiet hours based on severity vector |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-alerting.schema.yaml` | Schema for the config |
| `templates/sentry-filter-rules.md` | Common Sentry filter patterns |
| `templates/digest-format.md` | Hourly + daily digest format |
| `templates/quiet-hours-matrix.md` | Per-source quiet-hours rules |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/apply-rules.py` | Push filter rules to Sentry / Plausible via API; idempotent | After editing solo-alerting.yaml |
| `scripts/build-digest.py` | Pull last N hours from each source, render digest, send to channel | Cron hourly (low-prio) and daily (full) |
| `scripts/escalation-gate.py` | Evaluate whether to break quiet hours given event severity | Triggered by Sentry webhook |

## Related

- parent skill: `solo/infra/devops-engineer/`
- peer methodologies: `docker-compose`, `slo-burn-rate-review-protocol`, `solo-launch-day-runbook`
- external: [Sentry alert rules docs](https://docs.sentry.io/product/alerts/) · [Better Stack on-call playbook](https://betterstack.com/community) · [Plausible API](https://plausible.io/docs/stats-api)
