---
slug: agency-to-recurring-revenue-transition
tier: pro
group: product-management
persona: P5
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Project-heavy revenue mix to at least 50% recurring revenue and 40% less founder delivery time in 6 months."
content_id: e219f123bca64c33
methodology_refs:
  - aarrr-pirate-metrics
  - cohort-implementation
  - ops-metrics-basics
  - ops-financial-basics
  - business-model-research
  - risk-assessment
  - minimum-product-frameworks
  - mlp-planning
  - release-planning
  - competitive-positioning
  - growth-brand-positioning
  - growth-gtm-strategy
  - growth-free-trial-optimization
  - plg-implementation-guide
  - north-star-metric
  - retention-strategies
  - growth-affiliate-marketing
  - ops-customer-success-basics
  - ops-upselling-cross-selling
  - ops-partnership-strategy
  - onboarding-30-day
  - onboarding-60-90-day
  - ops-contractor-management
  - resource-management
  - product-operations
  - portfolio-strategy
  - ops-annual-planning-process
  - ops-annual-planning-templates
  - business-model-planning
  - trend-analysis
---

# Agency-to-recurring-revenue transition (6 months)

**Playbook slug:** `agency-to-recurring-revenue-transition`
**Tier:** pro
**Complexity:** deep
**Persona:** P5 -- Micro-agency founder

## Intent

Project-heavy revenue mix to at least 50% recurring revenue and 40% less founder delivery time in 6 months.

## Scope

Move the agency from majority project-based revenue to majority retainer/productized recurring revenue. Outcome: at least 50% MRR-style recurring by month 6, founder time spent on delivery cut by 40%, customer concentration at or below 30% per logo. Exit artifact: revenue-mix audit + transition decision pack.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Spinning up a SaaS product - separate playbook
- Hiring full-time team to scale projects - out of scope

### Prerequisites

- Steady project revenue across 12+ months
- At least 2 recurring patterns identified in past work

## Success criteria

The playbook is done when:
- Revenue-mix audit complete (project vs retainer vs productized)
- 2 productized offers live with intake + delivery SOPs
- 50%+ recurring revenue by month 6
- Founder delivery hours cut by 40%+
- Customer concentration at or below 30% per logo
- Annual plan refreshed against new mix

## Stages

### Stage 1: Audit the mix

**Intent:** Honest revenue + time + risk view today.

**Tasks:**
- Tag last 12 months revenue by type
- Map founder hours per revenue line
- Score customer concentration risk

**Methodologies in chain:**
- `aarrr-pirate-metrics` -> `pro/marketing/growth-marketer/aarrr-pirate-metrics`
- `cohort-implementation` -> `pro/marketing/growth-marketer/cohort-implementation`
- `ops-metrics-basics` -> `pro/marketing/growth-marketer/ops-metrics-basics`
- `ops-financial-basics` -> `pro/marketing/gtm-strategist/ops-financial-basics`
- `business-model-research` -> `pro/research/market-researcher/business-model-research`
- `risk-assessment` -> `pro/research/market-researcher/risk-assessment`

**Outputs:**
- Revenue-mix audit
- Founder time-by-line table

**Decision gate:**
> Advance with baseline + transition target documented.

### Stage 2: Productize 2

**Intent:** Two productized offers to anchor recurring revenue.

**Tasks:**
- Pick top-2 patterns from audit
- Productize using productize-a-service-offering chain
- Launch landings + intake forms

**Methodologies in chain:**
- `minimum-product-frameworks` -> `pro/product/product-manager/minimum-product-frameworks`
- `mlp-planning` -> `pro/product/product-manager/mlp-planning`
- `release-planning` -> `pro/product/product-manager/release-planning`
- `competitive-positioning` -> `pro/product/product-planning/competitive-positioning`
- `growth-brand-positioning` -> `pro/marketing/gtm-strategist/growth-brand-positioning`
- `growth-gtm-strategy` -> `pro/marketing/gtm-strategist/growth-gtm-strategy`
- `growth-free-trial-optimization` -> `pro/marketing/conversion-optimizer/growth-free-trial-optimization`
- `plg-implementation-guide` -> `pro/marketing/conversion-optimizer/plg-implementation-guide`

**Outputs:**
- 2 productized landings live
- Delivery SOPs

