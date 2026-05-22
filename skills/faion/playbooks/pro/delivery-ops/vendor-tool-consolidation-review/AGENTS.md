---
slug: vendor-tool-consolidation-review
tier: pro
group: delivery-ops
persona: P5
goal: operate-ritual
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Monthly SaaS audit to kill list + consolidation plan + projected savings.
content_id: 76ce9b007b51a526
methodology_refs:
  - ops-financial-basics
  - ops-tax-basics
  - ops-partnership-strategy
  - ops-pricing-strategy
  - communications-management
  - cross-tool-migration
  - tool-migration-process
---

# Vendor / tool consolidation review

**Playbook slug:** `vendor-tool-consolidation-review`
**Tier:** pro
**Complexity:** light
**Persona:** P5 -- Micro-agency founder

## Intent

Monthly SaaS audit to kill list + consolidation plan + projected savings.

## Scope

Founder audits SaaS + tool sprawl monthly and decides what to cut, consolidate, or replace. Output: kill list, consolidation plan, projected savings. Exit artifact: tool inventory + decisions + cancellation actions taken.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Annual financial close - separate ritual
- Migration execution - separate playbook per tool

### Prerequisites

- Bookkeeping with tool subscriptions tagged
- Last-month vendor + tool inventory

## Success criteria

The playbook is done when:
- Complete tool inventory with cost + usage tag
- Kill list with cancellation owner + date
- Consolidation plan written
- Projected monthly + annual savings logged

## Stages

### Stage 1: Inventory

**Intent:** Single source of truth for every active subscription.

**Tasks:**
- Pull subscription list from bookkeeping
- Cross-check with bank statements
- Tag each with active user count + last login

**Methodologies in chain:**
- `ops-financial-basics` -> `pro/marketing/gtm-strategist/ops-financial-basics`
- `ops-tax-basics` -> `pro/marketing/gtm-strategist/ops-tax-basics`

**Outputs:**
- Tool inventory

**Decision gate:**
> Advance once every line item tagged.

### Stage 2: Decide kill / keep / consolidate

**Intent:** Apply decision rule, no nostalgia.

**Tasks:**
- Score each tool by usage x strategic value
- Tag for kill / keep / consolidate
- Identify overlap candidates

**Methodologies in chain:**
- `ops-partnership-strategy` -> `pro/marketing/gtm-strategist/ops-partnership-strategy`
- `ops-pricing-strategy` -> `solo/marketing/gtm-strategist/ops-pricing-strategy`

**Outputs:**
- Kill list
- Consolidation plan

**Decision gate:**
> Advance once every line item has a decision.

### Stage 3: Execute + log

**Intent:** Cancel today, plan migrations for the month.

**Tasks:**
- Cancel kill-list items same day
- Schedule migrations + comms
- Log projected savings

**Methodologies in chain:**
- `communications-management` -> `pro/pm/project-manager/communications-management`
- `cross-tool-migration` -> `pro/pm/project-manager/cross-tool-migration`
- `tool-migration-process` -> `pro/pm/pm-agile/tool-migration-process`

**Outputs:**
- Cancellations confirmed
- Migration schedule
- Savings log

**Decision gate:**
> Required: cancellations executed same day. Migrations have owners + dates.

## Common pitfalls

- Keeping tools 'just in case' - sprawl grows unchecked
- Skipping migration plan - kills and rage-buys later
- Not logging savings - invisible win = no behavior change

## Quality checklist (self-review)

- Did I cancel today, or schedule a future cancellation?
- Is the migration plan dated?
- Did I log the saving in the books?

## Related playbooks

- `friday-cash-flow-and-utilization-check`
- `monthly-invoice-contractor-pay-batch`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **saas-stack-audit-micro-agency** (tier `pro`, blocks stage 1) -- Inventory stage needs a tested audit template for micro-agency stacks
- **tool-consolidation-decision-rule** (tier `pro`, blocks stage 2) -- Decide stage needs an explicit decision rule

## Operating notes

This ritual is shaped for the founder-operator running a 2-3 person agency. Speed matters more than ceremony: every minute lost on overhead is a minute taken from billable work. The atomic shape (single intent, short stage chain, hard decision gates) lets the operator complete the playbook in one session without losing context.

When the playbook fails, the failure is almost always in the decision gate: an operator advances despite an unmet criterion, or skips a stage entirely because it feels redundant. The playbook is most useful when the operator treats each gate as a stop sign rather than a recommendation. If a gate keeps blocking, the right move is usually upstream -- prerequisites are weak, the role brief is unclear, or the cadence is unrealistic for the actual workload.

The chained methodologies are written for adjacent personas (solo founder, growth marketer, project manager) and apply cleanly when the operator wears all three hats at once. Treat each methodology as a checklist rather than a course: skim, apply the relevant rubric, then move on. The point of the playbook is to deliver the exit artifact, not to read every methodology end to end.

## CLI usage

```
faion get-content vendor-tool-consolidation-review --format md       # human-readable rendering
faion get-content vendor-tool-consolidation-review --format context  # agent-optimised context bundle
faion get-content vendor-tool-consolidation-review --format json     # raw structured form
```
