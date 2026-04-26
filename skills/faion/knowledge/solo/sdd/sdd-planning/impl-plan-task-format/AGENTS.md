# Implementation Plan Task Format

## Summary

Defines the canonical TASK_*.md file format (v2.0) consumed by `faion-sdd-executor-agent`. Each task has: ID, Phase, Wave, Description, Traces To (AD-X / FR-X), Dependencies, Blocks, Complexity (simple/normal/complex), Context Estimate, Acceptance Criteria, Files table (CREATE/MODIFY/DELETE/RENAME), Technical Notes, Tests checklist. INVEST validation is applied after generation.

## Why

The executor agent parses TASK files mechanically — it must find every required field in a known location. Vague AC items ("works correctly") leave no observable outcome; the executor cannot determine success. The INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable) ensure tasks can be executed in isolation without blocking sibling waves, and that each task fits within the 100k token budget.

## When To Use

- Converting design.md architecture decisions into executor-ready TASK_*.md files.
- Defining structure for an implementation plan that supports parallel waves.
- Auditing existing task files for INVEST compliance before executor assignment.

## When NOT To Use

- One-off scripts or changes outside the SDD lifecycle — overhead exceeds benefit.
- Research spikes where the output is a document, not code.
- Tasks under ~15k tokens — the format overhead is not justified.

## Content

| File | What's inside |
|------|---------------|
| `content/01-task-format.xml` | Full TASK v2.0 format spec; INVEST validation table; three worked examples (simple/normal/complex); file action reference; dependency type reference (FS/SS/FF/SF). |
| `content/02-ac-rules.xml` | Rules for writing testable AC items; good vs bad AC examples; critical path structure and visualization; Technical Notes guidelines. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-template.md` | Blank TASK_*.md skeleton with all required fields and placeholder comments. |
| `templates/gen-dep-graph.sh` | Bash script: generates Graphviz DOT dependency graph from a feature's TASK files. |
