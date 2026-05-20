---
slug: on-call-rotation-bootstrap
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "04bada118b561e12"
summary: A bootstrap kit for designing a humane on-call rotation: shift length, escalation tree, comp-time policy, follow-the-sun handoff, on-call-load metrics, and a dual-track for new joiners.
tags: [on-call, sre, devops, rotation, burnout, escalation]
---

# On-Call Rotation Bootstrap

## Summary

**One-sentence:** Stand up a humane on-call rotation in a small-to-mid team (5-30 engineers) with explicit shift design, escalation tree, comp-time, follow-the-sun handoff, and burnout-prevention metrics — before the team backs into the wrong defaults.

**One-paragraph:** Faion has incident runbooks but no methodology for the rotation itself. Most teams reverse-engineer their on-call rotation from a stressed Friday afternoon and end up with the worst-of-all-worlds design: 24/7 single-engineer shifts, no comp, no shadow period for new joiners, no acknowledgement SLA, and the same on-call burning out every 6 months. This methodology defines the explicit choices that go into a rotation: shift length (8h / 24h / weekly), single-tier vs primary+secondary, follow-the-sun vs single-timezone, escalation paths and timeouts, comp-time policy (time-off-in-lieu vs cash), shadow period for new joiners, and on-call-load metrics with red-line thresholds. Primary output: a one-page on-call charter + a PagerDuty/Opsgenie/Better Stack schedule config + a comp-time policy in the HR handbook.

## Applies If (ALL must hold)

- team is responsible for a production system with paying customers OR an internal SLA
- team has 5-30 engineers eligible to participate in the rotation
- no formal on-call rotation exists yet, OR existing rotation is informal and breaking
- engineering leader has budget authority for comp-time (hours-off-in-lieu OR cash) for on-call work

## Skip If (ANY kills it)

- team smaller than 5 — rotation math does not work; use a shared-pager + paid retainer with an external SRE consultancy until headcount grows
- system has no real users / no SLA — on-call is theatre; defer until you have a customer who has paid you to be reachable
- pre-existing rotation works and team is happy — do not redesign without a signal of dysfunction
- regulated environment (banking, healthcare) where rotation design is governed by external compliance — apply those rules first, this methodology second

## Prerequisites

- monitoring + alerting stack exists and produces actionable alerts (no rotation can fix a noisy stack)
- runbook discipline at least at the "one runbook per top-5 alert" level
- HR / legal sign-off for the comp policy and any after-hours work compensation rules
- documented business-hours coverage expectations from the customer-facing side

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-elk-queries-alerting` | Alert-quality threshold must be acceptable before rotation design adds value |
| `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` | Runbook format consumed at incident time |
| `pro/infra/devops-engineer/dora-metrics` | MTTR is one of the rotation-health metrics |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: explicit charter, ack SLA, two-tier rotation, comp-time policy, on-call-load red-line | ~900 |
| `content/02-output-contract.xml` | essential | On-call charter schema, schedule config schema, load-metric schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: single-engineer rotation, no comp, alerts-as-rotation, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shift_length_proposal` | sonnet | Cross-input judgment (team size, geographic spread, alert volume) |
| `escalation_tree_design` | sonnet | Bounded judgment per alert severity |
| `comp_time_policy_drafting` | opus | Cross-function synthesis with HR and finance constraints |
| `paging_tool_config_generation` | haiku | Template fill into the chosen tool config |

## Templates

| File | Purpose |
|------|---------|
| `templates/on-call-charter.md` | One-page charter posted to team wiki |
| `templates/pagerduty-schedule.yaml` | PagerDuty schedule config skeleton |
| `templates/opsgenie-rotation.json` | Opsgenie rotation skeleton |
| `templates/comp-time-policy.md` | HR-handbook-ready comp-time policy document |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/on-call-load-report.py` | Computes per-engineer pages/week, off-hours pages, weekend pages, and flags red-line crossings | Weekly cron |
| `scripts/shadow-period-tracker.py` | Tracks new-joiner shadow shifts, certifies them after N successful shadow + N solo with safety-net | On rotation onboarding |

## Related

- parent skill: `pro/infra/devops-engineer/SKILL.md`
- peer methodologies: `pro/infra/devops-engineer/dora-metrics`, `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- external: [Google SRE Book, Chapter 11 "Being On-Call" (O'Reilly, 2016)] · [Beyer et al., The Site Reliability Workbook Chapter 8 (O'Reilly, 2018)] · [PagerDuty Operations Maturity Model] · [Increment Magazine, "On-Call" issue (Stripe Press)]
