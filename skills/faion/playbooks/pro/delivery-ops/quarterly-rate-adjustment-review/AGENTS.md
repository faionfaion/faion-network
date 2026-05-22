---
slug: quarterly-rate-adjustment-review
tier: pro
group: delivery-ops
persona: P3
goal: operate-ritual
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Every 90 days, decide whether to raise rates, with whom, and by how much. Done = rate decision matrix updated, raise-letters drafted for eligible clients, new prospect quotes adjusted.
content_id: 15964fd12cd1e268
methodology_refs:
  - competitive-intelligence
  - market-research-tam-sam-som
  - solo-utilization-and-pipeline-dashboard
  - ops-financial-basics
  - cost-estimation
  - risk-management
  - difficult-conversations
  - negotiation
  - selling-ideas
  - freelancer-rate-raise-letter-template
---

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
