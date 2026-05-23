# Solo Launch-Day Runbook

## Summary

**One-sentence:** Hour-by-hour solo-founder launch-day runbook — Stripe live, monitoring armed, mailer warm, fallback content queued, support inbox covered, social burst — so the single operator follows a script on the highest-stakes day of the quarter.

**One-paragraph:** Strategic product-launch methodologies cover positioning and timing; the operational hour-by-hour runbook for a solo founder is missing. Solo launch days are when small mistakes compound — Stripe in test mode, mailer rate-limited, no fallback when the homepage errors, social posts going out before the product is reachable. This methodology pins a 24-hour runbook with checkpoints at T-24h / T-2h / T+15m / T+1h / T+4h / T+12h / T+24h. Each checkpoint lists exact actions; the runbook is meant to be RUN on the day, not read. Output is a per-launch `launch-YYYY-MM-DD.md` execution log derived from the template.

**Ефективно для:**

- Solo founder launching a paid product (Stripe live + mailing list + social).
- Major release where small mistakes compound during a high-traffic window.
- Anchored sequel launches where last quarter's lessons feed the runbook.
- Coordinating multi-channel announce burst (mailing list + X + LinkedIn + IH + PH) under a script.

## Applies If (ALL must hold)

- Solo founder (or ≤2-person team) launching a product or major release.
- Live payments via Stripe (or equivalent) or paid sign-ups expected.
- Monitoring (Sentry + uptime + Plausible) in place.
- Transactional email working (welcome, receipts).
- ≥1 announcement channel (mailing list, X, LinkedIn, IndieHackers, Product Hunt).

## Skip If (ANY kills it)

- Enterprise launch with PR firm + comms team — different runbook.
- Launch is internal / private beta — over-engineered.
- Payments not live (free product) — skip Stripe sections, retain monitoring sections.
- Founder has launched ≥3 times — adapt this as a checklist, do not require it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stripe live keys provisioned (not yet active) | env vars | platform |
| Monitoring channels alive + tested | Sentry DSN + Plausible token + uptime check | engineering |
| Mailer warmed (≥48h before launch) | provider dashboard | marketing |
| Fallback content drafted (status page, holding page, refund template) | repo files | founder |
| Announce burst content ready in every channel | drafts | founder |
| 1Password unlocked for the day; SSH access verified | op session | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-time-tracking-discipline]] | Launch-day hours feed time tracking; capture habit applies. |
| [[reporting-dashboards]] | Post-launch metrics rollup uses the dashboard pipeline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pre-checked smoke tests, Stripe live ≥2h, fallback in place, change freeze, ≤10-min rollback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for per-launch execution log + checkpoints + rollback log | ~1000 |
| `content/03-failure-modes.xml` | essential | 7 modes: Stripe still test, mailer rate-limit, fallback missing, late-config cascade, support drowned, monitoring silent, founder exhaustion | ~1100 |
| `content/04-procedure.xml` | essential | 7-step timeline procedure T-24h → T+24h | ~1000 |
| `content/05-examples.xml` | essential | Worked example: a launch that hit fm-01 (Stripe-test) and the corrected version | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping inputs → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `smoke_test_runner` | haiku | Deterministic checklist execution. |
| `checkpoint_summary_drafter` | sonnet | Compose checkpoint update messages. |
| `support_inbox_first_response` | sonnet | Draft canned but personalised responses. |
| `rollback_decision_brief` | opus | Frame the rollback decision when things go sideways. |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-runbook.md` | Hour-by-hour template |
| `templates/smoke-tests.md` | Pre-launch verification checklist |
| `templates/rollback-runbook.md` | Step-by-step rollback procedure |
| `templates/support-canned-responses.md` | First-day FAQ responses |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-launch-day-runbook.py` | Validate the execution log against 02-output-contract schema | After launch closeout |

## Related

- [[reporting-dashboards]]
- [[solo-time-tracking-discipline]]
- [[status-report-templates-by-audience]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by Stripe state, smoke-test recency, fallback presence, change-freeze observance, and rollback readiness onto a rule from `content/01-core-rules.xml`. Walk it before every announce; the pre-flight branches block-or-approve in seconds.
