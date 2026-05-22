---
slug: productize-a-service-offering
tier: pro
group: product-management
persona: P5
goal: build-ship
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Recurring custom engagement to named, fixed-scope, fixed-price productized service with landing page, sales script, delivery SOP, and at least one paying customer.
content_id: 88085c51585b0603
methodology_refs:
  - business-process-analysis
  - business-model-research
  - market-analysis
  - competitive-positioning
  - minimum-product-frameworks
  - mlp-planning
  - release-planning
  - use-case-modeling
  - growth-brand-positioning
  - growth-conversion-optimization
  - conversion-tracking
  - growth-loops
  - growth-copywriting-fundamentals
  - growth-customer-testimonials
  - growth-seo-fundamentals
  - feedback-management
  - methodologies-summary
  - continuous-discovery-habits
  - growth-email-marketing
  - growth-newsletter-growth
  - growth-press-coverage
  - ops-customer-success-metrics
  - product-analytics
  - competitive-intelligence
  - competitor-analysis
---

# Productize a service offering (8-10 weeks idea to first paid sale)

**Playbook slug:** `productize-a-service-offering`
**Tier:** pro
**Complexity:** deep
**Persona:** P5 -- Micro-agency founder

## Intent

Recurring custom engagement to named, fixed-scope, fixed-price productized service with landing page, sales script, delivery SOP, and at least one paying customer.

## Scope

Take a recurring custom engagement and convert it into a named, fixed-scope, fixed-price productized service with a public landing page, sales script, delivery SOP, and at least one paying customer. Exit artifact: one shipped productized service whose unit-economics, delivery time, and customer satisfaction are documented and repeatable by the next contractor on the bench.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Full SaaS productization - this is a service, not software
- Multi-product portfolio - single productized offer per playbook run

### Prerequisites

- Three or more past clients who bought a similar engagement
- A landing page surface (Webflow, Framer, MDX, etc.)

## Success criteria

The playbook is done when:
- Named offer + one-sentence positioning
- Public landing page with pricing visible
- Documented sales script + objection FAQ
- Delivery SOP runnable by a contractor (not the founder)
- At least 1 paying customer at the productized price
- Unit economics measured: gross margin + delivery hours

## Stages

### Stage 1: Pattern audit

**Intent:** Find the recurring engagement worth productizing.

**Tasks:**
- List last 12 months of paid engagements
- Tag by pattern (deliverable, scope, duration)
- Pick top-1 pattern by frequency x margin

**Methodologies in chain:**
- `business-process-analysis` -> `pro/ba/business-analyst/business-process-analysis`
- `business-model-research` -> `pro/research/market-researcher/business-model-research`
- `market-analysis` -> `pro/research/market-researcher/market-analysis`
- `competitive-positioning` -> `pro/product/product-planning/competitive-positioning`

**Outputs:**
- Engagement-pattern table
- Productize candidate decision

**Decision gate:**
> Advance if one pattern recurs at least 3 times with stable margin.

### Stage 2: Scope + price

**Intent:** Lock fixed scope + fixed price with explicit cuts.

**Tasks:**
- Define MLP (minimum lovable productized) scope
- Price against value not hours
- Write 3 explicit non-goals

**Methodologies in chain:**
- `minimum-product-frameworks` -> `pro/product/product-manager/minimum-product-frameworks`
- `mlp-planning` -> `pro/product/product-manager/mlp-planning`
- `release-planning` -> `pro/product/product-manager/release-planning`
- `use-case-modeling` -> `pro/ba/business-analyst/use-case-modeling`

**Outputs:**
- Scope-of-work doc
- Price card

**Decision gate:**
> Advance only if scope fits one page and price defensible to a stranger.

### Stage 3: Landing + funnel

**Intent:** Public surface: positioning, copy, intake form, social proof.

**Tasks:**
- Write hero + 5 sections
- Add intake form with qualifying questions
- Drop 3 case-study or testimonial blocks

