---
slug: weekly-portfolio-metric-scan
tier: solo
group: product-ops
persona: P2
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Multi-product noise → one product that earns the next week's attention."
content_id: dfa1eb68657977f3
methodology_refs:
  - ops-dashboard-setup
  - vanity-metrics-audit
  - feature-prioritization-rice
  - rice-for-design
  - portfolio-triage-indie
  - weekly-pm-async-broadcast-template
  - kill-or-keep-criteria
---

# Weekly portfolio metric scan

## Why this playbook exists
Indie hackers run the entire pipeline alone — research, build, ship, market, support, and decide — under tight calendar constraints and often from a nomad schedule. Multi-product noise → one product that earns the next week's attention. This playbook turns that ambition into a sequenced set of stages with explicit decision gates so the founder doesn't confuse motion for progress and doesn't keep paying for products that quietly stopped working.

## What changes after running it
20-minute check across all live side-projects: which moved on MRR, signups, or traffic — pick the one product that earns next week's attention, and tag the rest for maintenance only.

## Stage flow
### Collect
All product metrics in one place in under 10 minutes.

**Tasks**
- Pull MRR, signups, and traffic for each product
- Compare against the previous 4-week median
- Flag any anomaly worth investigating

**Decision gate**
> Advance once every product has fresh numbers.

### Triage
RICE the products and pick a winner.

**Tasks**
- Score each product against a 4-factor RICE
- Pick the one with the strongest delta
- Tag the rest as 'maintenance only' for the week

**Decision gate**
> Advance only when a single winner is documented.

### Plan
Set the next week with one product in the foreground.

**Tasks**
- Define 3 outcomes for the winner
- Schedule maintenance windows for the rest
- Block the calendar accordingly

**Decision gate**
> Done once outcomes are in the calendar.

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