**Decision gate:**
> Advance once each productized offer has shipped 1 paid run.

### Stage 3: Convert + retain

**Intent:** Pull existing project clients into retainer / productized.

**Tasks:**
- Send retainer pitch to top 10 accounts
- Convert 3+ to retainer
- Stand up retention ops

**Methodologies in chain:**
- `north-star-metric` -> `pro/marketing/growth-marketer/north-star-metric`
- `retention-strategies` -> `pro/marketing/growth-marketer/retention-strategies`
- `growth-affiliate-marketing` -> `pro/marketing/gtm-strategist/growth-affiliate-marketing`
- `ops-customer-success-basics` -> `pro/marketing/gtm-strategist/ops-customer-success-basics`
- `ops-upselling-cross-selling` -> `pro/marketing/gtm-strategist/ops-upselling-cross-selling`
- `ops-partnership-strategy` -> `pro/marketing/gtm-strategist/ops-partnership-strategy`

**Outputs:**
- Retainer conversion ledger
- Retention SOP

**Decision gate:**
> Advance when 3+ accounts converted to recurring.

### Stage 4: De-risk delivery

**Intent:** Founder cuts hands-on hours: contractor coverage + ops.

**Tasks:**
- Hand 2 deliverables to contractors
- Stand up product-ops cadence
- Build founder-time dashboard

**Methodologies in chain:**
- `onboarding-30-day` -> `pro/comms/hr-recruiter/onboarding-30-day`
- `onboarding-60-90-day` -> `pro/comms/hr-recruiter/onboarding-60-90-day`
- `ops-contractor-management` -> `pro/marketing/gtm-strategist/ops-contractor-management`
- `resource-management` -> `pro/pm/project-manager/resource-management`
- `product-operations` -> `pro/product/product-operations/product-operations`
- `portfolio-strategy` -> `pro/product/product-manager/portfolio-strategy`
- `portfolio-strategy` -> `pro/product/product-planning/portfolio-strategy`

**Outputs:**
- Contractor coverage SOP
- Founder-time dashboard

**Decision gate:**
> Advance once founder delivery hours fall to or below 60% of baseline.

### Stage 5: Plan + decide

**Intent:** Annual plan against new mix; commit or roll back.

**Tasks:**
- Run annual planning ritual against new mix
- Forecast next 12 months
- Write commitment or rollback decision

**Methodologies in chain:**
- `ops-annual-planning-process` -> `pro/marketing/gtm-strategist/ops-annual-planning-process`
- `ops-annual-planning-templates` -> `pro/marketing/gtm-strategist/ops-annual-planning-templates`
- `business-model-planning` -> `pro/research/market-researcher/business-model-planning`
- `trend-analysis` -> `pro/research/market-researcher/trend-analysis`

**Outputs:**
- Annual plan v2
- Transition decision doc

**Decision gate:**
> Required: written decision. Continue, double down, or roll back to project-led.

## Common pitfalls

- Productizing without selling - landing pages without buyers do not move the mix
- Cutting founder hours before delivery SOPs are tested - quality drops, churn rises
- Treating month-3 revenue dip as failure - recurring revenue lags the work

## Quality checklist (self-review)

- Did I measure founder hours, not just revenue?
- Are the productized offers actually selling, not just live?
- Is concentration risk down or just hidden under retainers?

## Related playbooks

- `productize-a-service-offering`
- `annual-planning-and-financial-close`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-revenue-mix-audit-template** (tier `pro`, blocks stage 1) -- Audit-the-mix stage needs a working revenue-mix audit spreadsheet
- **retainer-conversion-script** (tier `pro`, blocks stage 3) -- Convert-and-retain stage needs a script for converting project clients
- **agency-to-saas-readiness-checklist** (tier `pro`, blocks stage 5) -- Plan-and-decide stage needs a readiness checklist if next step is SaaS
- **founder-time-audit-tool** (tier `pro`, blocks stage 4) -- De-risk-delivery stage needs a tool to track founder hours per revenue line

## CLI usage

```
faion get-content agency-to-recurring-revenue-transition --format md       # human-readable rendering
faion get-content agency-to-recurring-revenue-transition --format context  # agent-optimised context bundle
faion get-content agency-to-recurring-revenue-transition --format json     # raw structured form
```
