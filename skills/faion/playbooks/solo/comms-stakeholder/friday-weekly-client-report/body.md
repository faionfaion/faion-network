# Friday weekly client report

**Persona:** P3 Technical Freelancer · **Tier:** solo · **Complexity:** light · **Angle:** atomic

## Why this playbook exists

End-of-week recap to each active client: shipped / blocked / next, plus hours logged. Done = report sent, invoice draft updated, retainer-cap watch list refreshed.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Compile

**Intent:** Pull together shipped, blocked, next, hours.

**Tasks**
- Pull commits / tickets / time tracker
- Categorise into shipped / blocked / next
- Sum hours vs retainer cap

**Outputs**
- Raw weekly compile per client

**Decision gate**

Advance only when every active client has data ready.

### Stage 2 — Write report

**Intent:** Crisp shipped/blocked/next note with retainer-cap awareness.

**Tasks**
- Write 4-section report per client
- Highlight any retainer-cap risks
- Attach week-on-week metric trend if applicable

**Outputs**
- Weekly report per client

**Decision gate**

Report must include retainer-cap line. No exceptions.

### Stage 3 — Send + invoice

**Intent:** Send Friday before EOD; update invoice draft for month-end.

**Tasks**
- Send report through preferred channel
- Update draft invoice with this-week's hours
- Update watch list for caps near limit

**Outputs**
- Reports sent log
- Updated invoices
- Cap watch list

**Decision gate**

Cycle closes only when invoice drafts are current.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `solo-time-tracking-discipline` (stage 1) — Stage 1 (Compile) references this; no methodology exists yet.
- `freelancer-weekly-report-template` (stage 2) — Stage 2 (Write report) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
