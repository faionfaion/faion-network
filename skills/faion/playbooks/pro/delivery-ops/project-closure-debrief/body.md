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
