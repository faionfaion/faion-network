# Template: Task File

## Summary

**One-sentence:** Generates a single executor-ready TASK_NNN.md file containing SDD refs, dep tree, requirement coverage, Given-When-Then AC, files-to-touch, and token budget.

**One-paragraph:** Fills the canonical TASK_NNN.md skeleton — the atomic execution unit a subagent reads and implements. Each task carries SDD References (spec/design/plan paths), Task Dependency Tree, Requirements Coverage (FR-X / AD-X inline), Objective, Dependencies, Acceptance Criteria (Given-When-Then), Technical Approach (numbered steps), Files (CREATE/MODIFY), Estimated Tokens, and post-execution sections for Implementation + Summary. Output validates against the schema in `content/02-output-contract.xml`.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'task file authoring' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- An implementation-plan.md has been approved and converted into discrete tasks.
- The task is intended for autonomous subagent execution (not narrative human work).
- The task can be completed by a single agent in one session (≤100k tokens).
- The parent feature lives under `.aidocs/features/<status>/<feature>/`.

## Skip If (ANY kills it)

- Implementation-plan is still draft — task scope will shift and the file is wasted.
- Research spike where the deliverable is a decision, not code — use a lighter note format.
- Task under ~5k tokens of work — overhead of full template outweighs the benefit.
- Manual human execution — humans need narrative description, not Given-When-Then AC.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved implementation-plan.md | markdown | `.aidocs/features/<status>/<feature>/implementation-plan.md` |
| Approved design.md | markdown | `.aidocs/features/<status>/<feature>/design.md` |
| Approved spec.md | markdown | `.aidocs/features/<status>/<feature>/spec.md` |
| Feature directory exists | filesystem | `.aidocs/features/<status>/<feature>/todo/` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/writing-implementation-plans` | Provides the plan rows that this template renders into task files. |
| `solo/sdd/sdd-planning/workflow-design-phase` | Defines the AD-X decisions referenced from each task. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the task file + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: load plan row → render header → fill AC → fill files → estimate tokens | ~700 |
| `content/05-examples.xml` | medium | Worked example: a filled task for adding a JWT refresh endpoint | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `render-task-skeleton` | sonnet | Mechanical template fill from plan row. |
| `synthesize-acceptance-criteria` | sonnet | Bounded Given-When-Then composition. |
| `cross-task-dependency-audit` | opus | Detect missing implicit deps via shared-file analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task.md` | Canonical TASK_NNN.md skeleton with all required sections. |
| `templates/task-lifecycle.sh` | Validates required sections before moving task between todo / in-progress / done. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-template-task.py` | Validate the task file artefact against the schema in `content/02-output-contract.xml`. | After subagent emits the task file, before the executor picks it up. |

## Related

- [[writing-implementation-plans]]
- [[workflow-design-phase]]
- [[workflows]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (plan approved, feature dir exists, task scope under one session) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether to emit a full task file or fall back to a lighter note.
