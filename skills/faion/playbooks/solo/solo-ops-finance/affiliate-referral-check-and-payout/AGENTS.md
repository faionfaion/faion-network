---
slug: affiliate-referral-check-and-payout
tier: solo
group: solo-ops-finance
persona: P2
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Affiliate dashboard noise → monthly clean payouts and a message to top referrers.
content_id: 1b082c0c4310985c
methodology_refs:
  - ops-dashboard-setup
  - ops-financial-planning
  - affiliate-program-solo
  - referral-ledger
  - growth-customer-testimonials
  - growth-community-building
---

# Affiliate / referral check and payout

## Why this playbook exists
Indie hackers run the entire pipeline alone — research, build, ship, market, support, and decide — under tight calendar constraints and often from a nomad schedule. Affiliate dashboard noise → monthly clean payouts and a message to top referrers. This playbook turns that ambition into a sequenced set of stages with explicit decision gates so the founder doesn't confuse motion for progress and doesn't keep paying for products that quietly stopped working.

## What changes after running it
Monthly one-hour ritual: pull affiliate and referral stats, approve commissions, process payouts, and send a personal thank-you message to top referrers so the program compounds.

## Stage flow
### Pull
All referral and affiliate stats in one table.

**Tasks**
- Pull data from referral platform
- Cross-reference with Stripe payouts
- Flag anomalies (no signups but high traffic, etc.)

**Decision gate**
> Advance once stats reconcile against revenue.

### Pay
Payouts processed within the month.

**Tasks**
- Approve commissions in the platform
- Trigger payouts via Stripe or bank
- Log each payout in the runway calculator

**Decision gate**
> Advance only after all payouts are confirmed.

### Thank
Top referrers feel personally seen.

**Tasks**
- Pick top 5 referrers by paid revenue driven
- Send a personal message with stats
- Invite them to share testimonials

**Decision gate**
> Done once all 5 receive a personal note.

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
