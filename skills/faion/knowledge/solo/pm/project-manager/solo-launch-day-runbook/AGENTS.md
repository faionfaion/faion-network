---
slug: solo-launch-day-runbook
tier: solo
group: project-manager
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5ffe9ba808fa6633"
summary: Hour-by-hour operational runbook for a solo founder's launch day — Stripe live, monitoring armed, mailer warm, fallback content queued, support inbox, social burst — so the one operator does not improvise on the most expensive day of the quarter.
tags: [launch, solo, runbook, stripe, monitoring, founder]
---

# Solo Launch-Day Runbook

## Summary

**One-sentence:** Hour-by-hour solo-founder launch-day runbook — Stripe live, monitoring armed, mailer warm, fallback content queued, support inbox covered, social burst — so the single operator follows a script on the highest-stakes day of the quarter.

**One-paragraph:** Strategic product-launch methodology covers positioning and timing; the operational hour-by-hour runbook for a solo founder is missing. Solo launch days are when small mistakes compound — Stripe in test mode, mailer rate-limited, no fallback when the homepage errors, social posts going out before the product is reachable. This methodology pins a 24-hour runbook: T-24h preparation (final smoke tests, Stripe live key swap, fallback content frozen), T-2h to T-0 final checks, T+0 to T+12h launch window with explicit checkpoint times (15m, 1h, 4h, 12h post-launch), T+24h closeout. Each checkpoint lists exact actions: what to verify, where to look, what triggers rollback, how to respond to common questions in the support inbox. The runbook is meant to be RUN on the day, not just read. Mechanism: pre-loaded runbook + checkpoint timers + tg-bot integration for self-check. Primary output: a per-launch `launch-YYYY-MM-DD.md` execution log, derived from the template.

## Applies If (ALL must hold)

- solo founder (or ≤2-person team) launching a product or major release
- live payments via Stripe (or equivalent) or paid sign-ups expected
- monitoring (Sentry + uptime + Plausible) in place
- transactional email working (welcome, receipts)
- ≥1 announcement channel (mailing list, X, LinkedIn, IndieHackers, Product Hunt)

## Skip If (ANY kills it)

- enterprise launch with PR firm + comms team — different runbook
- launch is internal / private beta — over-engineered
- payments not live (free product) — skip Stripe sections, retain monitoring sections
- founder has launched ≥3 times — adapt this as a checklist, do not require it

## Prerequisites

- Stripe live keys provisioned but NOT yet in production
- monitoring channels alive and tested
- mailer warmed (first emails to small list ≥48h before launch)
- fallback content drafted (status page, holding page, refund response)
- launch announcement content ready in every channel
- 1Password unlocked for the day; SSH access verified

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/devops-engineer/sentry-alert-routing-for-solos` | Alert routing for the day |
| `solo/pm/project-manager/idea-to-validated-mvp-launch` | Strategic launch context this operationalises |
| `solo/pm/project-manager/pre-launch-beta-program` | Beta-day learnings feed this runbook |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pre-checked smoke tests, Stripe live ≥2h before announce, fallback in place, no live key changes mid-launch, rollback ≤10 min | ~1100 |
| `content/02-output-contract.xml` | essential | Per-launch execution-log schema, checkpoint shape, rollback decision log | ~800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: Stripe still test, mailer rate-limit, fallback missing, etc. | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `smoke_test_runner` | n/a | Deterministic checklist execution |
| `checkpoint_summary_drafter` | sonnet | Compose checkpoint update messages |
| `support_inbox_first_response` | sonnet | Draft canned but personalised responses |
| `rollback_decision_brief` | opus | Frame the rollback decision when things go sideways |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-runbook.md` | Hour-by-hour template |
| `templates/smoke-tests.md` | Pre-launch verification checklist |
| `templates/rollback-runbook.md` | Step-by-step rollback procedure |
| `templates/support-canned-responses.md` | First-day FAQ responses |
| `templates/announce-schedule.md` | Per-channel announce queue |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/preflight.sh` | Run all pre-launch smoke tests | T-24h and T-2h |
| `scripts/stripe-live-verify.sh` | Verify Stripe keys are live + a $1 test charge | T-2h |
| `scripts/launch-checkpoint-ping.sh` | Send checkpoint update to tg-bot + log to execution file | At each checkpoint |

## Related

- parent skill: `solo/pm/project-manager/`
- peer methodologies: `idea-to-validated-mvp-launch`, `pre-launch-beta-program`, `sentry-alert-routing-for-solos`, `weekly-product-launch-cadence`
- external: [Stripe — Going live checklist](https://stripe.com/docs/development/checklist) · [Indie Hackers — Launch day guides](https://www.indiehackers.com/) · [Product Hunt — Launch guide](https://www.producthunt.com/launch)
