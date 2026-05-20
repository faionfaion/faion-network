# Portfolio site update with new case study

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

A project closes successfully → add a case study to portfolio site within 2 weeks while context is fresh. Done = published case study with metrics, client quote (if NDA permits), and shareable link queued into social rotation.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Capture context

**Intent:** Within 2 weeks of close, capture metrics + quote while fresh.

**Tasks**
- Pull metrics: before / after / impact
- Schedule 20-min testimonial call with client
- Confirm what's NDA-safe to publish

**Outputs**
- Metrics doc
- Testimonial recording
- NDA-safe list

**Decision gate**

Advance only with both metrics and a client quote secured.

### Stage 2 — Write + design

**Intent:** Draft a one-page case study with clear hook.

**Tasks**
- Draft using STAR (Situation Task Action Result) structure
- Add visuals: screenshots, charts, before/after
- Internal review for clarity + NDA compliance

**Outputs**
- Case study draft
- Visual assets

**Decision gate**

Advance only after a peer reviewer says hook is clear within 30s.

### Stage 3 — Publish + distribute

**Intent:** Push to portfolio + LinkedIn + Twitter rotation.

**Tasks**
- Publish to portfolio site
- Schedule LinkedIn long-form post
- Queue Twitter thread + future re-rotation

**Outputs**
- Live case study URL
- Social posts scheduled

**Decision gate**

Cycle closes only when case study URL is live + social queue contains it.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `solo-testimonial-extraction-script` (stage 1) — Stage 1 (Capture context) references this; no methodology exists yet.
- `freelancer-case-study-template` (stage 2) — Stage 2 (Write + design) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
