# Sentry Alert Routing for Solos

## Summary

**One-sentence:** Generates a solo-alerting.yaml config — Sentry + Plausible + email-bounce + uptime → filter → digest → quiet-hours → single channel — so one human is paged only for actionable incidents.

**One-paragraph:** Generates a solo-alerting.yaml config — Sentry + Plausible + email-bounce + uptime → filter → digest → quiet-hours → single channel — so one human is paged only for actionable incidents.

**Ефективно для:**

- Solo operator running prod without an on-call rotation.
- Founder drowning in Sentry noise during weekdays.
- Quiet-hours discipline so weekends are protected.
- Single pager channel (Telegram / email / SMS).

## Applies If (ALL must hold)

- Single operator running production (no on-call rotation).
- Production system has Sentry / Plausible / transactional email / uptime monitor (all four typical).
- Operator has the ability to set rules in each tool's UI / API.
- Operator has at least one explicit channel they read.

## Skip If (ANY kills it)

- Multi-person on-call rotation — use PagerDuty / Opsgenie methodology.
- No uptime monitor configured — install one first.
- Regulated business with mandatory immediate alerting on any error — use compliance methodology.
- No Sentry / Plausible / mail bounce — adapt the source filters.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Sentry project DSN | url | Sentry org |
| Plausible site id | string | Plausible dashboard |
| Uptime monitor | url | UptimeRobot / Better Stack |
| Pager channel | url|email | Telegram chat id or email |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| docker-compose-devops | Production deployment context. |
| solo-deploy-checklist | Launch-day complements daily alerting. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-source-side-filtering-first, r2-digest-by-default, r3-quiet-hours-hard-cut, r4-single-pager-channel, r5-named-owner | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Sentry Alert Routing for Solos artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: alarm-fatigue, missed-real-alert, quiet-hours-blind-spot | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-sentry-alert-routing-for-solos` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-sentry-alert-routing-for-solos` | sonnet | Bounded structural check against the output contract. |
| `review-sentry-alert-routing-for-solos` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sentry-alert-routing-for-solos.json` | JSON skeleton matching the output contract. |
| `templates/sentry-alert-routing-for-solos.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sentry-alert-routing-for-solos.py` | Validate Sentry Alert Routing for Solos output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[docker-compose-devops]]
- [[solo-deploy-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
