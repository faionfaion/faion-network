---
slug: quarterly-retainer-review-per-client
tier: pro
group: client-engagement
persona: P5
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Per retainer client every quarter to confirmed renewal, scope adjustment, or planned offboarding.
content_id: 1846eb4c624451b8
methodology_refs:
  - ops-customer-success-metrics
  - benefits-realization
  - ops-upselling-cross-selling
  - stakeholder-engagement-advanced
  - project-closure
  - difficult-conversations
  - negotiation
---

# Quarterly retainer review per client

**Playbook slug:** `quarterly-retainer-review-per-client`
**Tier:** pro
**Complexity:** deep
**Persona:** P5 -- Micro-agency founder

## Intent

Per retainer client every quarter to confirmed renewal, scope adjustment, or planned offboarding.

## Scope

Founder runs a 45-minute structured review with each retainer client every quarter. Output: confirmed renewal, scope adjustment, or planned offboarding. Exit artifact: per-client review pack + signed renewal / scope-change / offboarding note.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Full QBR for project-based clients - separate playbook
- New-business pitch within the meeting - never mix

### Prerequisites

- Retainer client with 1+ quarter under contract
- Health + outcome data captured monthly

## Success criteria

The playbook is done when:
- Per-client health score updated
- Retainer renewal / scope change / offboarding decision logged
- Updated scope or signed offboarding note in writing
- Client commits one next-quarter outcome

## Stages

### Stage 1: Score health

**Intent:** Per-client signal: outcomes, friction, satisfaction.

**Tasks:**
- Pull last quarter's outcomes
- Apply health scorecard
- Tag retention risk + upsell signal

**Methodologies in chain:**
- `ops-customer-success-metrics` -> `pro/marketing/gtm-strategist/ops-customer-success-metrics`
- `benefits-realization` -> `pro/pm/project-manager/benefits-realization`

**Outputs:**
- Health score row

**Decision gate:**
> Advance once score + tags assigned.

### Stage 2: Prep + run review

**Intent:** 45 min: outcomes, gaps, next-quarter, ask.

**Tasks:**
- Draft review deck
- Schedule meeting with sponsor
- Run review with structured script

**Methodologies in chain:**
- `ops-upselling-cross-selling` -> `pro/marketing/gtm-strategist/ops-upselling-cross-selling`
- `stakeholder-engagement-advanced` -> `pro/pm/project-manager/stakeholder-engagement-advanced`

**Outputs:**
- Review deck
- Meeting notes

**Decision gate:**
> Advance after meeting held with sponsor decision direction.

### Stage 3: Decide + paper

**Intent:** Renew, change scope, or offboard - in writing.

**Tasks:**
- Apply renewal decision rule
- Paper any scope change
- Write offboarding plan if needed

**Methodologies in chain:**
- `project-closure` -> `pro/pm/project-manager/project-closure`
- `difficult-conversations` -> `solo/comms/communicator/difficult-conversations`
- `negotiation` -> `solo/comms/communicator/negotiation`

**Outputs:**
- Signed renewal or scope change
- Offboarding plan if applicable

**Decision gate:**
> Required: written outcome for every retainer reviewed.

## Common pitfalls

- Auto-renewing without a review - kills upsell + lets churn fester
- Skipping the offboarding paper trail - clients drift back resentful
- Letting the review drift into 'how is it going' chat

## Quality checklist (self-review)

- Did the client commit a next-quarter outcome?
- Is the renewal / change paper signed?
- If offboarding, is the wind-down plan dated?

## Related playbooks

- `quarter-end-retention-review`
- `weekly-client-status-email-batch`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **quarterly-retainer-review-script** (tier `pro`, blocks stage 2) -- Prep-and-run-review stage needs a 45-min script
- **client-health-scorecard-agency** (tier `pro`, blocks stage 1) -- Score-health stage needs a scorecard tailored to agency retainers
- **retainer-renewal-decision-rule** (tier `pro`, blocks stage 3) -- Decide-and-paper stage needs an explicit decision rule
- **scope-creep-management** (tier `pro`, blocks stage 3) -- Decide-and-paper stage references scope-creep-management playbook not yet ported to v2 manifest
- **statement-of-work** (tier `pro`, blocks stage 3) -- Decide-and-paper stage references statement-of-work playbook not yet ported to v2 manifest

## CLI usage

```
faion get-content quarterly-retainer-review-per-client --format md       # human-readable rendering
faion get-content quarterly-retainer-review-per-client --format context  # agent-optimised context bundle
faion get-content quarterly-retainer-review-per-client --format json     # raw structured form
```
