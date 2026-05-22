---
slug: sprint-planning-prep-with-engineering
tier: solo
group: role-product-manager
persona: role-product-manager
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Sprint top-N ranked, each item is acceptance-criteria + story-pointed-ready, dependencies surfaced; the planning meeting runs in 45 minutes instead of 2 hours.
content_id: 28d55887c41bbb19
methodology_refs:
  - kanban-scaled-agile-ceremonies
  - scrum-ceremonies
  - stakeholder-management
  - linear-issue-tracking
  - backlog-management
  - feature-prioritization-rice
---

# Sprint planning prep with engineering

## Context

Sprint top-N ranked, each item is acceptance-criteria + story-pointed-ready, dependencies surfaced; the planning meeting runs in 45 minutes instead of 2 hours.

Tier: **solo**. Complexity: **medium**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Draft top-N fits realistic capacity.
- Every shortlisted item has acceptance criteria.
- Every dependency has an owner.
- Walk-in 1-pager sent 24h ahead.

## Steps

### 1. Pre-rank

Bring a draft top-N before planning.

Tasks:
- Pull RICE-scored backlog top 15.
- Trim to top N that fits realistic capacity.
- Note carry-over items from last sprint.

Outputs:
- Draft top-N list.

Decision gate: Advance when the draft list fits a realistic capacity estimate.

### 2. Sharpen acceptance criteria

Every item must be AC-ready before the meeting.

Tasks:
- For each item, write AC in given/when/then form.
- Flag items that fail an AC quality check.
- Send the flagged items back to refinement.

Outputs:
- AC-ready item list.

Decision gate: Advance when every shortlisted item has AC.

### 3. Surface dependencies

Cross-team or cross-item dependencies should not surprise planning.

Tasks:
- Mark cross-team dependencies on each item.
- Reach out to each dependency owner ahead of planning.
- Note any item blocked by an external dependency.

Outputs:
- Dependency annotations.

Decision gate: Advance when every dependency has an owner and an expected resolution date.

### 4. Pre-size

Get a rough story point read before the room.

Tasks:
- Walk top 5 items with the tech lead pre-meeting.
- Capture initial estimates as a sanity check.
- Re-trim the top-N if estimates blow capacity.

Outputs:
- Pre-sized top-N.

Decision gate: Advance when capacity vs estimate has a realistic margin.

### 5. Walk-in deck

Show up to planning with a 1-pager.

Tasks:
- Build a 1-page walk-in: goal, top-N, dependencies, risks.
- Send the 1-pager 24h ahead of the meeting.
- Open the meeting by reading the 1-pager.

Outputs:
- Sprint walk-in 1-pager.

Decision gate: Required: the planning meeting opens with the 1-pager on screen.

## Decision points

- Story points vs t-shirt sizes — points for stable teams; t-shirts for new or volatile teams.
- Carry-over vs reset — carry over only if the original goal still holds; otherwise reset and re-decide.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/kanban-scaled-agile-ceremonies`
- `pro/pm/pm-agile/scrum-ceremonies`
- `pro/product/product-manager/stakeholder-management`
- `solo/pm/pm-agile/linear-issue-tracking`
- `solo/product/product-manager/backlog-management`
- `solo/product/product-manager/feature-prioritization-rice`
- `solo/product/product-operations/backlog-management`
