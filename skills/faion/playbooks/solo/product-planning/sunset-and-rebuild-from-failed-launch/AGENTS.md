---
slug: sunset-and-rebuild-from-failed-launch
tier: solo
group: product-planning
persona: P2
goal: govern-decide
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Failed launch → clean shutdown plus a sharper next-bet plan in 30 days.
content_id: d800c5257bb76f90
methodology_refs:
  - jobs-to-be-done
  - problem-validation-2026
  - user-interviews
  - mom-test
  - storytelling
  - ops-customer-support
  - sunset-customer-comms-template
  - growth-content-marketing
  - growth-twitter-x-growth
  - one-command-dev-env-template
  - product-lifecycle
  - asset-harvest-checklist
  - growth-indiehackers-strategy
  - feedback-management
  - idea-generation
  - indie-postmortem-template
  - feature-prioritization-rice
  - niche-evaluation
  - ops-financial-planning
  - anti-roadmap-template
  - weekly-pm-async-broadcast-template
---

# Sunset and rebuild from a failed launch

## Why this playbook exists
Indie hackers run the entire pipeline alone — research, build, ship, market, support, and decide — under tight calendar constraints and often from a nomad schedule. Failed launch → clean shutdown plus a sharper next-bet plan in 30 days. This playbook turns that ambition into a sequenced set of stages with explicit decision gates so the founder doesn't confuse motion for progress and doesn't keep paying for products that quietly stopped working.

## What changes after running it
Turn a missed launch into a clean shutdown plus a sharper next-bet plan: refund/migrate users, harvest learnings publicly, recycle assets, and decide on rebuild vs pivot vs walk away with an explicit rationale.

## Stage flow
### Assess
Make the failure crisp with numbers and quotes.

**Tasks**
- Re-run the success metrics against the actual launch
- Collect 5 user quotes on why the product missed
- Distinguish problem-fit failure vs distribution failure

**Decision gate**
> Advance when failure mode is named in one sentence.

### Sunset Comms
Users hear it from you first, with a clear path.

**Tasks**
- Send a sunset email with refund or migration path
- Publish a public retro on IH and X
- Process refunds within 14 days

**Decision gate**
> Advance only after all paying users have a confirmed status.

### Asset Harvest
Code, copy, audience, and infra survive even if the product does not.

**Tasks**
- Tag reusable components, prompts, and copy
- Migrate audience to an umbrella newsletter or handle
- Cut infra costs — pull the plug on unused services

**Decision gate**
> Advance once monthly infra costs are documented at the new baseline.

### Lessons
A public retro that builds trust and refines the next bet.

**Tasks**
- Write a 3-lesson postmortem ranked by stakes
- Frame the lessons in MoM-test language (no bragging)
- Invite reader replies — feed the next-bet idea pool

**Decision gate**
> Advance only once the retro is public and triaged.

### Next Bet
Choose rebuild, pivot, or retire with a documented rationale.

**Tasks**
- Score 3 candidate next bets using a quick RICE
- Run niche-evaluation on the top score
- Write the decision: rebuild / pivot / walk away

**Decision gate**
> Required output: explicit verdict. Pivot only with a fresh JTBD; walking away is valid.

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
