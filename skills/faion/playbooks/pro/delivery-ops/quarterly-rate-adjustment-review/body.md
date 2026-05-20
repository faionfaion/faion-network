# Quarterly rate adjustment review

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

Every 90 days, decide whether to raise rates, with whom, and by how much. Done = rate decision matrix updated, raise-letters drafted for eligible clients, new prospect quotes adjusted.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Data pull

**Intent:** Gather utilization, pipeline, market rate, and client scorecard.

**Tasks**
- Pull billable utilization for the quarter
- Pull pipeline pressure: backlog + waitlist
- Survey market-rate signal for your niche

**Outputs**
- Utilization report
- Pipeline snapshot
- Market-rate notes

**Decision gate**

Advance only with quantitative inputs, not vibes.

### Stage 2 — Decide raises

**Intent:** Pick whom to raise, by how much, and when.

**Tasks**
- Score each client on raise-eligibility (relationship, contract length, growth)
- Pick raise %
- Set effective dates

**Outputs**
- Rate decision matrix

**Decision gate**

Advance only when each client has a decision (raise / hold / drop).

### Stage 3 — Draft + send

**Intent:** Send raise-letters; quote new prospects at new rate.

**Tasks**
- Draft personalised raise-letter per eligible client
- Send with notice period
- Update all proposal templates to new rate

**Outputs**
- Raise-letters sent
- Updated proposal templates

**Decision gate**

Cycle closes only when letters are sent and templates updated.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `solo-utilization-and-pipeline-dashboard` (stage 1) — Stage 1 (Data pull) references this; no methodology exists yet.
- `freelancer-rate-raise-letter-template` (stage 3) — Stage 3 (Draft + send) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
