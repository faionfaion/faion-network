---
slug: friday-cash-flow-and-utilization-check
tier: pro
group: delivery-ops
persona: P5
goal: operate-ritual
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: 30-min Friday ritual to AR follow-up list + utilization heat map + go/no-go on next contractor hire.
content_id: 1e9f0a8a6701d95e
methodology_refs:
  - ops-financial-basics
  - ops-tax-basics
  - ops-financial-planning
  - ops-contractor-management
---

# Friday cash-flow + utilization check

**Playbook slug:** `friday-cash-flow-and-utilization-check`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

30-min Friday ritual to AR follow-up list + utilization heat map + go/no-go on next contractor hire.

## Scope

Founder reviews cash position, AR, AP, contractor utilization. Output: AR follow-up list + utilization heat map + go/no-go on next contractor hire. Exit artifact: cash + utilization summary doc, AR follow-ups sent, hire decision noted.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Monthly book close - separate ritual
- Annual financial planning - separate playbook

### Prerequisites

- Bookkeeping + invoicing system live
- Contractor + project utilization data captured weekly

## Success criteria

The playbook is done when:
- Cash position + 8-week runway noted
- AR follow-up list with owners + dates
- Contractor utilization heat map updated
- Hire / no-hire decision logged for the week

## Stages

### Stage 1: Cash + AR/AP

**Intent:** Cash truth + chase overdue invoices same day.

**Tasks:**
- Pull cash balance + 8-week runway
- List AR by age bucket
- Send AR follow-ups for items overdue more than 30 days

**Methodologies in chain:**
- `ops-financial-basics` -> `pro/marketing/gtm-strategist/ops-financial-basics`
- `ops-tax-basics` -> `pro/marketing/gtm-strategist/ops-tax-basics`
- `ops-financial-planning` -> `solo/marketing/gtm-strategist/ops-financial-planning`

**Outputs:**
- Cash snapshot
- AR follow-up log

**Decision gate:**
> Advance once AR follow-ups sent for every overdue invoice.

### Stage 2: Utilization heat map

**Intent:** Per-contractor + per-line utilization vs target.

**Tasks:**
- Pull hours per contractor
- Score against utilization target
- Tag over / under contractors

**Methodologies in chain:**
- `ops-contractor-management` -> `pro/marketing/gtm-strategist/ops-contractor-management`

**Outputs:**
- Utilization heat map

**Decision gate:**
> Advance once heat map covers every active contractor.

### Stage 3: Hire / no-hire

**Intent:** Use cash + utilization signal to decide on next hire.

**Tasks:**
- Apply hire decision rule to data
- Log decision + reason in tracker
- Trigger hire playbook if green

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Hire / no-hire decision doc

**Decision gate:**
> Required output: written go/no-go for next contractor hire.

## Common pitfalls

- Skipping AR chase because 'they will pay' - DSO creep kills cash
- Hiring on revenue spikes, not on sustained utilization
- Reading utilization as 'busy' rather than 'billable'

## Quality checklist (self-review)

- Did I chase every overdue invoice, no exceptions?
- Is the utilization number billable, not just hours worked?
- Did I write the hire decision down?

## Related playbooks

- `monthly-invoice-contractor-pay-batch`
- `monday-lead-pipeline-review`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-cash-flow-friday-routine** (tier `pro`, blocks stage 1) -- Cash-and-AR stage needs a step-by-step Friday routine document
- **contractor-utilization-heatmap** (tier `pro`, blocks stage 2) -- Utilization-heat-map stage needs a reusable heat-map template
- **capacity-planning** (tier `pro`, blocks stage 2) -- Utilization stage references capacity-planning playbook not yet ported to v2 manifest
- **hiring-funnel** (tier `pro`, blocks stage 3) -- Hire-decision stage references hiring-funnel playbook not yet ported to v2 manifest

## CLI usage

```
faion get-content friday-cash-flow-and-utilization-check --format md       # human-readable rendering
faion get-content friday-cash-flow-and-utilization-check --format context  # agent-optimised context bundle
faion get-content friday-cash-flow-and-utilization-check --format json     # raw structured form
```
