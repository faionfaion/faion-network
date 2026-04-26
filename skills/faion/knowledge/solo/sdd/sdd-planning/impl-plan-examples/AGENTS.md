# Implementation Plan Examples

## Summary

Three scaled implementation plan examples (3-task simple, 7-task medium, 12-task complex) plus a task-split example for oversized tasks exceeding the 100k token budget. Each example shows wave analysis tables, dependency graphs (text/table format), critical path chains, and per-task breakdowns with AC and file lists. Used as structural references when generating or reviewing real implementation plans.

## Why

Agents generating implementation plans without a concrete reference produce inconsistent wave counts, miss dependency chains, and underestimate parallelization opportunities. These examples calibrate structure and scale: simple/medium/complex examples set expectations for wave count, task count, and checkpoint frequency; the refactoring split example shows exactly where and how to divide a task that exceeds 100k tokens.

## When To Use

- Bootstrapping a new implementation plan for a feature of known complexity (simple/medium/complex).
- Validating a generated plan against a known-good structural reference.
- Teaching wave analysis and critical path before an agent attempts it on a real feature.
- Identifying the split point for tasks that exceed the 100k token budget (use the refactoring split example).

## When NOT To Use

- Copying example task names, file paths, or effort estimates into a real plan — examples are structural references only.
- Referencing hour-based effort estimates from examples — project rules prohibit time estimates; use token estimates only.
- For plans with more than 20 tasks — examples top out at 12; very large features need a custom approach.
- Using ASCII wave diagrams from the examples — project rules prohibit ASCII art; use tables only.

## Content

| File | What's inside |
|------|---------------|
| `content/01-simple-and-medium-examples.xml` | Simple (3-task email verification) and medium (7-task payment system) plan examples with wave analysis tables and task detail format. |
| `content/02-complex-and-split-examples.xml` | Complex (12-task multi-tenant architecture) critical path chain, task-split example for oversized refactoring tasks, quality checklist, and rules for using examples correctly. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dep-graph-validator.py` | Topological sort script to detect cycles in the task dependency graph. |
