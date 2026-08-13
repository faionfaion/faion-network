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
- `aarrr-pirate-metrics` → `marketing/aarrr-pirate-metrics`
- `cohort-implementation` → `marketing/cohort-implementation`
- `ops-metrics-basics` → `marketing/ops-metrics-basics`
- `ops-financial-basics` → `marketing/ops-financial-basics`
- `business-model-research-market-research` → `research/business-model-research-market-research`
- `risk-assessment-market-research` → `research/risk-assessment-market-research`

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
- `minimum-product-frameworks` → `pm/minimum-product-frameworks`
- `mlp-planning` → `pm/mlp-planning`
- `release-planning` → `pm/release-planning`
- `competitive-positioning-product-planning` → `pm/competitive-positioning-product-planning`
- `growth-brand-positioning` → `marketing/growth-brand-positioning`
- `growth-gtm-strategy` → `marketing/growth-gtm-strategy`
- `plg-implementation-guide` → `marketing/plg-implementation-guide`

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
- `north-star-metric` → `marketing/north-star-metric`
- `retention-strategies` → `marketing/retention-strategies`
- `growth-affiliate-marketing` → `marketing/growth-affiliate-marketing`
- `ops-customer-success-basics` → `marketing/ops-customer-success-basics`
- `ops-upselling-cross-selling` → `marketing/ops-upselling-cross-selling`
- `ops-partnership-strategy` → `marketing/ops-partnership-strategy`

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
- `onboarding-30-day` → `hr/onboarding-30-day`
- `onboarding-60-90-day` → `hr/onboarding-60-90-day`
- `ops-contractor-management` → `marketing/ops-contractor-management`
- `resource-management` → `pm/resource-management`
- `product-operations-product-ops` → `pm/product-operations-product-ops`
- `portfolio-strategy` → `pm/portfolio-strategy`
- `portfolio-strategy-product-planning` → `pm/portfolio-strategy-product-planning`

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
- `ops-annual-planning-process` → `marketing/ops-annual-planning-process`
- `ops-annual-planning-templates` → `marketing/ops-annual-planning-templates`
- `business-model-planning` → `research/business-model-planning`
- `trend-analysis-market-research` → `research/trend-analysis-market-research`

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
