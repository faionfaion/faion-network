# Invoice send + chase-up

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

Monthly invoice run. Done = invoices out by 1st, payment received by 15th, late ones escalated by 30th without burning the relationship.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Send

**Intent:** Invoices out by the 1st of the month.

**Tasks**
- Generate invoices from time tracker / milestones
- Verify VAT / tax fields
- Send via preferred channel

**Outputs**
- Invoices sent log

**Decision gate**

Advance only when all active clients invoiced by EOD on the 1st.

### Stage 2 — Track + nudge

**Intent:** Friendly day-7 nudge; firm day-15 reminder.

**Tasks**
- Set day-7 + day-15 reminders per invoice
- Send polite chase-up on day-7
- Send firmer reminder on day-15

**Outputs**
- Chase-up log

**Decision gate**

Advance once payment received OR escalation triggered.

### Stage 3 — Escalate

**Intent:** Day-30 escalation without burning the relationship.

**Tasks**
- Apply late fee per contract
- Pause new work until paid (per clause)
- Log incident in client scorecard

**Outputs**
- Late fee invoice
- Pause notice
- Lesson logged

**Decision gate**

Escalation closes only when paid OR engagement formally suspended.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `freelancer-payment-chase-script-library` (stage 2) — Stage 2 (Track + nudge) references this; no methodology exists yet.
- `solo-late-fee-and-pause-clause-template` (stage 3) — Stage 3 (Escalate) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
