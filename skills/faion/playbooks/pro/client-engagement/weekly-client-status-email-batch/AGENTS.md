---
slug: weekly-client-status-email-batch
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
summary: One sitting to 3-8 client status emails sent, each anchored to scope + next milestone, scope-creep flagged.
content_id: d5378288306f9516
methodology_refs:
  - scope-management
  - change-control
  - stakeholder-engagement
  - business-storytelling
---

# Weekly client status email batch

**Playbook slug:** `weekly-client-status-email-batch`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

One sitting to 3-8 client status emails sent, each anchored to scope + next milestone, scope-creep flagged.

## Scope

Founder writes status emails for all active retainers + projects in one sitting. Output: 3-8 status emails sent, each anchored to scope + next milestone, scope-creep flagged. Exit artifact: every active client received a status email by Friday EOD with a structured update.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Long-form quarterly business reviews - separate ritual
- Marketing newsletters to clients - distinct cadence

### Prerequisites

- Active retainer + project list with sponsor emails
- Per-client scope + next-milestone notes

## Success criteria

The playbook is done when:
- Every active client emailed by Friday EOD
- Each email anchored to scope + next milestone
- Scope-creep risks flagged inline
- Founder spent 90 min or less in single batch session

## Stages

### Stage 1: Prep facts

**Intent:** Pull per-client deltas before writing anything.

**Tasks:**
- Pull last week's delivered items per account
- List next milestone + owner per account
- Tag scope-creep risks

**Methodologies in chain:**
- `scope-management` -> `pro/pm/project-manager/scope-management`
- `change-control` -> `pro/pm/project-manager/change-control`
- `stakeholder-engagement` -> `pro/pm/project-manager/stakeholder-engagement`

**Outputs:**
- Per-client fact card

**Decision gate:**
> Advance once every client has a fact card.

### Stage 2: Draft in batch

**Intent:** One sitting, structured template, no Slack.

**Tasks:**
- Use email template per account
- Anchor every paragraph to scope + milestone
- Flag scope-creep risks in writing

**Methodologies in chain:**
- `business-storytelling` -> `solo/comms/communicator/business-storytelling`

**Outputs:**
- Email drafts per account

**Decision gate:**
> Advance once every client has a draft.

### Stage 3: Send + log

**Intent:** Send Friday; log scope-creep follow-ups for Monday review.

**Tasks:**
- Send all emails in one session
- Log scope-creep risks for Monday review
- Calendar any follow-up calls

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Emails sent
- Scope-creep risk log

**Decision gate:**
> Required: 100% of active clients emailed by Friday EOD.

## Common pitfalls

- Writing scope-creep euphemisms instead of flagging it - invites silent drift
- Skipping a client because 'nothing happened' - silence reads as trouble
- Letting the batch slip past Friday - clients judge timeliness

## Quality checklist (self-review)

- Did every email map to a scope item and a milestone?
- Did I flag scope-creep in writing, or only in my head?
- Did I actually batch, or did I context-switch?

## Related playbooks

- `monday-lead-pipeline-review`
- `weekly-status-report`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **client-status-email-template-agency** (tier `pro`, blocks stage 2) -- Draft-in-batch stage needs a tested status-email template
- **scope-creep-email-language-pack** (tier `pro`, blocks stage 2) -- Draft-in-batch stage needs reusable language for flagging scope creep
- **scope-creep-management** (tier `pro`, blocks stage 1) -- Prep-facts stage references scope-creep-management playbook not yet ported to v2 manifest
- **weekly-status-report** (tier `pro`, blocks stage 2) -- Draft-in-batch stage references weekly-status-report playbook not yet ported to v2 manifest

## CLI usage

```
faion get-content weekly-client-status-email-batch --format md       # human-readable rendering
faion get-content weekly-client-status-email-batch --format context  # agent-optimised context bundle
faion get-content weekly-client-status-email-batch --format json     # raw structured form
```
