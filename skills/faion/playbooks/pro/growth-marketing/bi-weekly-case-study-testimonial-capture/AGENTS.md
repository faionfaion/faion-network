---
slug: bi-weekly-case-study-testimonial-capture
tier: pro
group: growth-marketing
persona: P5
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Every fortnight to one quotable result captured (case study or 1-2 sentence testimonial) with permission, in reusable format.
content_id: ff45655c6455f76e
methodology_refs:
  - retention-strategies
  - growth-conversion-optimization
  - ops-customer-success-basics
  - stakeholder-communication
  - growth-content-marketing
  - growth-customer-testimonials
---

# Bi-weekly case-study / testimonial capture

**Playbook slug:** `bi-weekly-case-study-testimonial-capture`
**Tier:** pro
**Complexity:** light
**Persona:** P5 -- Micro-agency founder

## Intent

Every fortnight to one quotable result captured (case study or 1-2 sentence testimonial) with permission, in reusable format.

## Scope

Founder captures one quotable result per fortnight from a happy client. Output: short case study or 1-2 sentence testimonial, with permission, in reusable format. Exit artifact: testimonial + permission + one media asset (logo or quote card).

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Long-form case-study production - separate motion
- Paid endorsements / affiliate quotes - distinct workflow

### Prerequisites

- Active book of clients with measurable outcomes
- Testimonial microsurvey template

## Success criteria

The playbook is done when:
- 1 quote captured per fortnight
- Written permission on file
- Quote tied to a measurable outcome
- Reusable asset (logo / quote card / 30-sec video) saved

## Stages

### Stage 1: Pick the win

**Intent:** Pick the most measurable, repeatable win from the last 2 weeks.

**Tasks:**
- Scan QBR / status notes for outcomes
- Pick one with the cleanest metric
- Tag it to a content pillar

**Methodologies in chain:**
- `retention-strategies` -> `pro/marketing/growth-marketer/retention-strategies`
- `growth-conversion-optimization` -> `pro/marketing/conversion-optimizer/growth-conversion-optimization`
- `ops-customer-success-basics` -> `pro/marketing/gtm-strategist/ops-customer-success-basics`

**Outputs:**
- Win candidate

**Decision gate:**
> Advance once the win has a number tied to it.

### Stage 2: Ask + capture

**Intent:** Microsurvey + permission in same touch.

**Tasks:**
- Send 3-question microsurvey to the sponsor
- Ask for written permission
- Offer 3 quote-length options

**Methodologies in chain:**
- `stakeholder-communication` -> `solo/comms/communicator/stakeholder-communication`
- `growth-content-marketing` -> `solo/marketing/content-marketer/growth-content-marketing`
- `growth-customer-testimonials` -> `solo/marketing/content-marketer/growth-customer-testimonials`

**Outputs:**
- Returned microsurvey
- Permission note

**Decision gate:**
> Advance only with written permission on file.

### Stage 3: Package + log

**Intent:** Make it reusable across landing, deck, social.

**Tasks:**
- Format quote in 3 lengths (1-line, 3-line, 100-word)
- Generate a quote card / logo block
- Save in case-study library

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Reusable asset
- Library entry

**Decision gate:**
> Required: asset saved in library + tagged to pillar.

## Common pitfalls

- Capturing fluffy quotes ('great team!') - useless on landing pages
- Skipping the permission step - re-work later
- Storing assets in Slack - lost within a month

## Quality checklist (self-review)

- Does the quote include a number?
- Is permission in writing?
- Is the asset findable in 3 clicks from the library?

## Related playbooks

- `weekly-linkedin-positioning-post`
- `proposal-customization-from-base-template`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **testimonial-capture-microsurvey** (tier `pro`, blocks stage 2) -- Ask-and-capture stage needs a 3-question microsurvey template
- **case-study-three-format-template** (tier `pro`, blocks stage 3) -- Package-and-log stage needs a 3-length quote/case-study template

## CLI usage

```
faion get-content bi-weekly-case-study-testimonial-capture --format md       # human-readable rendering
faion get-content bi-weekly-case-study-testimonial-capture --format context  # agent-optimised context bundle
faion get-content bi-weekly-case-study-testimonial-capture --format json     # raw structured form
```
