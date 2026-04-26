# Risk Management

## Summary

Identify threats and opportunities, rate them by probability and impact, assign owners with observable triggers, plan responses, and monitor weekly. The rule: every risk must have a named owner (a person, not "the team") and explicit triggers — observable signals that convert an abstract risk into an actionable event. "Accept" is not a free pass; it requires a contingency budget line equal to the risk's EMV.

## Why

Surprises become crises because risks were identified but not tracked. EMV (Probability × Impact in dollars) provides a relative ranking and seeds contingency reserves — it does not imply precision. A risk that materializes becomes an Issue and leaves the register; double-tracking inflates the register and hides what is actually in flight. Risk reviews must be short (15 min) and frequent (weekly), not 2-hour quarterly exercises.

## When To Use

- Project initiation: build initial risk register before charter sign-off
- Stage-gate reviews: refresh probability/impact and trigger statuses
- Pre-launch (T-2 weeks): focused launch-risk pass with rollback plans
- After incidents: feed lessons back as new risks for similar projects
- High-uncertainty domains: new technology, new vendor, regulatory change

## When NOT To Use

- Trivial internal task (1 person, under 1 week, no external dependency) — overhead exceeds value
- Pure agile teams with strong incremental delivery — short cycles already de-risk; use a "top 5" sticky list
- Crisis already in progress — switch to incident response; add lessons to register afterward

## Content

| File | What's inside |
|------|---------------|
| `content/01-risk-framework.xml` | Risk types, four-step process, threat/opportunity response strategies, EMV formula |
| `content/02-risk-antipatterns.xml` | Common failures: subjective scoring, stale register, Accept abuse, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Risk register table: ID, category, P, I, score, response, owner, trigger, status |
| `templates/risk-response-plan.md` | Individual risk response plan with prevention steps and fallback actions |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/risk-score.py` | Compute Score and EMV from risks.yaml using deterministic P×I matrix |
