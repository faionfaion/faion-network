# Project kickoff to handover (typical 6-12 week engagement)

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

From signed SOW to client-accepted final deliverable, with the freelancer running solo across discovery, build, and ship — no scope creep, weekly invoices paid on time, written handover + warranty period defined.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Kickoff & discovery

**Intent:** Align stakeholders, lock scope baseline, set communication cadence.

**Tasks**
- Run kickoff workshop with named stakeholders
- Document elicited requirements + acceptance criteria
- Publish weekly cadence calendar

**Outputs**
- Stakeholder register
- Requirements doc v1
- Weekly cadence published

**Decision gate**

Advance once stakeholders sign off on requirements + cadence. No scope ambiguity beyond known unknowns.

### Stage 2 — Plan & spec

**Intent:** Translate requirements into a delivery plan with milestones tied to invoices.

**Tasks**
- Break work into 1-2 week milestones
- Map acceptance criteria to every milestone
- Lock MVP scope; defer the rest

**Outputs**
- Milestone plan with invoice points
- Acceptance criteria matrix

**Decision gate**

Advance once milestones + invoice points are agreed. Push back on any scope adds.

### Stage 3 — Build & ship

**Intent:** Deliver milestones on a weekly cadence; invoice on completion.

**Tasks**
- Ship one milestone per week
- Send weekly status with shipped/blocked/next
- Invoice on milestone acceptance

**Outputs**
- Deployed milestones
- Weekly status notes
- Paid invoices

**Decision gate**

Advance to next milestone only after current is signed-off. If two slipped, escalate.

### Stage 4 — Handover & warranty

**Intent:** Package deliverables, hand off, define warranty window, harvest testimonial.

**Tasks**
- Publish handover package (code, docs, credentials)
- Walk client through usage; record session
- Define 30-day warranty terms in writing

**Outputs**
- Handover package URL
- Walkthrough recording
- Warranty doc
- Testimonial captured

**Decision gate**

Engagement closes only after handover doc accepted and final invoice paid.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `scope-creep-firewall` (stage 3) — Stage 3 (Build & ship) references this; no methodology exists yet.
- `freelance-weekly-invoice-cadence` (stage 3) — Stage 3 (Build & ship) references this; no methodology exists yet.
- `client-handover-package` (stage 4) — Stage 4 (Handover & warranty) references this; no methodology exists yet.
- `warranty-period-sop` (stage 4) — Stage 4 (Handover & warranty) references this; no methodology exists yet.
- `mvp-scoping` (stage 2) — Stage 2 (Plan & spec) cites pro/product/product-planning/mvp-scoping but path does not resolve under KNOWLEDGE_ROOT.
- `release-planning` (stage 2) — Stage 2 (Plan & spec) cites pro/product/product-planning/release-planning but path does not resolve under KNOWLEDGE_ROOT.
- `ops-automation-workflow` (stage 3) — Stage 3 (Build & ship) cites solo/dev/automation-tooling/ops-automation-workflow but path does not resolve under KNOWLEDGE_ROOT.
- `ops-dashboard-setup` (stage 3) — Stage 3 (Build & ship) cites solo/dev/automation-tooling/ops-dashboard-setup but path does not resolve under KNOWLEDGE_ROOT.
- `continuous-delivery` (stage 3) — Stage 3 (Build & ship) cites solo/dev/software-developer/continuous-delivery but path does not resolve under KNOWLEDGE_ROOT.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.

## When to use this playbook

This is a deep-complexity global-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

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
