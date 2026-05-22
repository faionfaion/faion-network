---
slug: monday-lead-pipeline-review
tier: pro
group: client-engagement
persona: P5
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Once a week to updated sales pipeline + 3-5 next-step actions assigned per active deal.
content_id: 510dc469d569cdc7
methodology_refs:
  - aarrr-pirate-metrics
  - conversion-tracking
  - ops-customer-success-metrics
  - communications-management
---

# Monday lead-pipeline review

**Playbook slug:** `monday-lead-pipeline-review`
**Tier:** pro
**Complexity:** light
**Persona:** P5 -- Micro-agency founder

## Intent

Once a week to updated sales pipeline + 3-5 next-step actions assigned per active deal.

## Scope

Founder walks the sales pipeline once a week, decides which deals advance, which die, and what outreach happens this week. Output: updated pipeline + 3-5 next-step actions assigned. Exit artifact: pipeline doc with stage + decision + next-step per active deal.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Long-form weekly strategy review - atomic ritual only
- Outbound list-building - separate workflow

### Prerequisites

- Pipeline tracker (Notion, Airtable, HubSpot Free, Sheets)
- Last-week notes from prior pipeline review

## Success criteria

The playbook is done when:
- Each active deal has stage + decision + next-step
- Dead deals are killed in writing
- 5 or fewer next-step actions assigned for the week
- Pipeline metrics updated

## Stages

### Stage 1: Refresh metrics

**Intent:** Numbers first, opinions second.

**Tasks:**
- Pull current stage counts + conversion rates
- Note week-over-week deltas

**Methodologies in chain:**
- `aarrr-pirate-metrics` -> `pro/marketing/growth-marketer/aarrr-pirate-metrics`
- `conversion-tracking` -> `pro/marketing/growth-marketer/conversion-tracking`
- `ops-customer-success-metrics` -> `pro/marketing/gtm-strategist/ops-customer-success-metrics`

**Outputs:**
- Pipeline metrics snapshot

**Decision gate:**
> Advance when numbers refresh complete.

### Stage 2: Walk each deal

**Intent:** Triage each active deal: advance, kill, hold.

**Tasks:**
- Review every deal against last week's notes
- Apply kill rule to stuck deals
- Assign next-step per advancing deal

**Methodologies in chain:**
- `communications-management` -> `pro/pm/project-manager/communications-management`

**Outputs:**
- Per-deal verdict + next step

**Decision gate:**
> Each deal must have one of: advance / kill / explicit hold.

### Stage 3: Commit actions

**Intent:** 5 or fewer actions for the week, owned and timestamped.

**Tasks:**
- Pick top-5 next-steps
- Calendar block per action
- Send any waiting follow-ups today

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Action list with owner + day
- Follow-ups sent

**Decision gate:**
> Required: 5 or fewer actions, each calendar-blocked. If more, kill some deals.

## Common pitfalls

- Refusing to kill stuck deals - pipeline stays inflated but nothing advances
- Adding 15 actions every Monday - finishes none
- Skipping the kill rule because 'they might come back'

## Quality checklist (self-review)

- Did I actually kill at least one deal this quarter?
- Is every advancing deal on my calendar?
- Did I update the doc, or just look at it?

## Related playbooks

- `proposal-customization-from-base-template`
- `weekly-client-status-email-batch`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-pipeline-hygiene-15min** (tier `pro`, blocks stage 2) -- Walk-each-deal stage needs a 15-min hygiene script
- **founder-deal-kill-rule** (tier `pro`, blocks stage 2) -- Walk-each-deal stage needs an explicit kill rule
- **ltv-cac-attribution** (tier `pro`, blocks stage 1) -- Refresh-metrics stage references LTV/CAC attribution playbook not yet ported to v2 manifest

## CLI usage

```
faion get-content monday-lead-pipeline-review --format md       # human-readable rendering
faion get-content monday-lead-pipeline-review --format context  # agent-optimised context bundle
faion get-content monday-lead-pipeline-review --format json     # raw structured form
```
