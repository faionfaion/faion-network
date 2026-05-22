---
slug: product-hunt-comment-back-day
tier: solo
group: launch-operations
persona: P2
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: PH launch noise → every comment and DM answered within 24h, lurkers converted to signups.
content_id: e3b02d716b256aee
methodology_refs:
  - active-listening
  - growth-product-hunt-launch
  - feedback
  - ops-customer-support
  - growth-onboarding-emails
  - backlog-hygiene-cron-checklist
  - objection-bank
---

# Product Hunt comment-back day

## Why this playbook exists
Indie hackers run the entire pipeline alone — research, build, ship, market, support, and decide — under tight calendar constraints and often from a nomad schedule. PH launch noise → every comment and DM answered within 24h, lurkers converted to signups. This playbook turns that ambition into a sequenced set of stages with explicit decision gates so the founder doesn't confuse motion for progress and doesn't keep paying for products that quietly stopped working.

## What changes after running it
Launch-day or post-launch maintenance: respond to every Product Hunt comment and DM within the day, convert lurkers to signups, gather objections, and turn the comment thread into long-term social proof.

## Stage flow
### Triage
All inbound sorted by intent and urgency.

**Tasks**
- Filter comments by question / praise / objection
- Tag DMs by stage (curious / evaluating / blocking)
- Pin the open question or feature ask to the top of the thread

**Decision gate**
> Advance only when every comment has a tag.

### Respond
Personal, on-brand replies to every comment.

**Tasks**
- Write personal replies in batches, not template blasts
- Address each objection with concrete proof or roadmap link
- Escalate hot leads into DMs with offer

**Decision gate**
> Advance once 100% of comments have a response and ≥30% of replies push to signup.

### Archive
Comment day becomes lasting product intelligence.

**Tasks**
- Update the objection bank
- Add lurker DMs to nurture sequence
- Log new feature requests into the backlog

**Decision gate**
> Done once objections and backlog are committed.

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
