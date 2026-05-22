---
slug: monthly-competitor-scan
tier: solo
group: product-planning
persona: P1
goal: operate-ritual
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Stale competitive picture → sharper positioning + 1 ship + kill-list updates.
content_id: 2c2c67abaa111be1
methodology_refs:
  - market-researcher
  - researcher
  - topical-authority
  - business-storytelling
  - growth-copywriting-fundamentals
  - growth-landing-page-design
  - ops-pricing-strategy
  - backlog-management
---

# Monthly competitor and landscape scan

**Playbook slug:** `monthly-competitor-scan`  
**Tier:** solo  
**Complexity:** medium  
**Persona:** P1 — Solo SaaS Builder

## Intent

Stale competitive picture → sharper positioning + 1 ship + kill-list updates.

## Scope

Solo founder runs a 90-minute monthly scan: top 5 competitors re-audited, pricing & feature deltas captured, 1 positioning tweak shipped, kill-list updated for non-differentiating roadmap items. Exit artifact is positioning-diff log + shipped landing-page edit.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- New market entry research — separate niche-evaluation
- Full ICP rewrite — quarterly only

### Prerequisites

- Existing positioning statement
- Competitor list with URLs

## Success criteria

The playbook is done when:
- Top 5 competitors checked: pricing + 3 newest features
- Positioning diff captured with screenshots
- 1 positioning tweak shipped on landing
- Kill-list updated (removed items recorded)

## Stages

### Stage 1: Audit

**Intent:** Re-check pricing + features of top 5 competitors.

**Tasks:**
- Open each competitor pricing page
- Note feature deltas vs ours
- Screenshot positioning copy

**Methodologies in chain:**
- `market-researcher` → `solo/research/market-researcher`
- `researcher` → `solo/research/researcher`
- `topical-authority` → `solo/marketing/seo-manager/topical-authority`

**Outputs:**
- Competitor audit table

**Decision gate:**
> Advance when all 5 audited. Refuse partial — biases positioning.

### Stage 2: Diff

**Intent:** What changed in positioning vs our copy?

**Tasks:**
- Compare value-prop statements
- Identify our differentiation gap
- Note non-differentiating features in our roadmap

**Methodologies in chain:**
- `business-storytelling` → `solo/comms/communicator/business-storytelling`
- `growth-copywriting-fundamentals` → `solo/marketing/content-marketer/growth-copywriting-fundamentals`
- `growth-landing-page-design` → `solo/marketing/conversion-optimizer/growth-landing-page-design`
- `ops-pricing-strategy` → `solo/marketing/gtm-strategist/ops-pricing-strategy`

**Outputs:**
- Positioning diff doc

**Decision gate:**
> Advance when 1 actionable insight per competitor. Stay if findings are vague.

### Stage 3: Ship

**Intent:** 1 landing-page tweak + kill-list update.

**Tasks:**
- Edit landing-page copy with sharpest delta
- Remove non-diff items from roadmap
- Log decision

**Methodologies in chain:**
- `backlog-management` → `solo/product/product-manager/backlog-management`

**Outputs:**
- Landing-page diff
- Kill-list entry

**Decision gate:**
> Required output: shipped copy + kill-list entry. No 'we should do this' notes only.

## Common pitfalls

- Copying competitor positioning verbatim — kills differentiation
- Adding their features to our roadmap reflexively — should trigger Kill-list update, not Add

## Quality checklist (self-review)

- Did I cut something from the roadmap, or only add?
- Is the landing-page edit visible to a stranger, or cosmetic?

## Related playbooks

- `quarterly-persona-pricing-recal`
- `pmf-hunt-post-mvp`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **competitor-tracker-template-solo** (tier `solo`, blocks stage 1) — Audit stage needs ready-to-fill tracker for top-5-competitor cadence
- **positioning-diff-log** (tier `solo`, blocks stage 2) — Diff stage needs structured log to compare over time

## CLI usage

```
faion get-content monthly-competitor-scan --format md       # human-readable rendering
faion get-content monthly-competitor-scan --format context  # agent-optimised context bundle
faion get-content monthly-competitor-scan --format json     # raw structured form
```
