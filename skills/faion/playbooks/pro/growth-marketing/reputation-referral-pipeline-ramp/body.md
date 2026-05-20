# Reputation + referral pipeline ramp (90-day flywheel)

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** global

## Why this playbook exists

Build a system that compounds: every closed engagement produces a testimonial + a referral + a public artefact, so by day 90 inbound covers >=50% of new pipeline and outbound effort drops.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Define the loop

**Intent:** Map the loop: every closed engagement → testimonial + referral + artefact.

**Tasks**
- Sketch the 3-output loop diagram
- Define triggers + handoffs
- Identify automation points

**Outputs**
- Loop diagram
- Trigger / handoff doc

**Decision gate**

Advance once loop is documented and at least one past engagement has been retrofitted.

### Stage 2 — Build harvest SOPs

**Intent:** Turn the loop into repeatable SOPs.

**Tasks**
- Write testimonial-harvest script
- Write referral-ask script
- Write public-artefact (case study) checklist

**Outputs**
- 3 SOPs
- Template library

**Decision gate**

Advance once SOPs run end-to-end on one closed engagement.

### Stage 3 — Distribute proof

**Intent:** Surface testimonials + case studies where buyers look.

**Tasks**
- Publish case study + LinkedIn version + newsletter version
- Add testimonials to landing page above the fold
- Schedule social-rotation of evergreen artefacts

**Outputs**
- Case study live
- Testimonials on landing
- Social rotation calendar

**Decision gate**

Advance once distribution surface covers landing + LinkedIn + newsletter.

### Stage 4 — Referral + partner

**Intent:** Activate referral incentive + partner swaps.

**Tasks**
- Design referral incentive (cash, hours, or trade)
- Identify 5 swap partners (non-competing peers)
- Set up intake qualification for inbound

**Outputs**
- Referral program doc
- Partner swap agreements
- Inbound intake form

**Decision gate**

Advance once inbound covers ≥50% of new pipeline over 30 days.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `testimonial-harvest-sop` (stage 2) — Stage 2 (Build harvest SOPs) references this; no methodology exists yet.
- `freelance-referral-program-design` (stage 4) — Stage 4 (Referral + partner) references this; no methodology exists yet.
- `inbound-intake-qualification` (stage 4) — Stage 4 (Referral + partner) references this; no methodology exists yet.
- `partner-swap-deal-template` (stage 4) — Stage 4 (Referral + partner) references this; no methodology exists yet.
- `business-storytelling` (stage 2) — Stage 2 (Build harvest SOPs) cites solo/marketing/content-marketer/business-storytelling but path does not resolve under KNOWLEDGE_ROOT.
- `growth-linkedin-strategy` (stage 3) — Stage 3 (Distribute proof) cites pro/marketing/smm-manager/growth-linkedin-strategy but path does not resolve under KNOWLEDGE_ROOT.
- `ops-automation-workflow` (stage 3) — Stage 3 (Distribute proof) cites solo/dev/automation-tooling/ops-automation-workflow but path does not resolve under KNOWLEDGE_ROOT.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
