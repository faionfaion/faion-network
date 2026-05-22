---
slug: customer-feedback-triage-from-intercompylon
tier: solo
group: role-product-manager
persona: role-product-manager
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: All inbound feature requests and complaints from the previous week routed into the backlog with severity, theme tag, and a verdict (now / later / never); the requester is acknowledged.
content_id: fabb70aaed42dd5a
methodology_refs:
  - feedback-management
  - stakeholder-management
  - feature-prioritization-moscow
  - feature-prioritization-rice
  - backlog-management
---

# Customer feedback triage from Intercom or Pylon

## Context

All inbound feature requests and complaints from the previous week routed into the backlog with severity, theme tag, and a verdict (now / later / never); the requester is acknowledged.

Tier: **solo**. Complexity: **light**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- All last-week feedback de-duped and tagged.
- Every item has theme + severity + verdict.
- Every requester acked within 5 business days.
- Graveyard rationale captured for 'never' items.

## Steps

### 1. Pull

Pull the previous week's feedback into one place.

Tasks:
- Filter Intercom/Pylon for last-week tickets.
- Export to a triage queue.
- De-duplicate verbatims with the same underlying ask.

Outputs:
- Triage queue with de-duped items.

Decision gate: Advance when the queue has no obvious duplicates.

### 2. Tag

Apply theme + severity.

Tasks:
- Assign each item a theme tag (max 12 themes total).
- Score severity (P0 broken trust → P3 nice-to-have).
- Tag the requester's plan + ARR.

Outputs:
- Tagged triage queue.

Decision gate: Advance when every item has theme + severity.

### 3. Score

Run a MoSCoW or RICE pass on the new items.

Tasks:
- Apply MoSCoW for fast directional sort.
- RICE only for the top quartile.
- Note any items already in flight.

Outputs:
- Scored queue.

Decision gate: Advance when every item has a score (Must/Should/Could/Won't, or a RICE number).

### 4. Verdict + route

Each item gets now / later / never plus a destination.

Tasks:
- File 'now' items to current sprint.
- File 'later' items to backlog with theme tag.
- File 'never' items to a graveyard with rationale.

Outputs:
- Backlog + graveyard with routed items.

Decision gate: Advance when every item has a verdict and a destination.

### 5. Acknowledge

Close the loop with the requester.

Tasks:
- Use a templated reply per verdict (now/later/never).
- Send within 5 business days of the original ticket.
- Log the ack on the ticket.

Outputs:
- Ack record per requester.

Decision gate: Required: every requester is acked, even on 'never'.

## Decision points

- MoSCoW vs RICE — MoSCoW for fast triage; RICE only for the top quartile worth scoring deeply.
- Now vs later vs never — 'never' is a real verdict; soft 'somedays' poison the backlog.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/product/product-manager/feedback-management`
- `pro/product/product-manager/stakeholder-management`
- `solo/product/product-manager/feature-prioritization-moscow`
- `solo/product/product-manager/feature-prioritization-rice`
- `solo/product/product-operations/backlog-management`
- `solo/product/product-operations/feedback-management`
