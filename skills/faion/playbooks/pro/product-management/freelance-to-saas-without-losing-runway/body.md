# Freelancer-to-SaaS transition without losing the runway

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** deep · **Angle:** synthesis

## Why this playbook exists

From a stable freelance income, validate and ship a SaaS product on the side, then taper client work month-by-month according to MRR triggers — without dropping below 6-month runway at any point.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Runway baseline

**Intent:** Set the minimum acceptable runway; never cross it.

**Tasks**
- Calculate current runway
- Set floor (e.g. 6 months)
- Define MRR triggers for each taper step

**Outputs**
- Runway dashboard
- Floor + triggers doc

**Decision gate**

Advance only with explicit floor + trigger rules written.

### Stage 2 — Validate + scope

**Intent:** Confirm the SaaS pain is real and scope is tight.

**Tasks**
- Use Mom Test interviews on 10 prospects
- Run idea-validation landing page
- Cut scope to ugliest first version

**Outputs**
- Validated pain note
- Landing page conversion data
- Cut scope doc

**Decision gate**

Advance only when landing converts ≥5% AND interviews confirm pain.

### Stage 3 — Dual-track ship

**Intent:** Ship SaaS in fixed weekly hours; keep client cadence intact.

**Tasks**
- Set fixed time-box per week for product work
- Move repeat clients to retainer to stabilize
- Ship v1 to first design partners

**Outputs**
- Weekly time-allocation log
- Retainer conversions
- v1 deployed

**Decision gate**

Advance only when product time-box held for 8 straight weeks without missed client deliverables.

### Stage 4 — Taper

**Intent:** Drop client hours as MRR hits triggers; keep runway above floor.

**Tasks**
- Hit MRR trigger 1: drop 1 client
- Hit MRR trigger 2: drop another or shift to retainer-only
- Each step: verify runway still above floor

**Outputs**
- MRR / runway / client-roster log per month

**Decision gate**

Never cross the runway floor. If approaching, pause taper and ramp client work back.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `freelance-to-saas-runway-gates` (stage 1) — Stage 1 (Runway baseline) references this; no methodology exists yet.
- `minimum-acceptable-rate-floor` (stage 1) — Stage 1 (Runway baseline) references this; no methodology exists yet.
- `dual-track-context-switching-discipline` (stage 3) — Stage 3 (Dual-track ship) references this; no methodology exists yet.
- `time-allocation-ratio-by-runway` (stage 3) — Stage 3 (Dual-track ship) references this; no methodology exists yet.
- `retainer-conversion-from-project-client` (stage 3) — Stage 3 (Dual-track ship) references this; no methodology exists yet.
- `mrr-trigger-client-taper-plan` (stage 4) — Stage 4 (Taper) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
