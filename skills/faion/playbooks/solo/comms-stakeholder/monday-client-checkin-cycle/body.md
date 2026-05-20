# Monday client check-in cycle (one per active client)

**Persona:** P3 Technical Freelancer · **Tier:** solo · **Complexity:** light · **Angle:** atomic

## Why this playbook exists

Each active client receives a 5-10 min status note before noon Monday: what shipped last week, what's next, blockers, expected hours. Done = all active clients pinged, replies tracked, week's plan adjusted.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Prepare

**Intent:** By Sunday evening, draft Monday updates per active client.

**Tasks**
- List active clients
- Per client: collect last-week shipped + this-week plan + blockers
- Draft 5-10 min status note per client

**Outputs**
- Draft updates per client (4-line max)

**Decision gate**

Advance once every active client has a draft. No blanks.

### Stage 2 — Send

**Intent:** All updates out before noon Monday.

**Tasks**
- Send updates via each client's preferred channel
- Set reply tracking

**Outputs**
- Updates sent log

**Decision gate**

Advance once 100% of active clients pinged before noon.

### Stage 3 — Adapt

**Intent:** Use replies to adjust this week's plan.

**Tasks**
- Triage replies by urgency
- Re-order this week's task list
- Log new blockers in personal CRM

**Outputs**
- Updated weekly plan
- CRM entry per client

**Decision gate**

Cycle closes only after every reply is acknowledged within 24h.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `solo-monday-update-template` (stage 1) — Stage 1 (Prepare) references this; no methodology exists yet.
- `freelancer-personal-crm-minimal` (stage 3) — Stage 3 (Adapt) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
