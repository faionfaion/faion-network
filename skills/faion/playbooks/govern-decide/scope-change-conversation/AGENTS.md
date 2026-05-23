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

## When to use this playbook

This is a light-complexity atomic-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

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
