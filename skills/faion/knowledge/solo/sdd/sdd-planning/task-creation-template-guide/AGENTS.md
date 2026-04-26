# Task Creation Template Guide

## Summary

The canonical template for TASK_NNN.md files — the atomic units executor agents consume.
Each task file must be self-contained within a 100k token budget: SDD references (15%),
dependency tree with completed-task summaries and code snippets (10%), research (25%),
implementation (40%), testing (10%). The dependency tree is the most critical section —
it prevents agents from re-discovering patterns already established in completed tasks.

## Why

Executor agents receiving stub task files waste 30-40% of context budget re-discovering
patterns, make inconsistent implementation decisions, and contradict earlier tasks. A fully
populated task file with a dependency tree (summaries + key code from completed tasks) and
explicit FR/AD traceability lets the executor start coding immediately. Token budget
enforcement prevents tasks that exceed the 100k context window.

## When To Use

- Generating TASK_NNN.md files from an approved implementation plan
- Ensuring each task contains enough context for single-agent execution without re-reading
  the whole codebase
- Before handing off feature execution to `faion-sdd-executor-agent`

## When NOT To Use

- Before `spec.md` and `design.md` are both approved — templates will be incomplete
- Spike/research tasks with unknown scope (token budget cannot be estimated)
- New greenfield project with no prior tasks (no dependency tree to build)

## Content

| File | What's inside |
|------|---------------|
| `content/01-context-budget.xml` | 100k token budget breakdown, why dependency tree is critical, context optimization rules |
| `content/02-template-sections.xml` | All template sections with purpose and constraints: metadata, SDD refs, dependency tree, goals, AC, files, risks, testing, subtasks |
| `content/03-checklist.xml` | Phase-by-phase creation checklist and quality gate |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-template.md` | Canonical TASK_NNN.md template v2.0 with all sections |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/estimate-tokens.py` | Estimate token count for task context components before writing the task file |
