---
slug: quarter-end-retention-review
tier: pro
group: client-engagement
persona: P5
goal: operate-ritual
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: End of quarter to per-account next-quarter plan, 3 upsell targets, churn-risk list with mitigation, and a refreshed reference pool.
content_id: 49d9987e2e0d682c
methodology_refs:
  - cohort-implementation
  - ops-churn-basics
  - retention-metrics
  - ops-customer-success-metrics
  - benefits-realization
  - feedback-management
  - ops-customer-success-basics
  - growth-customer-testimonials
  - stakeholder-register
  - stakeholder-engagement-advanced
  - ops-upselling-cross-selling
  - ops-churn-prevention
  - retention-strategies
  - ops-annual-planning-process
  - ops-annual-planning-templates
  - project-closure
  - portfolio-strategy
---

# Quarter-end retention review (QBR cycle, 4 weeks)

**Playbook slug:** `quarter-end-retention-review`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

End of quarter to per-account next-quarter plan, 3 upsell targets, churn-risk list with mitigation, and a refreshed reference pool.

## Scope

Across the active book of clients, run a structured quarterly business review that surfaces churn risk, upsell, and reference opportunities. Outputs: per-account next-quarter plan, three upsell targets, churn-risk list with mitigation, and a refreshed reference pool. Exit artifact: QBR pack per account + portfolio dashboard row updated for the quarter.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Annual planning - separate playbook
- New-business pipeline review - distinct cadence

### Prerequisites

- Active retainer + project book of 3+ clients
- Basic delivery + outcome metrics already captured per account

## Success criteria

The playbook is done when:
- Account health scored for every active client
- Churn-risk list with mitigation owner per account
- 3 upsell targets with concrete next step
- Refreshed reference pool
- Per-account next-quarter plan signed by client
- Portfolio dashboard updated

## Stages

### Stage 1: Score health

**Intent:** Cohort + outcome data to account health score per client.

**Tasks:**
- Pull cohort + retention data
- Score each account on health rubric
- Tag risk + upsell candidates

**Methodologies in chain:**
- `cohort-implementation` -> `pro/marketing/growth-marketer/cohort-implementation`
- `ops-churn-basics` -> `pro/marketing/growth-marketer/ops-churn-basics`
- `retention-metrics` -> `pro/marketing/growth-marketer/retention-metrics`
- `ops-customer-success-metrics` -> `pro/marketing/gtm-strategist/ops-customer-success-metrics`

**Outputs:**
- Account-health table
- Risk + upsell tags

**Decision gate:**
> Advance once every account has a numeric health score.

### Stage 2: Prep QBR pack

**Intent:** Per-account: results, risks, options, asks.

**Tasks:**
- Draft QBR slides per account
- Capture wins + benefits realized
- List 3 next-quarter options

**Methodologies in chain:**
- `benefits-realization` -> `pro/pm/project-manager/benefits-realization`
- `feedback-management` -> `pro/product/product-manager/feedback-management`
- `ops-customer-success-basics` -> `pro/marketing/gtm-strategist/ops-customer-success-basics`
- `growth-customer-testimonials` -> `solo/marketing/content-marketer/growth-customer-testimonials`

**Outputs:**
- QBR pack per account

**Decision gate:**
> Advance when every active account has a draft QBR pack.

### Stage 3: Run reviews

**Intent:** 45-min QBR per account; capture renewal + upsell signal.

**Tasks:**
- Schedule QBR with each sponsor
- Run 45-min meeting against pack
- Capture next-quarter commitments in writing

**Methodologies in chain:**
- `stakeholder-register` -> `pro/pm/project-manager/stakeholder-register`
- `stakeholder-engagement-advanced` -> `pro/pm/project-manager/stakeholder-engagement-advanced`
- `ops-upselling-cross-selling` -> `pro/marketing/gtm-strategist/ops-upselling-cross-selling`

**Outputs:**
- Per-account next-quarter plan
- Upsell + reference signals

**Decision gate:**
> Advance once every QBR meeting held OR formally declined.

### Stage 4: Plan + close out

**Intent:** Portfolio view: who renews, who churns, who upsells.

**Tasks:**
- Mitigate churn risks with owners
- Schedule upsell follow-ups
- Refresh reference pool

**Methodologies in chain:**
- `ops-churn-prevention` -> `pro/marketing/growth-marketer/ops-churn-prevention`
- `retention-strategies` -> `pro/marketing/growth-marketer/retention-strategies`
- `ops-annual-planning-process` -> `pro/marketing/gtm-strategist/ops-annual-planning-process`
- `ops-annual-planning-templates` -> `pro/marketing/gtm-strategist/ops-annual-planning-templates`
- `project-closure` -> `pro/pm/project-manager/project-closure`
- `portfolio-strategy` -> `pro/product/product-manager/portfolio-strategy`
- `portfolio-strategy` -> `pro/product/product-planning/portfolio-strategy`

**Outputs:**
- Portfolio dashboard updated
- Churn-mitigation actions live

**Decision gate:**
> Required output: written next-quarter plan per account + portfolio dashboard refreshed.

## Common pitfalls

- Treating QBR as a status report instead of a renewal + upsell conversation
- Skipping the QBR for 'happy' accounts - those are the ones to upsell
- No written next-quarter plan = no contract for the next 90 days

## Quality checklist (self-review)

- Does every account have a numeric health score?
- Did I leave each QBR with at least one client commitment?
- Is the reference pool refreshed every quarter?

## Related playbooks

- `quarterly-retainer-review-per-client`
- `annual-planning-and-financial-close`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **qbr-deck-template-services** (tier `pro`, blocks stage 2) -- Prep-QBR-pack stage needs a default deck template for services QBR
- **account-health-scoring-model** (tier `pro`, blocks stage 1) -- Score-health stage needs an explicit numeric scoring model
- **graceful-offboard-script** (tier `pro`, blocks stage 4) -- Plan-and-close-out stage needs a script for graceful churn offboarding
- **reference-program-playbook** (tier `pro`, blocks stage 4) -- Plan-and-close-out stage needs a structured reference program

## CLI usage

```
faion get-content quarter-end-retention-review --format md       # human-readable rendering
faion get-content quarter-end-retention-review --format context  # agent-optimised context bundle
faion get-content quarter-end-retention-review --format json     # raw structured form
```
