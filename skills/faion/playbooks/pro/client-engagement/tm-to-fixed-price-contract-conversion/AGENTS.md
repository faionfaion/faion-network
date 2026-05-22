---
slug: tm-to-fixed-price-contract-conversion
tier: pro
group: client-engagement
persona: P4
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Engagement on T&M → client requests fixed-price for next phase → vendor lands a signed amendment without a margin haircut, with frozen requirements baseline, three-point estimate, risk reserves."
content_id: 4d41f578d17444e5
methodology_refs:
  - elicitation-techniques
  - requirements-prioritization
  - requirements-traceability
  - acceptance-criteria
  - strategy-analysis-current-state
  - solution-assessment
  - lessons-learned
  - risk-management
  - risk-register
  - procurement-management
  - cost-estimation
  - wbs-creation
  - schedule-development
  - quality-management
  - scope-management
  - stakeholder-engagement
  - earned-value-management
  - raci-matrix
  - tm-to-fp-conversion-playbook
  - vendor-margin-defense-checklist
  - change-control
  - communications-management
  - change-request-rate-card-template
  - scope-creep-management
  - statement-of-work
  - scoping-workshop
---

# T&M to fixed-price contract conversion (6 weeks)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

Engagement on T&M → client requests fixed-price for next phase → vendor lands a signed amendment without a margin haircut, with frozen requirements baseline, three-point estimate, risk reserves.

Six-week conversion sprint that runs in parallel to delivery. Daria leads the conversion from time-and-materials to fixed-price for phase 2. Output: requirements baseline frozen, three-point estimate with risk reserves, defensible commercial proposal, signed contract amendment. Margin floor protected.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Phase-2 scope freeze

**Intent:** Lock the requirements before pricing them.

**Tasks**
- Elicitation interviews on phase-2 outcomes
- Prioritise requirements (MoSCoW / RICE)
- Trace each requirement to phase-1 context where applicable
- Validate scope with client PM + sponsor; capture written sign-off

**Outputs**
- Requirements doc v2 with priorities
- Acceptance criteria matrix
- Sign-off record

**Decision gate**

Advance when client PM signs off requirements doc v2 in writing. Verbal nods do not count.

### Stage 2 — Solution + risk

**Intent:** Assess solution options and their risk envelope.

**Tasks**
- Solution assessment: build vs buy vs hybrid
- Lessons-learned from phase-1 incorporated into phase-2 risk register
- Risk register stacked with named owners
- Procurement exposure mapped (licenses, sub-contractors)

**Outputs**
- Solution-assessment memo
- Risk register v2
- Procurement exposure log

**Decision gate**

Advance once risks have named owners + mitigations. Risks without owners stay open and block.

### Stage 3 — Estimate + commercial

**Intent:** Cost the work, defend the margin, draft the commercial pitch.

**Tasks**
- WBS to leaf level for phase 2
- Three-point estimate (P50/P80/P95)
- Schedule with milestone payment points
- Quality-management plan
- Earned-value tracking points
- Draft commercial proposal (one-pager)

**Outputs**
- WBS + estimate sheet
- Schedule with payment points
- Quality-management plan
- Commercial proposal draft

**Decision gate**

Advance when P80 + reserves clears the margin floor. If not, scope-cut first, then re-price.

### Stage 4 — Change-control hardening

**Intent:** Wire up the guard rails BEFORE you sign fixed-price.

**Tasks**
- Communications-management plan tailored to fixed-price ops
- Change-control workflow with daily SLA
- Change-request rate card (for in-flight requests)
- Stakeholder engagement plan for the next 6 months

**Outputs**
- Comms plan
- Change-control workflow doc
- Rate card

**Decision gate**

Advance when the change-control workflow is co-signed by client PM.

### Stage 5 — Negotiation + signature

**Intent:** Close the amendment without giving the margin back.

**Tasks**
- Internal red-team challenge
- Run client negotiation (pricing, payment terms, acceptance criteria)
- Capture lessons-learned for the next conversion
- File signed amendment + run kickoff communication

**Outputs**
- Red-team notes
- Signed amendment
- Lessons-learned

**Decision gate**

Sign only with margin floor cleared AND change-control wired up. Walk if the client wants neither.

## Common pitfalls

- Converting without freezing the requirements — guaranteed margin loss
- Letting the client treat the amendment as a renegotiation of phase 1
- Skipping the rate card — every change request becomes a fight

## Quality checklist

- Did we lock requirements BEFORE we priced them?
- Could we defend the margin to our CFO without flinching?
- Did we agree the change-control workflow in writing, with rates?

## Related playbooks

- `statement-of-work`
- `scoping-workshop`
- `scope-creep-management`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `tm-to-fp-conversion-playbook` (blocks stage 3)
- `vendor-margin-defense-checklist` (blocks stage 3)
- `change-request-rate-card-template` (blocks stage 4)
- `scope-creep-management` (blocks stage 4)
- `statement-of-work` (blocks stage 5)
- `scoping-workshop` (blocks stage 5)
