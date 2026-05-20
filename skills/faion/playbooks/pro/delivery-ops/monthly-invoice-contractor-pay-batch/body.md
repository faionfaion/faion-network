# Monthly invoice + contractor pay batch

**Playbook slug:** `monthly-invoice-contractor-pay-batch`
**Tier:** pro
**Complexity:** light
**Persona:** P5 -- Micro-agency founder

## Intent

One sitting per month to all client invoices sent + all contractors paid + books reconciled.

## Scope

Founder issues all client invoices and pays all contractors in one batched session monthly. Output: invoices sent, contractors paid, books reconciled. Exit artifact: invoices list + contractor payment confirmations + reconciled books for the month.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Annual financial close - separate playbook
- Tax filing - separate cadence

### Prerequisites

- Bookkeeping + invoicing tooling live
- Contractor timesheets / deliverables captured

## Success criteria

The playbook is done when:
- All client invoices sent by first business day of month
- All contractors paid by 5th business day
- Books reconciled with bank
- Late payers flagged with follow-up date

## Stages

### Stage 1: Invoice clients

**Intent:** Send every invoice on the same day, no excuses.

**Tasks:**
- Pull retainer + project invoiceable lines
- Generate invoices
- Send via accounting tool

**Methodologies in chain:**
- `ops-financial-basics` -> `pro/marketing/gtm-strategist/ops-financial-basics`
- `ops-legal-compliance-checklist` -> `pro/marketing/gtm-strategist/ops-legal-compliance-checklist`
- `ops-tax-compliance` -> `pro/marketing/gtm-strategist/ops-tax-compliance`
- `ops-financial-planning` -> `solo/marketing/gtm-strategist/ops-financial-planning`

**Outputs:**
- Sent invoices list

**Decision gate:**
> Advance once 100% of invoices sent.

### Stage 2: Pay contractors

**Intent:** Approve, batch, send. Days, not weeks.

**Tasks:**
- Verify contractor invoices against deliverables
- Batch payments
- Confirm receipt + log

**Methodologies in chain:**
- `ops-contractor-management` -> `pro/marketing/gtm-strategist/ops-contractor-management`
- `cost-estimation` -> `pro/pm/project-manager/cost-estimation`

**Outputs:**
- Payments sent
- Receipt confirmations

**Decision gate:**
> Advance once all contractors paid within agreed terms.

### Stage 3: Reconcile + log

**Intent:** Books match bank; late payers tagged.

**Tasks:**
- Match invoices to deposits
- Tag late payers + schedule follow-ups
- Update KPI sheet

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Reconciliation note
- Late-payer log

**Decision gate:**
> Required: books reconciled within 48h of batch.

## Common pitfalls

- Sending invoices the day each project finishes - never batch, always late
- Paying contractors late to 'manage cash' - destroys bench loyalty
- Skipping reconciliation - DSO drifts invisibly

## Quality checklist (self-review)

- Did I send every invoice on the same day?
- Were contractors paid on agreed terms?
- Did the books match the bank?

## Related playbooks

- `friday-cash-flow-and-utilization-check`
- `annual-planning-and-financial-close`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **monthly-billing-batch-routine** (tier `pro`, blocks stage 1) -- Invoice-clients stage needs a step-by-step batch routine
- **agency-pnl-tracker-template** (tier `pro`, blocks stage 3) -- Reconcile stage needs a P&L tracker template

## CLI usage

```
faion get-content monthly-invoice-contractor-pay-batch --format md       # human-readable rendering
faion get-content monthly-invoice-contractor-pay-batch --format context  # agent-optimised context bundle
faion get-content monthly-invoice-contractor-pay-batch --format json     # raw structured form
```
