# Code Decomposition Principles

## Summary

Rules for splitting source files into single-responsibility units that fit in an LLM context window and in a human reviewer's head. Concrete thresholds: split when a file exceeds 300 lines or ~9–10k tokens; target 30–200 lines per file; set a minimum of 30 lines to prevent micro-files. Use `git mv` to preserve history. Run tests between every move.

## Why

LLMs produce partial or incorrect diffs when a file plus its tests exceed the effective context window (~20–50k tokens). Humans review poorly past ~300 lines. Modular architectures correlate with 973× higher deployment frequency (2024 DORA report). The DORA findings and Addy Osmani's LLM workflow both confirm that small, single-responsibility files unlock both human and agent productivity.

## When To Use

- A target file exceeds ~300 lines and a subagent must edit it under a tight context budget.
- LLM keeps producing partial/incorrect diffs because it cannot hold the full file plus tests in one window.
- Designing a new module from a spec and laying out the file tree from the start.
- Onboarding an LLM to an unfamiliar repo: split first, then have the agent read the new tree.

## When NOT To Use

- File is under 100 lines and tightly cohesive — splitting adds indirection without context savings.
- Hot path with a measured performance cost from indirection (rare in app code).
- Generated code (migrations, protobuf stubs) — apply rules to the source, not the output.
- Throwaway scripts and one-shot notebooks where the file is the unit of thought.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Single-responsibility rule, optimal file-size table, token-budget planning, when-to-split checklist. |
| `content/02-antipatterns.xml` | God file, micro-files, leaky abstractions, barrel re-exports — with code examples and fixes. |
| `content/03-workflow.xml` | Analyze → plan → execute → verify loop; planner/executor/reviewer subagent split; prompt patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decomp-candidates.sh` | Lists oversize files, high-complexity functions, and high-churn hotspots for the planner agent. |
| `templates/planner-prompt.txt` | Agent prompt: produce target file tree + ordered move list as JSON. |
