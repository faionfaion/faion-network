---
slug: productize-one-service-from-custom-to-fixed
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
summary: Recurring custom engagement to fixed-scope, fixed-price productized service with landing page, intake form, delivery SOP.
content_id: a8fbc2c06bbd4e4a
methodology_refs:
  - competitive-positioning
  - niche-evaluation
  - ops-pricing-strategy
  - growth-brand-positioning
  - funnel-tactics-basics
  - ops-customer-success-basics
  - ops-financial-basics
  - ops-upselling-cross-selling
---

# Productize one service from custom to fixed

**Playbook slug:** `productize-one-service-from-custom-to-fixed`
**Tier:** pro
**Complexity:** deep
**Persona:** P5 -- Micro-agency founder

## Intent

Recurring custom engagement to fixed-scope, fixed-price productized service with landing page, intake form, delivery SOP.

## Scope

Convert a recurring custom engagement into a fixed-scope, fixed-price productized service with a landing page, intake form, and delivery SOP that any senior operator on the team can execute without the founder. Exit artifact: shipped productized offer + SOP-driven first delivery + measured unit economics.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Full SaaS productization - service stays human-delivered
- Multi-product launch - single service per playbook run

### Prerequisites

- Recurring custom engagement pattern across 3+ past clients
- Bench operator capable of delivering with SOP

## Success criteria

The playbook is done when:
- Named productized service with positioning
- Landing page + intake form live
- Delivery SOP executable by a non-founder operator
- Pricing tiers locked (retainer / project / fixed)
- First delivery completed using SOP only
- Unit-economics row updated

## Stages

### Stage 1: Niche the offer

**Intent:** Concrete ICP + outcome + price tier choice.

**Tasks:**
- Run niche evaluation against ICP
- Pick retainer vs project vs fixed
- Lock outcome statement

**Methodologies in chain:**
- `competitive-positioning` -> `pro/product/product-planning/competitive-positioning`
- `niche-evaluation` -> `solo/research/researcher/niche-evaluation`
- `ops-pricing-strategy` -> `solo/marketing/gtm-strategist/ops-pricing-strategy`
- `growth-brand-positioning` -> `pro/marketing/gtm-strategist/growth-brand-positioning`

**Outputs:**
- Niche + outcome doc
- Pricing model decision

**Decision gate:**
> Advance with a concrete outcome statement + price tier choice.

### Stage 2: Funnel + landing

**Intent:** Public landing + intake form + A/B baseline.

**Tasks:**
- Write hero + 5 sections
- Build intake form with qualifying questions
- Baseline 1 A/B test on price or hero

**Methodologies in chain:**
- `funnel-tactics-basics` -> `pro/marketing/conversion-optimizer/funnel-tactics-basics`

**Outputs:**
- Landing live
- Intake form live

**Decision gate:**
> Advance once landing + intake gets 1 qualified inbound.

### Stage 3: Delivery SOP + ops

**Intent:** Operator-runnable SOP, not founder-runnable.

**Tasks:**
- Author SOP per step
- Record one demo session
- Lock financial + success metrics

**Methodologies in chain:**
- `ops-customer-success-basics` -> `pro/marketing/gtm-strategist/ops-customer-success-basics`
- `ops-financial-basics` -> `pro/marketing/gtm-strategist/ops-financial-basics`
- `ops-upselling-cross-selling` -> `pro/marketing/gtm-strategist/ops-upselling-cross-selling`

**Outputs:**
- SOP doc
- Demo recording
- Metrics row

**Decision gate:**
> Advance once SOP passes 'an operator can deliver without me' test.

### Stage 4: First delivery

**Intent:** SOP-only delivery; measure margin + NPS.

**Tasks:**
- Operator delivers using SOP only
- Founder reviews after
- Capture margin + NPS

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- First paid delivery completed
- Margin + NPS

**Decision gate:**
> Required: first delivery completed with SOP only AND margin acceptable.

## Common pitfalls

- Founder shadow-delivers and pretends the SOP worked - kills the bench leverage
- Pricing in hours - undoes the productize move
- Treating landing live as launch - first paid delivery is launch

## Quality checklist (self-review)

- Did the operator deliver without me touching it?
- Is the pricing in outcomes, not hours?
- Is margin measured, not just revenue?

## Related playbooks

- `productize-a-service-offering`
- `agency-to-recurring-revenue-transition`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **productized-service-design** (tier `pro`, blocks stage 1) -- Niche-the-offer stage needs a structured design canvas
- **agency-pricing-tiers** (tier `pro`, blocks stage 1) -- Niche-the-offer stage needs a pricing-tiers reference for fixed-price services
- **retainer-vs-project-rubric** (tier `pro`, blocks stage 1) -- Niche-the-offer stage needs an explicit rubric for retainer vs project
- **service-delivery-sop-template** (tier `pro`, blocks stage 3) -- Delivery-SOP stage needs a default SOP template

## CLI usage

```
faion get-content productize-one-service-from-custom-to-fixed --format md       # human-readable rendering
faion get-content productize-one-service-from-custom-to-fixed --format context  # agent-optimised context bundle
faion get-content productize-one-service-from-custom-to-fixed --format json     # raw structured form
```
