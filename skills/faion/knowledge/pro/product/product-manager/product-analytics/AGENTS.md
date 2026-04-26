# Product Analytics

## Summary

Product analytics is measuring and analyzing user behavior to make better product decisions. The key discipline: define which decisions each event will inform before implementing tracking. Freeze the event taxonomy in git (`tracking-plan.md` as source of truth); runtime catalogs drift toward it via PR, never the other way. Structure analytics as a four-stage agent pipeline: plan → implement → monitor → analyze.

## Why

Teams that track everything understand nothing. The failure mode is vanity metrics (total signups, DAU) that move with marketing spend but don't inform product decisions. Decision-first tracking — every event must state which decision it informs — stops the sprawl. Agents replicate the vanity-metric pattern by default; the event taxonomy and tracking plan must be in the system prompt as constraints.

## When To Use

- Pre-launch: drafting the tracking plan from a feature spec so day-1 events ship with the code.
- Activation diagnosis: funnel drop + cohort data → pinpoint highest-leakage step → propose experiments.
- Weekly product-health digest: scheduled agent reads BI source, writes markdown summary with anomalies.
- Post-experiment readout: merge A/B exposure logs with metric tables, flag Simpson's-paradox segments.
- Tracking-plan audit before a vendor migration (GA4 → PostHog).

## When NOT To Use

- Pre-PMF with fewer than 100 weekly active users — sample sizes are too small; talk to users instead.
- Causal claims with only observational data — funnels answer "what," not "why."
- Exec one-pagers needing judgment — let the agent prep data, a human writes the recommendation.
- High-cardinality PII queries without aggregation/scrubbing.
- Replacing a tracking plan review with a one-shot LLM call.

## Content

| File | What's inside |
|------|---------------|
| `content/01-analytics-framework.xml` | Maturity levels, AARRR metric categories, 5-step implementation process |
| `content/02-tracking-rules.xml` | Decision-first events, naming convention (object_action), server vs. client rule, cohort fixed-window rule |

## Templates

| File | Purpose |
|------|---------|
| `templates/tracking-plan.md` | Tracking plan template: user properties, onboarding events, core feature events, conversion events |
| `templates/tracking-plan-lint.sh` | Enforce snake_case naming and required fields on the tracking plan markdown |
