---
slug: backlog-grooming-prioritization-session
tier: solo
group: role-product-manager
persona: role-product-manager
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Backlog under 100 items, every item has an owner plus score plus tag, stale items archived; the top-20 ready-to-pull queue exists.
content_id: dac47667a1dd03dd
methodology_refs:
  - reporting-basics
  - stakeholder-management
  - backlog-management
  - feature-prioritization-moscow
  - feature-prioritization-rice
  - okr-setting
---

# Backlog grooming and prioritization session

## Context

Backlog under 100 items, every item has an owner plus score plus tag, stale items archived; the top-20 ready-to-pull queue exists.

Tier: **solo**. Complexity: **medium**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Backlog under 100 items.
- Every item has owner, tag, and score.
- Top-20 ready-to-pull queue exists.
- Graveyard has one-line rationale per item.

## Steps

### 1. Audit size

Refuse to groom past 100 items.

Tasks:
- Count current backlog items.
- Identify items older than 90 days with no movement.
- Move stale items to a graveyard.

Outputs:
- Backlog size after archive.

Decision gate: Advance when the backlog is under 100 items.

### 2. Tag + own

Every item gets a theme tag and an owner.

Tasks:
- Apply theme tags (max 12).
- Assign an owner per item.
- Reject items without an owner — close or assign.

Outputs:
- Tagged + owned backlog.

Decision gate: Advance when every item has a tag and an owner.

### 3. Score

Run MoSCoW pass; RICE for the top quartile.

Tasks:
- MoSCoW the full backlog quickly.
- RICE the top 25 items only.
- Note the OKR each item ties to.

Outputs:
- Scored backlog.

Decision gate: Advance when every item has a MoSCoW class.

### 4. Top-20 queue

Build a ready-to-pull queue.

Tasks:
- Pull the top 20 by score.
- Confirm each has AC + dependencies surfaced.
- Mark each 'ready to pull'.

Outputs:
- Top-20 ready queue.

Decision gate: Advance when 20 items pass the ready definition.

### 5. Graveyard rationale

Make 'never' loud so it does not return.

Tasks:
- For every archived item, write a one-line rationale.
- File the graveyard list separately from active backlog.
- Schedule a quarterly graveyard scan.

Outputs:
- Graveyard log with rationale.

Decision gate: Required: every graveyard item has a one-line reason.

## Decision points

- Archive vs delete — archive (graveyard) preserves rationale; delete only for true duplicates.
- MoSCoW vs RICE depth — MoSCoW everywhere; RICE only on the top quartile worth deeper effort.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/reporting-basics`
- `pro/product/product-manager/stakeholder-management`
- `solo/product/product-manager/backlog-management`
- `solo/product/product-manager/feature-prioritization-moscow`
- `solo/product/product-manager/feature-prioritization-rice`
- `solo/product/product-manager/okr-setting`
- `solo/product/product-operations/backlog-management`
