---
slug: annual-planning-and-financial-close-v2
tier: pro
group: micro-agency
persona: p5-micro-agency-founder
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Run an annual planning cycle that closes the books, files taxes, sets next-year revenue / margin / hiring targets, locks the service portfolio, and surfaces compliance risks before they bite.
content_id: 5350fe782f0a7c2c
methodology_refs:
  - privacy-compliance
  - growth-brand-positioning
  - growth-gtm-strategy
  - ops-annual-planning-process
  - ops-annual-planning-templates
  - ops-contractor-management
  - ops-financial-basics
  - ops-legal-basics
  - ops-legal-compliance
  - ops-legal-compliance-checklist
  - ops-partnership-strategy
  - ops-tax-basics
  - ops-tax-compliance
  - predictive-analytics-pm
  - risk-management
  - risk-register
  - portfolio-strategy
  - risk-assessment
  - trend-analysis
---

# Annual planning and financial close (6–8 weeks, Q4 cycle)

## Context

Run an annual planning cycle that closes the books, files taxes, sets next-year revenue / margin / hiring targets, locks the service portfolio, and surfaces compliance risks before they bite.

## Outcome

By the end of this playbook, the operator has run the 5 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 5 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Close the Books

Get last-year's numbers final and clean.

Tasks:
- Reconcile all invoices, expenses, and contractor payouts
- Run end-of-year tax-and-legal close with your accountant
- Lock the books and snapshot the P&L

Outputs:
- reconciled ledger
- tax+legal close memo
- locked P&L

Decision gate: Advance only when books are closed and P&L is signed off.

### 2. Compute Capacity & Margin

Know what you actually have to invest.

Tasks:
- Compute capacity in billable hours and ICP-day-rate
- Compute net margin per offering and per client
- Decide which offerings to grow, hold, or drop

Outputs:
- capacity model
- margin-by-offering table
- grow/hold/drop list

Decision gate: Advance when every offering has a documented grow/hold/drop call.

### 3. Set Annual Plan

Outcomes, not vibes.

Tasks:
- Set 3-5 annual outcomes with measurable targets
- Cascade outcomes into quarterly milestones
- Pre-commit capacity and budget per outcome

Outputs:
- annual plan doc
- quarterly milestones
- outcome-to-capacity map

Decision gate: Advance when every outcome has a quarterly milestone and budgeted capacity.

### 4. Re-price & Renew

New year, new pricing.

Tasks:
- Decide which clients get a rate adjustment this quarter
- Send adjustment notices with enough notice to be fair
- Sign renewed retainers / scopes at the new rates

Outputs:
- adjustment plan
- sent notices
- signed renewals

Decision gate: Advance only when adjustment notices are out AND renewals start landing.

### 5. Kickoff & Communicate

Tell the team and clients what changed.

Tasks:
- Hold the all-hands annual kickoff covering plan and changes
- Send client newsletter or 1:1s with anything that affects them
- Set the quarterly review cadence on the calendar

Outputs:
- kickoff deck
- client comms log
- quarterly review calendar

Decision gate: Required output: every active client has been told what changed.

## Decision points

- Stage 1 (Close the Books): Advance only when books are closed and P&L is signed off.
- Stage 2 (Compute Capacity & Margin): Advance when every offering has a documented grow/hold/drop call.
- Stage 3 (Set Annual Plan): Advance when every outcome has a quarterly milestone and budgeted capacity.
- Stage 4 (Re-price & Renew): Advance only when adjustment notices are out AND renewals start landing.
- Stage 5 (Kickoff & Communicate): Required output: every active client has been told what changed.

## References

- `privacy-compliance`
- `growth-brand-positioning`
- `growth-gtm-strategy`
- `ops-annual-planning-process`
- `ops-annual-planning-templates`
- `ops-contractor-management`
- `ops-financial-basics`
- `ops-legal-basics`
- `ops-legal-compliance`
- `ops-legal-compliance-checklist`
- `ops-partnership-strategy`
- `ops-tax-basics`
- `ops-tax-compliance`
- `predictive-analytics-pm`
- `risk-management`
- `risk-register`
- `portfolio-strategy`
- `risk-assessment`
- `trend-analysis`

Gaps (status: draft until empty):
- `agency-year-end-close-checklist` (see `gaps[]` in `playbook.yaml`)
- `us-uk-eu-compliance-matrix` (see `gaps[]` in `playbook.yaml`)
- `agency-annual-plan-template` (see `gaps[]` in `playbook.yaml`)
- `agency-risk-register-template` (see `gaps[]` in `playbook.yaml`)
