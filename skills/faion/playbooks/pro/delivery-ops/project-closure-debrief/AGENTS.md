---
slug: project-closure-debrief
tier: pro
group: delivery-ops
persona: P3
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Project hits final milestone or retainer ends. Done = handover artifacts delivered, final invoice settled, internal retro logged, referral/upsell motion triggered.
content_id: ec75274c41ea95ee
methodology_refs:
  - communications-management
  - procurement-management
  - project-closure
  - freelancer-handover-bundle-template
  - benefits-realization
  - lessons-learned
  - ops-customer-success-basics
  - ops-upselling-cross-selling
  - growth-customer-testimonials
  - solo-retainer-reactivation-cadence
---

# Project closure debrief + retrospective

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

Project hits final milestone or retainer ends. Done = handover artifacts delivered, final invoice settled, internal retro logged, referral/upsell motion triggered.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Handover

**Intent:** Deliver handover artifacts; settle final invoice.

**Tasks**
- Package code + docs + credentials
- Run a 30-min walkthrough
- Settle final invoice

**Outputs**
- Handover bundle
- Walkthrough recording
- Final invoice paid

**Decision gate**

Advance only after final invoice is paid.

### Stage 2 — Retro

**Intent:** Internal retro: what to repeat, what to fix.

**Tasks**
- Write win / loss / surprise notes
- Log lessons in personal patterns doc
- Flag SOPs to update

**Outputs**
- Retro doc
- Updated patterns library

**Decision gate**

Advance only with written retro. Mental-only doesn't count.

### Stage 3 — Reactivate

**Intent:** Trigger referral, upsell, or retainer-restart motion.

**Tasks**
- Ask for testimonial + referral
- Pitch upsell or retainer-restart if relevant
- Add to 90-day check-in cadence

**Outputs**
- Referral ask sent
- Upsell pitch (if relevant)
- Check-in scheduled

**Decision gate**

Cycle closes only when at least one of testimonial/referral/upsell is requested.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `freelancer-handover-bundle-template` (stage 1) — Stage 1 (Handover) references this; no methodology exists yet.
- `solo-retainer-reactivation-cadence` (stage 3) — Stage 3 (Reactivate) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.

## When to use this playbook

This is a medium-complexity atomic-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

## Anti-patterns to avoid

- Running the stages out of order because one feels more urgent. Order encodes risk: skipping earlier stages usually means absorbing risk in a later stage where the cost is higher.
- Treating outputs as optional. Every stage requires a written artifact — that artifact is what makes the next decision-gate verifiable.
- Letting the client write your scope, your timeline, or your contract clauses. The whole point of this playbook is that *you* run a deterministic pipeline; the client engages with the pipeline, not the other way around.
- Skipping the closure / retro step. The compounding value of running this playbook many times is in the lessons captured at the end. Without retros, you re-learn the same expensive lessons every quarter.

## Agent prompt hints

If you are routing this playbook through `faion get-content` for an agent:

- Ask the agent to produce *each* stage's outputs as named files before moving to the next stage. Reject hand-wave outputs.
- Have the agent state the decision-gate condition out loud after producing outputs, and pass the gate before continuing.
- For any gap in the methodology chain (see *Gaps in the methodology chain* above), the agent should explicitly mark its substitute approach so you can backfill the missing methodology later.
