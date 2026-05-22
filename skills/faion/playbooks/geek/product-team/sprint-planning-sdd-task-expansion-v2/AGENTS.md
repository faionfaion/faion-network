---
slug: sprint-planning-sdd-task-expansion-v2
tier: geek
group: product-team
persona: p6-product-dev-team
goal: operate-ritual
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Spec-ready stories from grooming become SDD feature folders: spec.md + design.md (where needed) + implementation-plan.md broken into TASK_*.md files. Capacity decided from team velocity and complex..."
content_id: c2cd9b279bd3780a
methodology_refs:
  - task-agent-drafts-spec-before-coding
  - task-spec-kit-three-step
  - tracker-linear-agent-as-assignee
  - predictive-analytics-pm
  - raci-matrix
  - scrum-ceremonies
  - value-stream-management
  - impl-plan-100k-rule
  - template-design
  - template-spec
  - template-task
  - task-creation-parallelization
  - writing-design-documents
  - writing-implementation-plans
  - writing-specifications
---

# Sprint planning with SDD task expansion (bi-weekly)

## Context

Spec-ready stories from grooming become SDD feature folders: spec.md + design.md (where needed) + implementation-plan.md broken into TASK_*.md files. Capacity decided from team velocity and complexity tags. No time estimates — token/complexity only.

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Pick the Sprint Goal

One outcome the sprint exists for.

Tasks:
- PM proposes 1-2 sprint goal candidates tied to quarterly outcomes
- Team votes on the goal that fits capacity
- Write the goal and the success signal

Outputs:
- goal candidate list
- team vote
- written goal + signal

Decision gate: Advance only when one written goal is agreed.

### 2. Expand Tasks (SDD)

Each story becomes a self-contained task file.

Tasks:
- Pull ready stories from the backlog
- Expand each story into SDD task files in tasks/todo/
- Verify each task has spec links, AC, and complexity

Outputs:
- task files in tasks/todo/
- spec-link review
- complexity per task

Decision gate: Advance only when every selected story has materialized as task files.

### 3. Commit Capacity

Match scope to people, not hope.

Tasks:
- Sum complexity vs available capacity
- Cut the bottom of the list until it fits
- Lock the committed list

Outputs:
- capacity sum
- cut list
- committed task list

Decision gate: Advance only when committed scope ≤ capacity.

### 4. Kickoff

Start the sprint clean.

Tasks:
- Hold the planning close-out with the committed list
- Assign owners to each task
- Set the demo and retro dates

Outputs:
- close-out notes
- task owners assigned
- demo + retro calendar

Decision gate: Required output: a written, owned sprint backlog.

## Decision points

- Stage 1 (Pick the Sprint Goal): Advance only when one written goal is agreed.
- Stage 2 (Expand Tasks (SDD)): Advance only when every selected story has materialized as task files.
- Stage 3 (Commit Capacity): Advance only when committed scope ≤ capacity.
- Stage 4 (Kickoff): Required output: a written, owned sprint backlog.

## References

- `task-agent-drafts-spec-before-coding`
- `task-spec-kit-three-step`
- `tracker-linear-agent-as-assignee`
- `predictive-analytics-pm`
- `raci-matrix`
- `scrum-ceremonies`
- `value-stream-management`
- `impl-plan-100k-rule`
- `template-design`
- `template-spec`
- `template-task`
- `task-creation-parallelization`
- `writing-design-documents`
- `writing-implementation-plans`
- `writing-specifications`

Gaps (status: draft until empty):
- `sprint-capacity-from-complexity-tags` (see `gaps[]` in `playbook.yaml`)
- `sdd-promotion-gate-checklist` (see `gaps[]` in `playbook.yaml`)
