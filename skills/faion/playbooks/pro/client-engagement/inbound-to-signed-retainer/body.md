# Inbound-to-signed-retainer in one client cycle

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** synthesis

## Why this playbook exists

From a cold inbound DM/email to a countersigned monthly retainer with first invoice paid, run a deterministic pipeline that filters bad-fit clients early, prices the engagement defensively, and locks payment terms before any work starts.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Triage

**Intent:** Score inbound; reject bad-fit fast.

**Tasks**
- Apply triage scoring rubric to the inbound message
- Disqualify if any red flag hit
- Schedule discovery only with qualified leads

**Outputs**
- Triage score
- Scheduled call OR polite decline

**Decision gate**

Advance only with explicit score and decision documented.

### Stage 2 — Discovery

**Intent:** Run discovery using Mom Test; emerge with hypothesis.

**Tasks**
- Run discovery call
- Capture pain + budget + decision-maker access
- Write hypothesis note

**Outputs**
- Call notes
- Hypothesis note

**Decision gate**

Advance only if discovery confirms budget + decision-maker access.

### Stage 3 — Propose + price

**Intent:** Send a retainer proposal with defensive pricing and anchoring.

**Tasks**
- Pick fixed vs hourly vs retainer
- Compute price using rate floor + risk uplift
- Send 3-option anchored proposal

**Outputs**
- Retainer proposal sent
- Pricing rationale

**Decision gate**

Advance only when proposal includes deposit + 3 anchored options.

### Stage 4 — Negotiate + sign

**Intent:** Handle redlines; close with deposit before any work.

**Tasks**
- Walk through redlines on a call
- Lock contract clauses (IP, termination, payment terms)
- Collect deposit before kickoff

**Outputs**
- Countersigned retainer
- Deposit landed

**Decision gate**

Cycle closes only when deposit clears. No deposit, no kickoff.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `inbound-lead-triage-scoring` (stage 1) — Stage 1 (Triage) references this; no methodology exists yet.
- `bad-fit-disqualification-script` (stage 1) — Stage 1 (Triage) references this; no methodology exists yet.
- `hourly-rate-floor-calculation` (stage 3) — Stage 3 (Propose + price) references this; no methodology exists yet.
- `retainer-pricing-methodology` (stage 3) — Stage 3 (Propose + price) references this; no methodology exists yet.
- `fixed-vs-hourly-decision-framework` (stage 3) — Stage 3 (Propose + price) references this; no methodology exists yet.
- `proposal-from-discovery-template` (stage 3) — Stage 3 (Propose + price) references this; no methodology exists yet.
- `three-option-pricing-anchoring` (stage 3) — Stage 3 (Propose + price) references this; no methodology exists yet.
- `solo-freelancer-contract-clauses` (stage 4) — Stage 4 (Negotiate + sign) references this; no methodology exists yet.
- `redline-and-pricing-objection-handling` (stage 4) — Stage 4 (Negotiate + sign) references this; no methodology exists yet.
- `deposit-before-work-policy` (stage 4) — Stage 4 (Negotiate + sign) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
