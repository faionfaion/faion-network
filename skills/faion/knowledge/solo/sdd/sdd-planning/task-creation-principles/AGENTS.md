# Task Creation Principles

## Summary

Principles for decomposing an approved design into bounded, executor-ready TASK_*.md files. Applies the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable), SMART task goals, WBS 8-80 rule adapted to token budgets (hard cap: 100k tokens per task), Given-When-Then acceptance criteria, and full FR-X/AD-X traceability links inside each task file.

## Why

Implementation plans fail when tasks are too large (executor runs out of context mid-implementation), too vague (AC are not testable), or untraceable (executor cannot verify the task satisfies a requirement). INVEST + SMART enforced at task creation time catches these defects before execution, and inline FR/AD text eliminates re-reading the full SDD context during execution.

## When To Use

- Converting an approved design document into executable TASK_*.md files.
- Splitting large undefined work into bounded units before assigning to a subagent.
- Auditing an existing implementation plan where tasks are vague or oversized.
- When faion-sdd-executor-agent will run unattended and needs unambiguous inputs.

## When NOT To Use

- Prototyping or exploratory spikes — INVEST/SMART overhead is not worth it.
- Single-file hot-fixes with obvious scope — task structure adds ceremony with no return.
- Early brainstorming phases before a spec exists (no FR-X to trace to yet).

## Content

| File | What's inside |
|------|---------------|
| `content/01-decomposition-principles.xml` | Right-size rule (simple/normal/complex token tiers), INVEST criteria table with examples, SMART criteria applied to task goals, traceability format (TASK → FR-X → AD-X), task states and lifecycle. |
| `content/02-ac-and-checklist.xml` | Given-When-Then acceptance criteria format, AC coverage checklist (happy path, alternatives, boundaries, errors, security, performance), full pre-creation quality checklist, common mistakes with fixes. |

## Templates

none
