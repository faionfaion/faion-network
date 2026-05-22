---
slug: customer-support-inbox-sweep
tier: solo
group: launch-operations
persona: P1
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Unread customer messages → zero unread + top 3 themes promoted to product feedback.
content_id: 396d6617f4333697
methodology_refs:
  - active-listening
  - stakeholder-communication
  - ops-customer-support
  - mom-test
  - continuous-discovery
  - feedback-management
  - backlog-management
---

# Customer support inbox sweep (2x weekly)

**Playbook slug:** `customer-support-inbox-sweep`  
**Tier:** solo  
**Complexity:** light  
**Persona:** P1 — Solo SaaS Builder

## Intent

Unread customer messages → zero unread + top 3 themes promoted to product feedback.

## Scope

2x weekly 30-minute sweep: every ticket resolved or scheduled, top 3 themes pushed into product feedback, churn signals flagged, FAQ updated where the same answer was given twice. Exit artifact is inbox-zero + updated FAQ.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Major feature decisions from support — escalate to scoping session
- Refund processing policy changes — handled in launch-operations refund playbook

### Prerequisites

- Support inbox routed (email, Crisp, or similar)
- FAQ page exists

## Success criteria

The playbook is done when:
- Zero unread tickets at end of sweep
- Top 3 themes added to product backlog
- Churn signals tagged in CRM
- FAQ updated for any repeat question

## Stages

### Stage 1: Read

**Intent:** Read every ticket; tag by intent + sentiment.

**Tasks:**
- Read all unread tickets
- Tag: question / bug / feature / churn / refund
- Note any repeat question

**Methodologies in chain:**
- `active-listening` → `solo/comms/communicator/active-listening`
- `stakeholder-communication` → `solo/comms/communicator/stakeholder-communication`
- `ops-customer-support` → `solo/marketing/gtm-strategist/ops-customer-support`

**Outputs:**
- Tagged ticket list

**Decision gate:**
> Advance once all unread are tagged. Refuse to skim — sentiment shifts get missed.

### Stage 2: Respond

**Intent:** Resolve or schedule every ticket. No silent ignores.

**Tasks:**
- Answer with FAQ link where applicable
- Schedule callbacks for >5min asks
- Tag churn-risk tickets red

**Methodologies in chain:**
- `mom-test` → `solo/comms/communicator/mom-test`

**Outputs:**
- All tickets resolved or scheduled

**Decision gate:**
> Advance when inbox is zero. Stay if any ticket is 'I'll get back to it'.

### Stage 3: Promote

**Intent:** Top 3 themes → product backlog. FAQ updated.

**Tasks:**
- Identify top 3 themes from this week
- Add backlog entries with quotes
- Update FAQ for repeat questions

**Methodologies in chain:**
- `continuous-discovery` → `solo/product/product-manager/continuous-discovery`
- `feedback-management` → `solo/product/product-operations/feedback-management`
- `backlog-management` → `solo/product/product-manager/backlog-management`

**Outputs:**
- 3 backlog entries
- FAQ diff

**Decision gate:**
> Required output: 3 backlog items + FAQ diff. Without this, support stays a black hole.

## Common pitfalls

- Sweeping daily and burning out — 2x/week is the cadence
- Treating every feature request as a roadmap input — filter by theme convergence

## Quality checklist (self-review)

- Did the top 3 themes actually land in the backlog, or in a 'maybe' note?
- Did I answer the same question twice without updating FAQ?

## Related playbooks

- `friday-bug-bash-triage`
- `sunday-roadmap-ritual`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-support-sla-template** (tier `solo`, blocks stage 2) — Respond stage needs SLA template scoped to one operator
- **verbatim-to-backlog-pattern** (tier `solo`, blocks stage 3) — Promote stage needs pattern for turning customer quotes into backlog items

## CLI usage

```
faion get-content customer-support-inbox-sweep --format md       # human-readable rendering
faion get-content customer-support-inbox-sweep --format context  # agent-optimised context bundle
faion get-content customer-support-inbox-sweep --format json     # raw structured form
```
