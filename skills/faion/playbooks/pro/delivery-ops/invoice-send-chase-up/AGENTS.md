---
slug: invoice-send-chase-up
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
summary: Monthly invoice run. Done = invoices out by 1st, payment received by 15th, late ones escalated by 30th without burning the relationship.
content_id: b8c92a7a125e2311
methodology_refs:
  - ops-financial-basics
  - ops-legal-compliance
  - ops-legal-compliance-checklist
  - ops-tax-basics
  - difficult-conversations
  - freelancer-payment-chase-script-library
  - lessons-learned
  - negotiation
  - solo-late-fee-and-pause-clause-template
---

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
