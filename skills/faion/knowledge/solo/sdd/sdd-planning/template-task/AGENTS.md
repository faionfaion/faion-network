# Template: Task File

## Summary

A fill-in-the-blanks template for TASK_NNN.md files — the atomic execution units that a subagent reads and implements. Each task file includes SDD References, Task Dependency Tree, Requirements Coverage (FR-X / AD-X inline), Objective, Dependencies, Acceptance Criteria (Given-When-Then), Technical Approach (numbered steps), Files (CREATE/MODIFY), Estimated Tokens, and sections for execution output.

## Why

Executor agents without a complete task file are forced to re-read the full SDD context on each run, wasting tokens and introducing inconsistency. A self-contained task file with inline FR/AD text, explicit dependency outputs, and testable ACs lets the executor proceed without external lookups, and makes the token budget predictable and enforceable (hard cap: 100k per task).

## When To Use

- Generating TASK_*.md files from an approved implementation plan.
- Converting implementation plan row stubs into standalone, self-contained task files.
- Ensuring the executing agent has all required context within a single file.
- Verifying completed tasks before marking them done — template defines the done state.

## When NOT To Use

- Before the implementation plan is approved — task scope will change and the file is wasted effort.
- For research spikes where the deliverable is a decision, not code — use a lighter note format.
- When a task takes fewer than 5k tokens to execute — overhead of full template is not worth it.
- For manual human execution — human tasks need narrative description, not Given-When-Then AC.

## Content

| File | What's inside |
|------|---------------|
| `content/01-template-rules.xml` | Rules for creating task files: section fill order (creator vs executor), token budget breakdown, INVEST validation, AC testability requirements, lifecycle states, anti-patterns. |
| `content/02-checklist.xml` | Phase-by-phase checklist: create file structure, add SDD references, document dependency tree, define requirements coverage, write objective, list dependencies, write ACs, define technical approach, list files, estimate token budget, create implementation and summary sections, quality gate before assignment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task.md` | Complete TASK_NNN.md template with all required sections and placeholder text. |
| `templates/task-lifecycle.sh` | Script to move a task file between lifecycle states (todo/in-progress/done) with section header validation. |
