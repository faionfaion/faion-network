---
slug: run-a-1-hour-backlog-grooming-session
tier: solo
group: role-project-manager
persona: role-project-manager
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Weekly grooming: top 20 backlog items are readable, sized, dependency-mapped. Exit: 2 sprints of well-formed work ready to pull."
content_id: 1b0b281a0cecf79e
methodology_refs:
  - scrum-ceremonies
  - schedule-development
  - scope-management
  - wbs-creation
  - work-breakdown-structure
  - jira-workflow-management
---

# Run a 1-hour backlog grooming session

## Context

Weekly grooming: top 20 backlog items are readable, sized, dependency-mapped. Exit: 2 sprints of well-formed work ready to pull.

Tier: **solo**. Complexity: **medium**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Top 20 walked and irrelevant flagged.
- Every item passes DoR or is sent back.
- Every item has a size or a 'needs split' tag.
- Every dependency has an owner.
- Ready queue sized for 2 sprints.

## Steps

### 1. Walk top 20

Walk the top 20 in the order they will be pulled.

Tasks:
- Sort the backlog by priority.
- Pull the top 20 into the grooming view.
- Tag any that lost relevance for removal.

Outputs:
- Top-20 grooming view.

Decision gate: Advance when 20 items are queued and irrelevant ones are flagged.

### 2. Readable?

Every item passes a 'definition of ready' check.

Tasks:
- For each item, confirm the description tells the why + the what.
- Add missing context; do not assume.
- Reject items that still cannot be read.

Outputs:
- Definition-of-ready pass results.

Decision gate: Advance when every item passes DoR or is sent back to refinement.

### 3. Sized?

Apply story points or t-shirt sizes.

Tasks:
- Size with the team via planning poker or async vote.
- Re-size items >XL or unclear.
- Note items that need to be split.

Outputs:
- Sized items.

Decision gate: Advance when every item has a size or a 'needs split' tag.

### 4. Dependencies?

Map cross-item or cross-team dependencies.

Tasks:
- Tag dependencies per item.
- Confirm dependency owners are aware.
- Note any item blocked by a missing dependency.

Outputs:
- Dependency annotations.

Decision gate: Advance when each dependency has an owner.

### 5. Ready queue

Build the 2-sprint ready queue.

Tasks:
- Promote items that pass readable + sized + dependency checks.
- Cap the ready queue at 2 sprints of work.
- Move overflow back to the wider backlog.

Outputs:
- 2-sprint ready queue.

Decision gate: Required: ready queue is sized for 2 sprints of capacity.

## Decision points

- Split vs leave-XL — split when the XL hides multiple value steps; leave it when the XL is a single integration step.
- Promote vs hold-back — hold back items whose dependencies are unowned even if their AC is ready.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/scrum-ceremonies`
- `pro/pm/pm-traditional/schedule-development`
- `pro/pm/pm-traditional/scope-management`
- `pro/pm/pm-traditional/wbs-creation`
- `pro/pm/pm-traditional/work-breakdown-structure`
- `pro/pm/project-manager/jira-workflow-management`
