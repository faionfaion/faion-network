# Writing Implementation Plans

## Summary

Bridges design.md (AD-X decisions) and executor-ready TASK files by producing an ordered, wave-structured implementation plan. The 11-phase writing process: load SDD context → prerequisites → WBS → dependency graph → wave analysis → phase definition → task format → critical path → risk assessment → testing strategy → rollout strategy. Output is `implementation-plan.md`; TASK_*.md files are created separately, wave by wave.

## Why

Design documents are too high-level to act on directly — no ordering of operations, no dependency visibility, no success criteria per step. The impl-plan is the coordination artifact that lets `faion-sdd-executor-agent` process tasks in dependency order without re-reading the entire design. Wave-based decomposition also exposes parallelism opportunities and enforces the 100k token budget before any task file is written.

## When To Use

- Design doc is finalized (Accepted status) and the feature is promoted to `todo/` or `in-progress/`.
- Feature has 3+ components that interact and sequencing matters.
- Multiple waves of parallel tasks are possible (API before frontend, schema before service layer).
- Handoff is needed between agents or sessions — the impl-plan is the coordination artifact.

## When NOT To Use

- Feature has fewer than 3 tasks — skip the plan, write TASK files directly.
- Spec or design doc is still in draft — writing the plan too early wastes tokens when requirements shift.
- Bug fixes — use a single TASK file.
- Exploratory spikes — impl-plans assume known solutions; spikes discover the solution.

## Content

| File | What's inside |
|------|---------------|
| `content/01-writing-process.xml` | 11-phase process with inputs and outputs per phase; document hierarchy (spec → design → impl-plan → tasks); prerequisites checklist; wave analysis rules. |
| `content/02-quality-gates.xml` | Quality gate checklist (AD/FR coverage, 100k compliance, acyclic dependencies, success criteria, testing, risks, critical path); common mistakes table; rollout strategy requirements. |

## Templates

| File | Purpose |
|------|---------|
| `templates/create-tasks.sh` | Bash script: creates empty TASK_*.md stubs with objective, files, AC, and token budget fields from a task ID list. |
