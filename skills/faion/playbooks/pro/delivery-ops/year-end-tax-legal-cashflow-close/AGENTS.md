---
slug: year-end-tax-legal-cashflow-close
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
summary: "Across 4-6 weeks at year-end: close books, file taxes / VAT correctly across jurisdictions, refresh contracts + insurance, and publish a yearly retrospective that doubles as a marketing asset."
content_id: a471b223cb95b2ad
methodology_refs:
  - data-analysis
  - ops-financial-basics
  - ops-financial-planning
  - ops-tax-basics
  - ops-tax-compliance
  - ops-legal-compliance
  - ops-legal-compliance-checklist
  - cross-border-tax-cheatsheet
  - ops-legal-basics
  - ops-contractor-management
  - ops-partnership-strategy
  - freelance-insurance-buyers-guide
  - freelancer-year-end-checklist
  - ops-annual-planning-templates
  - portfolio-strategy
  - okr-setting
  - business-storytelling
  - growth-content-marketing
  - growth-newsletter-growth
  - growth-indiehackers-strategy
  - year-in-review-as-marketing
---

# Year-end tax, legal, and cash-flow close

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** global

## Why this playbook exists

Across 4-6 weeks at year-end: close books, file taxes / VAT correctly across jurisdictions, refresh contracts + insurance, and publish a yearly retrospective that doubles as a marketing asset.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Close books

**Intent:** Reconcile every invoice + expense for the calendar year.

**Tasks**
- Pull bank + Stripe + invoice ledger
- Reconcile against P&L
- Categorise expenses for tax

**Outputs**
- Reconciled P&L
- Expense categories spreadsheet

**Decision gate**

Advance only after books reconcile to the cent.

### Stage 2 — Taxes + VAT

**Intent:** File correctly across every jurisdiction with no surprises.

**Tasks**
- Confirm tax residency + obligations
- Compute estimated tax + VAT/GST
- Engage accountant for review

**Outputs**
- Tax computation worksheet
- Accountant review note
- Filings submitted

**Decision gate**

Advance only after filings are submitted, not just drafted.

### Stage 3 — Contracts + insurance

**Intent:** Refresh client contracts + liability/E&O insurance for the new year.

**Tasks**
- Audit each active contract for outdated terms
- Renew or shop insurance policies
- Send revised MSA to long-term clients

**Outputs**
- Updated MSAs
- Renewed insurance
- Compliance checklist signed

**Decision gate**

Advance once all contracts are current. No expired terms carrying into new year.

### Stage 4 — Year-in-review as marketing

**Intent:** Publish a transparent annual retrospective; turn close into a marketing asset.

**Tasks**
- Draft retrospective: revenue, lessons, projects shipped
- Edit for narrative + share-worthy hooks
- Publish on blog + newsletter + LinkedIn

**Outputs**
- Published retrospective post
- Newsletter sent
- Social distribution

**Decision gate**

Required artifact: published post. Internal-only retros don't count.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `cross-border-tax-cheatsheet` (stage 2) — Stage 2 (Taxes + VAT) references this; no methodology exists yet.
- `freelance-insurance-buyers-guide` (stage 3) — Stage 3 (Contracts + insurance) references this; no methodology exists yet.
- `freelancer-year-end-checklist` (stage 3) — Stage 3 (Contracts + insurance) references this; no methodology exists yet.
- `year-in-review-as-marketing` (stage 4) — Stage 4 (Year-in-review as marketing) references this; no methodology exists yet.
- `ops-financial-planning` (stage 1) — Stage 1 (Close books) cites solo/marketing/growth-marketer/ops-financial-planning but path does not resolve under KNOWLEDGE_ROOT.
- `okr-setting` (stage 4) — Stage 4 (Year-in-review as marketing) cites pro/product/product-planning/okr-setting but path does not resolve under KNOWLEDGE_ROOT.
- `business-storytelling` (stage 4) — Stage 4 (Year-in-review as marketing) cites solo/marketing/content-marketer/business-storytelling but path does not resolve under KNOWLEDGE_ROOT.
- `growth-indiehackers-strategy` (stage 4) — Stage 4 (Year-in-review as marketing) cites solo/marketing/growth-marketer/growth-indiehackers-strategy but path does not resolve under KNOWLEDGE_ROOT.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.

## When to use this playbook

This is a medium-complexity global-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

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
