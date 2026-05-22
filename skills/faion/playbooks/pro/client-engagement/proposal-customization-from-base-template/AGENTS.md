---
slug: proposal-customization-from-base-template
tier: pro
group: client-engagement
persona: P5
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Qualified discovery call to scoped proposal + SOW + price, sent within one working day of decision.
content_id: 37caa2402eece84f
methodology_refs:
  - requirements-prioritization
  - solution-assessment
  - ops-upselling-cross-selling
  - ops-pricing-strategy
  - business-storytelling
  - growth-customer-testimonials
---

# Proposal customization from base template

**Playbook slug:** `proposal-customization-from-base-template`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

Qualified discovery call to scoped proposal + SOW + price, sent within one working day of decision.

## Scope

Founder turns a qualified discovery call into a sent proposal. Output: scoped proposal + SOW + price, sent within working day of decision. Exit artifact: signed-or-pending proposal in the deal record.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Multi-vendor RFP responses - separate workflow
- Free 'spec work' proposals - never offered

### Prerequisites

- Discovery verdict = 'propose'
- Versioned base proposal template

## Success criteria

The playbook is done when:
- Proposal personalized to lead's pain map
- Outcome-anchored pricing (not hours)
- SOW non-goals explicit
- Sent within 24h of discovery verdict
- Objection FAQ block included

## Stages

### Stage 1: Scope shaping

**Intent:** Convert pain map into priced outcomes.

**Tasks:**
- Prioritize must-have outcomes
- Score solution options against value
- Lock 3 explicit non-goals

**Methodologies in chain:**
- `requirements-prioritization` -> `pro/ba/business-analyst/requirements-prioritization`
- `solution-assessment` -> `pro/ba/business-analyst/solution-assessment`

**Outputs:**
- Scope decision doc

**Decision gate:**
> Advance with scope on one page + non-goals.

### Stage 2: Price

**Intent:** Outcome-anchored, defensible price.

**Tasks:**
- Pick fixed / tiered / retainer model
- Set price against value not hours
- Add an upsell tier intentionally

**Methodologies in chain:**
- `ops-upselling-cross-selling` -> `pro/marketing/gtm-strategist/ops-upselling-cross-selling`
- `ops-pricing-strategy` -> `solo/marketing/gtm-strategist/ops-pricing-strategy`

**Outputs:**
- Price card + tiers

**Decision gate:**
> Advance when price is defensible without quoting hours.

### Stage 3: Customize template

**Intent:** Personalize hero, results section, FAQ to this lead.

**Tasks:**
- Adapt hero + summary to lead's words
- Drop 2 case studies in same niche
- Add objection FAQ block

**Methodologies in chain:**
- `business-storytelling` -> `solo/comms/communicator/business-storytelling`
- `growth-customer-testimonials` -> `solo/marketing/content-marketer/growth-customer-testimonials`

**Outputs:**
- Customized proposal doc

**Decision gate:**
> Advance once draft passes 'a stranger could follow this' test.

### Stage 4: Send + log

**Intent:** Within 24h of discovery verdict; calendar the follow-up.

**Tasks:**
- Send via email + sales tool
- Calendar follow-up call in 3 days
- Log in pipeline with stage + reason

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Sent proposal
- Follow-up call booked

**Decision gate:**
> Required: sent within 24h. If late, flag root cause.

## Common pitfalls

- Padding the scope because the proposal feels 'too short'
- Quoting hours - invites scope creep and locks margin
- Sending without an explicit follow-up plan

## Quality checklist (self-review)

- Is the proposal personalized in the lead's language?
- Does the price defend itself without hours?
- Did I send within 24h, or did I drift?

## Related playbooks

- `discovery-call-run-45-min`
- `inbound-lead-to-signed-retainer`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **proposal-template-micro-agency-tiered** (tier `pro`, blocks stage 3) -- Customize-template stage needs a tiered proposal template
- **objection-faq-library** (tier `pro`, blocks stage 3) -- Customize-template stage needs a reusable objection FAQ library
- **scoping-workshop** (tier `pro`, blocks stage 1) -- Scope-shaping stage references scoping-workshop playbook not yet ported to v2 manifest
- **statement-of-work** (tier `pro`, blocks stage 2) -- Price stage references statement-of-work playbook not yet ported to v2 manifest

## CLI usage

```
faion get-content proposal-customization-from-base-template --format md       # human-readable rendering
faion get-content proposal-customization-from-base-template --format context  # agent-optimised context bundle
faion get-content proposal-customization-from-base-template --format json     # raw structured form
```
