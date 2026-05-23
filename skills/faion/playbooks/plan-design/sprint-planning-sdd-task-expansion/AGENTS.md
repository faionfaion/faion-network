# Sprint planning with SDD task expansion (bi-weekly)

**Playbook slug:** `sprint-planning-sdd-task-expansion`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Spec-ready stories → SDD feature folders with spec.md + design.md + implementation-plan.md broken into TASK_*.md files.

## Scope

Bi-weekly sprint planning. Spec-ready stories that came out of grooming become SDD feature folders under `.aidocs/in-progress/<feature>/`: spec.md + design.md (where complexity demands) + implementation-plan.md broken into TASK_*.md files in `tasks/todo/`. Capacity is decided from team velocity and complexity tags — token estimates only, no time estimates. The tracker mirrors the SDD layout.

### What this playbook covers

Four stages that turn spec-ready backlog into committed work. The chain enforces the *no-time-estimates* and *promotion-gate* rules: stories may not enter `todo/` until each task is materialised as its own self-contained file. The tracker mirrors SDD — never the other way around.

### Non-goals

- Spec/design authoring from scratch — see `rfc-to-production-feature-delivery`
- Daily execution — see `daily-standup-ai-prebrief`
- Quarterly OKR setting — see `quarter-planning-okr-reset`

### Prerequisites

- Backlog grooming completed in the same week
- SDD feature directory layout convention adopted (backlog → todo → in-progress → done)
- Token-budget heuristic agreed by team

## Success criteria

The playbook is done when:
- Each selected story has spec.md + (where needed) design.md
- `implementation-plan.md` broken into TASK_*.md files in `tasks/todo/`
- Capacity confirmed from velocity + complexity tags
- Promotion-gate checklist signed off per feature
- Tracker mirrors the SDD folder layout

## Stages

### Stage 1: Promote spec-ready stories

**Intent:** Stories chosen from backlog get promoted into SDD feature folders.

**Methodologies in chain:**
- `task-spec-kit-three-step` → `geek/sdlc-ai/task-spec-kit-three-step`
- `task-agent-drafts-spec-before-coding` → `geek/sdlc-ai/task-agent-drafts-spec-before-coding`
- `template-spec` → `solo/sdd/sdd-planning/template-spec`
- `writing-specifications` → `solo/sdd/sdd/writing-specifications`

**Decision gate:**
> Advance once each promoted story has a spec.md and passes DoR. No promotion without it.

### Stage 2: Design where needed

**Intent:** Features touching cross-service boundaries get a design.md.

**Methodologies in chain:**
- `template-design` → `solo/sdd/sdd-planning/template-design`
- `writing-design-documents` → `solo/sdd/sdd/writing-design-documents`

**Decision gate:**
> Advance when every cross-service feature has a design.md AND every isolated feature has an explicit waiver in the spec.

### Stage 3: Expand to tasks

**Intent:** implementation-plan.md becomes TASK_*.md files in `tasks/todo/`.

**Methodologies in chain:**
- `template-task` → `solo/sdd/sdd-planning/template-task`
- `writing-implementation-plans` → `solo/sdd/sdd/writing-implementation-plans`
- `impl-plan-100k-rule` → `solo/sdd/sdd-planning/impl-plan-100k-rule`
- `task-creation-parallelization` → `solo/sdd/sdd/task-creation-parallelization`
- `tracker-linear-agent-as-assignee` → `geek/sdlc-ai/tracker-linear-agent-as-assignee`

**Decision gate:**
> Advance once every promoted feature has a `tasks/todo/` tree with self-contained task files.

### Stage 4: Decide capacity + commit

**Intent:** Velocity + complexity tags fit inside confirmed capacity; sprint commit posted.

**Methodologies in chain:**
- `predictive-analytics-pm` → `pro/pm/pm-agile/predictive-analytics-pm`
- `raci-matrix` → `pro/pm/pm-agile/raci-matrix`
- `scrum-ceremonies` → `pro/pm/pm-agile/scrum-ceremonies`
- `value-stream-management` → `pro/pm/pm-agile/value-stream-management`

**Decision gate:**
> Required: sprint commit signed off. Overcommitting at this gate = guaranteed mid-sprint scope cut.

## Common pitfalls

- Promoting stories without spec.md — task files become guesswork
- Time estimates sneaking in — violates the No-Time-Estimates rule
- Skipping design.md on a cross-service feature — bites at QA stage
- Tracker drifts from SDD layout — devs lose source of truth

## Quality checklist (self-review)

- Does every task have a self-contained TASK_*.md?
- Is the sprint commit reachable given last 2 sprints' velocity?
- Does each spec.md pass the DoR checklist?

## Related playbooks

- `backlog-grooming-pm-tech-lead`
- `rfc-to-production-feature-delivery`
- `quarter-planning-okr-reset`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **sprint-capacity-from-complexity-tags** (tier `geek`, blocks stage 4) — Capacity stage needs an explicit method to translate complexity tags into capacity without time estimates
- **sdd-promotion-gate-checklist** (tier `geek`, blocks stage 1) — Promote stage needs the canonical backlog → todo promotion checklist

## CLI usage

```
faion get-content sprint-planning-sdd-task-expansion --format md       # human-readable rendering
faion get-content sprint-planning-sdd-task-expansion --format context  # agent-optimised context bundle
faion get-content sprint-planning-sdd-task-expansion --format json     # raw structured form
```
