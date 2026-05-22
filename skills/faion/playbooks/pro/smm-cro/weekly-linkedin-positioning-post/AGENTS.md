---
slug: weekly-linkedin-positioning-post
tier: pro
group: smm-cro
persona: P5
goal: acquire-grow
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: One post per week to reinforce agency niche + earn 1-2 inbound replies per post.
content_id: 662a111e8c245cdf
methodology_refs:
  - growth-brand-positioning
  - growth-influencer-marketing
  - growth-content-marketing
  - business-storytelling
  - storytelling
  - growth-copywriting-fundamentals
  - instagram-basics
---

# Weekly LinkedIn positioning post

**Playbook slug:** `weekly-linkedin-positioning-post`
**Tier:** pro
**Complexity:** light
**Persona:** P5 -- Micro-agency founder

## Intent

One post per week to reinforce agency niche + earn 1-2 inbound replies per post.

## Scope

Founder publishes one LinkedIn / X post per week that reinforces agency niche + earns 1-2 inbound replies. Output: post drafted, scheduled, engagement plan. Exit artifact: published post + reply log + 1 follow-up DM.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Daily posting cadence - weekly only
- Paid LinkedIn ads - separate playbook

### Prerequisites

- ICP one-pager + 3-4 content pillars defined
- Personal LinkedIn / X profile aligned with agency positioning

## Success criteria

The playbook is done when:
- Post published each week
- Post anchored to a defined content pillar
- 1+ qualified reply within 72h
- 1 inbound DM sent as follow-up

## Stages

### Stage 1: Pick the angle

**Intent:** Pillar + insight + audience pain.

**Tasks:**
- Pick the content pillar for the week
- Surface 1 concrete insight from recent work
- Map to ICP's stated pain

**Methodologies in chain:**
- `growth-brand-positioning` -> `pro/marketing/gtm-strategist/growth-brand-positioning`
- `growth-influencer-marketing` -> `pro/marketing/gtm-strategist/growth-influencer-marketing`
- `growth-content-marketing` -> `solo/marketing/content-marketer/growth-content-marketing`

**Outputs:**
- Angle note

**Decision gate:**
> Advance once angle ties to a real pillar + lived insight.

### Stage 2: Draft

**Intent:** Hook + payoff + ask in 200 words or less.

**Tasks:**
- Write hook (15 words or less)
- Build payoff (insight, story, or number)
- End with an explicit ask or CTA

**Methodologies in chain:**
- `business-storytelling` -> `solo/comms/communicator/business-storytelling`
- `storytelling` -> `solo/comms/communicator/storytelling`
- `growth-copywriting-fundamentals` -> `solo/marketing/content-marketer/growth-copywriting-fundamentals`
- `instagram-basics` -> `pro/marketing/smm-manager/instagram-basics`

**Outputs:**
- Draft post

**Decision gate:**
> Advance only when hook stands alone without context.

### Stage 3: Schedule + engage

**Intent:** Publish at peak slot, reply to every comment for 24h.

**Tasks:**
- Schedule for peak slot
- Reply to comments in first 24h
- Send 1 thoughtful DM to a high-signal reply

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Published post
- Engagement log

**Decision gate:**
> Required: 1+ qualified reply + 1 follow-up DM logged.

## Common pitfalls

- Posting generic 'thought leadership' - invisible to ICP
- Skipping reply cadence - kills algorithmic distribution
- Treating likes as success - measure replies + DMs

## Quality checklist (self-review)

- Does the post embarrass me with how on-niche it is?
- Did I reply to every comment within 24h?
- Did I send the inbound DM, or just admire it?

## Related playbooks

- `bi-weekly-case-study-testimonial-capture`
- `monday-lead-pipeline-review`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **linkedin-founder-post-template** (tier `pro`, blocks stage 2) -- Draft stage needs a tested founder-post template (hook + payoff + ask)
- **agency-content-pillars-niche** (tier `pro`, blocks stage 1) -- Pick-the-angle stage needs a content-pillars worksheet tied to niche

## CLI usage

```
faion get-content weekly-linkedin-positioning-post --format md       # human-readable rendering
faion get-content weekly-linkedin-positioning-post --format context  # agent-optimised context bundle
faion get-content weekly-linkedin-positioning-post --format json     # raw structured form
```
