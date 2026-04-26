# Writing Implementation Plans

## Summary

An implementation plan bridges design docs and executable tasks. It transforms architectural decisions (AD-X) into ordered, token-budgeted work units optimized for LLM agent execution. The 100k token rule: each task must fit within a focused context window. Wave analysis identifies parallel execution opportunities. Every task must trace to an AD-X or FR-X — orphan tasks are a quality gate failure.

## Why

Without an implementation plan, agents execute tasks in arbitrary order, creating merge conflicts and dependency violations. Wave analysis enables 1.8-3.5x parallelization speedup. Token budgets prevent context window exhaustion mid-task, which is the most common cause of incomplete or broken agent outputs.

## When To Use

- After spec and design are both in Approved status
- When feature has 3+ tasks requiring ordered execution
- When design doc contains parallel-eligible work (Wave 1 / Wave 2 pattern)
- When task token estimates exceed 30k (simple tasks may skip formal plan)

## When NOT To Use

- Before spec or design are approved — planning against unapproved docs creates rework
- For trivial single-file changes that need no coordination
- For bug fixes that touch one file and have no dependencies
- When design doc has no AD-X decisions (no design = no plan needed)

## Content

| File | What's inside |
|------|---------------|
| `content/01-task-structure.xml` | INVEST criteria, token budget tiers, task definition fields, acceptance criteria rules |
| `content/02-dependency-waves.xml` | DAG construction, wave algorithm, critical path analysis, anti-patterns |
| `content/03-quality-gates.xml` | Traceability 100% rule, pre-writing checklist, common issues table |

## Templates

| File | Purpose |
|------|---------|
| `templates/implementation-plan.md` | Full plan stub with wave table, critical path, and per-task sections |
| `templates/parse-plan.py` | Python script to extract task list and dependency graph from implementation-plan.md |