**Methodologies in chain:**
- `growth-brand-positioning` -> `pro/marketing/gtm-strategist/growth-brand-positioning`
- `growth-conversion-optimization` -> `pro/marketing/conversion-optimizer/growth-conversion-optimization`
- `conversion-tracking` -> `pro/marketing/growth-marketer/conversion-tracking`
- `growth-loops` -> `pro/marketing/growth-marketer/growth-loops`
- `growth-copywriting-fundamentals` -> `solo/marketing/content-marketer/growth-copywriting-fundamentals`
- `growth-customer-testimonials` -> `solo/marketing/content-marketer/growth-customer-testimonials`
- `growth-seo-fundamentals` -> `solo/marketing/seo-manager/growth-seo-fundamentals`

**Outputs:**
- Public landing URL
- Intake form live

**Decision gate:**
> Advance when landing converts at least 1 qualified discovery in 14 days.

### Stage 4: Sales script + delivery SOP

**Intent:** Make the sale + delivery repeatable without founder presence.

**Tasks:**
- Write sales call run-of-show (15-30 min)
- Author delivery SOP step-by-step
- Record one demo session for the SOP

**Methodologies in chain:**
- `feedback-management` -> `pro/product/product-manager/feedback-management`
- `methodologies-summary` -> `pro/product/product-manager/methodologies-summary`
- `continuous-discovery-habits` -> `pro/product/product-manager/continuous-discovery-habits`
- `growth-email-marketing` -> `solo/marketing/content-marketer/growth-email-marketing`
- `growth-newsletter-growth` -> `solo/marketing/content-marketer/growth-newsletter-growth`

**Outputs:**
- Sales script
- Delivery SOP doc

**Decision gate:**
> Advance once a contractor can read the SOP and produce a draft deliverable.

### Stage 5: Launch + measure

**Intent:** Sell, deliver, measure unit-economics on first paid run.

**Tasks:**
- Pitch to 5 best-fit past clients first
- Sell + deliver one full cycle
- Measure margin + delivery hours + NPS

**Methodologies in chain:**
- `growth-press-coverage` -> `pro/marketing/gtm-strategist/growth-press-coverage`
- `ops-customer-success-metrics` -> `pro/marketing/gtm-strategist/ops-customer-success-metrics`
- `product-analytics` -> `pro/product/product-manager/product-analytics`
- `competitive-intelligence` -> `pro/research/market-researcher/competitive-intelligence`
- `competitor-analysis` -> `pro/research/market-researcher/competitor-analysis`

**Outputs:**
- First paid invoice
- Unit-economics dashboard row

**Decision gate:**
> Required: 1 paid sale at productized price AND margin at or above baseline custom engagement.

## Common pitfalls

- Productizing the pattern the founder enjoys, not the one with the best margin
- Pricing at last-engagement hours - locks you into custom margins
- Treating the landing page as the launch - the SOP is the launch

## Quality checklist (self-review)

- Could a contractor deliver this without my direct involvement?
- Does the price card embarrass me? If yes, raise it.
- Did I measure margin or only revenue on the first run?

## Related playbooks

- `productize-one-service-from-custom-to-fixed`
- `inbound-lead-to-signed-retainer`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **productized-service-canvas** (tier `pro`, blocks stage 1) -- Pattern-audit stage needs a one-page canvas to score candidates
- **agency-case-study-template** (tier `pro`, blocks stage 3) -- Landing+funnel stage needs a structured case-study block format
- **service-offer-pricing-calculator** (tier `pro`, blocks stage 2) -- Scope+price stage needs a working margin-aware calculator
- **delivery-sop-template** (tier `pro`, blocks stage 4) -- Sales+delivery stage needs a reusable SOP template

## CLI usage

```
faion get-content productize-a-service-offering --format md       # human-readable rendering
faion get-content productize-a-service-offering --format context  # agent-optimised context bundle
faion get-content productize-a-service-offering --format json     # raw structured form
```
