# Pricing experiment toggle

## Why this playbook exists
Indie hackers run the entire pipeline alone — research, build, ship, market, support, and decide — under tight calendar constraints and often from a nomad schedule. Static pricing → one variable flipped for 14 days with a measured paid-conversion delta. This playbook turns that ambition into a sequenced set of stages with explicit decision gates so the founder doesn't confuse motion for progress and doesn't keep paying for products that quietly stopped working.

## What changes after running it
Bi-weekly: flip one pricing variable (price, billing period, trial length, plan name) for 14 days, measure paid conversion delta vs baseline, and decide keep, rollback, or iterate.

## Stage flow
### Hypothesis
One pricing variable with a directional hypothesis.

**Tasks**
- Pick one variable (price, billing, trial, plan name)
- State expected direction of conversion change
- Set a minimum significance threshold

**Decision gate**
> Advance once the hypothesis fits in one sentence.

### Toggle
Switch flipped in Stripe or pricing page.

**Tasks**
- Implement the change end-to-end
- Confirm checkout still completes
- Update marketing copy that references price

**Decision gate**
> Advance only after stranger test passes.

### Measure
14 days of clean data versus baseline.

**Tasks**
- Pull paid conversion data at day 7 and day 14
- Compare to baseline cohort
- Note any seasonality risk

**Decision gate**
> Advance once both checkpoints have data.

### Decide
Keep, rollback, or iterate with a written verdict.

**Tasks**
- Write a one-paragraph verdict
- Update pricing experiment log
- Queue next variable to test

**Decision gate**
> Keep only if delta exceeds threshold; otherwise rollback.

## When to skip a stage
Every stage exists because indie hackers historically skip exactly that one — Validate is skipped by builders who fall in love with code, Decide is skipped by founders who can't bear to kill a product, and Cadence is skipped when travel tempts a creator into silence. If you must skip a stage, write a one-paragraph rationale in the playbook artefact log so the next run can audit the trade-off.

## How this playbook compounds
The artefacts from each run — quotes, postmortems, conversion tables, hook banks — feed directly into the next playbook the founder runs. A weekly review fed by these outputs is the difference between a portfolio of half-finished projects and a portfolio of compounding bets. Treat every gap[] entry as a methodology to ship; the playbook stays in draft until the gaps clear.

## Reading order
First-time runs should read the playbook YAML end-to-end before starting Stage 1. Repeat runs can jump to the stage matching current ambiguity and skim only that stage's methodologies. The decision gate is always the source of truth — even if the founder feels confident, the gate decides.

## Failure modes to watch
- Mistaking audience engagement for paying intent; the playbook insists on a paid checkpoint.
- Letting one stage drag because the next is intimidating — the gate is meant to force the move.
- Burning out by trying to combine this playbook with two others in the same week.

## Done means done
The playbook is done when every success criterion is checked AND a written verdict exists in the founder's notes. Anything short of a written verdict is an in-progress playbook — file it back into the queue and keep going.
