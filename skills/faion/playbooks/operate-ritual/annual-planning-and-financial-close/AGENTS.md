# Annual planning and financial close (6-8 weeks, Q4 cycle)

**Playbook slug:** `annual-planning-and-financial-close`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

Q4 to books closed, taxes filed, next-year targets locked, service portfolio refreshed, compliance risks logged.

## Scope

Run an annual planning cycle that closes the books, files taxes, sets next-year revenue / margin / hiring targets, locks the service portfolio, and surfaces compliance risks before they bite. Exit artifact: annual-plan pack + closed books + filed returns + refreshed risk register.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Multi-year strategic planning - separate cadence
- Investor-grade financial audit - out of scope for solo / micro-agency

### Prerequisites

- Bookkeeping in place (Xero / QuickBooks / equivalent)
- Last 12 months revenue + expense data accessible

## Success criteria

The playbook is done when:
- Books closed for prior year
- Taxes filed or scheduled with accountant
- Next-year revenue, margin, hiring targets locked
- Service portfolio refreshed (kept / dropped / new)
- Compliance risk register updated
- Annual plan signed off by the founder in writing

## Stages

### Stage 1: Close books + file taxes

**Intent:** Honest financial picture before planning anything.

**Tasks:**
- Reconcile bank + invoicing data
- Lock prior-year P&L + balance sheet
- File taxes or schedule with accountant

**Methodologies in chain:**
- `ops-financial-basics` → `marketing/ops-financial-basics`
- `ops-tax-basics` → `marketing/ops-tax-basics`
- `ops-tax-compliance` → `marketing/ops-tax-compliance`
- `ops-legal-basics` → `marketing/ops-legal-basics`
- `ops-legal-compliance` → `marketing/ops-legal-compliance`
- `ops-legal-compliance-checklist` → `marketing/ops-legal-compliance-checklist`

**Outputs:**
- Closed P&L + BS
- Tax filing confirmation

**Decision gate:**
> Advance only when books are reconciled and tax filing started.

### Stage 2: Plan targets

**Intent:** Revenue, margin, hiring targets - defensible numbers.

**Tasks:**
- Forecast revenue lines
- Set margin + hiring targets
- Run sensitivity analysis

**Methodologies in chain:**
- `ops-annual-planning-process` → `marketing/ops-annual-planning-process`
- `ops-annual-planning-templates` → `marketing/ops-annual-planning-templates`
- `growth-gtm-strategy` → `marketing/growth-gtm-strategy`
- `growth-brand-positioning` → `marketing/growth-brand-positioning`
- `trend-analysis-market-research` → `research/trend-analysis-market-research`
- `predictive-analytics-pm` → `pm/predictive-analytics-pm`

**Outputs:**
- Target spreadsheet
- Sensitivity scenarios

**Decision gate:**
> Advance when targets pass the gut + math test.

### Stage 3: Refresh portfolio + ops

**Intent:** Service lines pruned, ops + contractor mix adjusted.

**Tasks:**
- Score each service line
- Drop or refactor weakest
- Adjust contractor + partnership commitments

**Methodologies in chain:**
- `portfolio-strategy-product-planning` → `pm/portfolio-strategy-product-planning`
- `ops-contractor-management` → `marketing/ops-contractor-management`
- `ops-partnership-strategy` → `marketing/ops-partnership-strategy`

**Outputs:**
- Service-line decision doc
- Contractor + partnership plan

**Decision gate:**
> Advance when each service line is in 'keep', 'refactor', or 'sunset' bucket.

### Stage 4: Risk + compliance

**Intent:** Surface risks now so they do not blindside next year.

**Tasks:**
- Refresh risk register
- Audit data + privacy compliance
- Plan mitigations + owners

**Methodologies in chain:**
- `privacy-compliance` → `marketing/privacy-compliance`
- `risk-management` → `pm/risk-management`
- `risk-register` → `pm/risk-register`
- `risk-assessment-market-research` → `research/risk-assessment-market-research`

**Outputs:**
- Risk register v2
- Compliance gap list

**Decision gate:**
> Required output: every high-impact risk has an owner + mitigation date.

## Common pitfalls

- Setting next-year targets without closed books - fiction in, fiction out
- Skipping the portfolio prune because services 'might come back'
- Treating compliance as a Q1 problem - late filings are expensive

## Quality checklist (self-review)

- Are the targets defensible to a stranger with the spreadsheet?
- Did I actually drop or refactor a service, or only nudge?
- Is the risk register updated, not just dusted off?

## Related playbooks

- `quarter-end-retention-review`
- `agency-to-recurring-revenue-transition`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-year-end-close-checklist** (tier `pro`, blocks stage 1) -- Close-books stage needs a step-by-step year-end close checklist
- **us-uk-eu-compliance-matrix** (tier `pro`, blocks stage 4) -- Risk-and-compliance stage needs a jurisdiction-aware compliance matrix
- **agency-annual-plan-template** (tier `pro`, blocks stage 2) -- Plan-targets stage needs a working annual plan template
- **agency-risk-register-template** (tier `pro`, blocks stage 4) -- Risk-and-compliance stage needs a refreshable risk register template

## CLI usage

```
faion get-content annual-planning-and-financial-close --format md       # human-readable rendering
faion get-content annual-planning-and-financial-close --format context  # agent-optimised context bundle
faion get-content annual-planning-and-financial-close --format json     # raw structured form
```
