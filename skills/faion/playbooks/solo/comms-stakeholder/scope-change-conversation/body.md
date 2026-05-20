# Scope-change conversation when client says 'just one more thing'

**Persona:** P3 Technical Freelancer · **Tier:** solo · **Complexity:** light · **Angle:** atomic

## Why this playbook exists

Inbound request outside agreed scope. Done = either a written change order with new price/timeline, or a polite deferral to next sprint, with no silent absorption.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Triage

**Intent:** Decide whether ask is in-scope, change-order, or defer.

**Tasks**
- Re-read SOW
- Estimate effort delta
- Pick triage outcome

**Outputs**
- Triage decision note

**Decision gate**

Refuse to start work until triage outcome is written.

### Stage 2 — Talk

**Intent:** Have the conversation: change-order or graceful defer.

**Tasks**
- Open with what you heard them ask
- Present effort delta + price + timeline impact
- Land on change-order, defer, or no-thanks

**Outputs**
- Conversation outcome note

**Decision gate**

Required: a written outcome. No silent absorption.

### Stage 3 — Document

**Intent:** Get the change-order in writing.

**Tasks**
- Draft mini-contract or amendment
- Get countersignature before work starts
- Update project plan + invoice schedule

**Outputs**
- Countersigned change-order
- Updated plan

**Decision gate**

Work does not start until amendment is countersigned.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `freelancer-scope-change-script-library` (stage 2) — Stage 2 (Talk) references this; no methodology exists yet.
- `solo-change-order-mini-contract` (stage 3) — Stage 3 (Document) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
