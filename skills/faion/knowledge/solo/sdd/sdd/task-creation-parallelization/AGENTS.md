# Task Creation & Parallelization

## Summary

Decompose an approved `design.md` into LLM-executable `TASK-XXX-*.md` files, each bounded by the 100k token rule, then organize them into dependency waves for parallel execution. Each task must satisfy INVEST criteria: Independent within its wave, Negotiable on impl details, Valuable (traces to FR-X), Estimable (token budget), Small (single context window), Testable (Given-When-Then AC).

## Why

LLMs have fixed context windows. A task that exceeds 100k tokens causes forgotten requirements, inconsistent patterns, and incomplete implementations. Wave-based execution (2-4x speedup) requires task boundaries that are file-level, not feature-level — two tasks modifying the same file conflict in parallel git worktrees. Pattern propagation between waves requires explicit dependency-summary sections; without them each agent starts fresh and produces divergent naming and error handling.

## When To Use

- Decomposing an approved `design.md` before execution begins
- Planning wave-based parallel execution across multiple agents or worktrees
- Checking that each task fits the 100k token context budget
- Propagating patterns from early waves into later-wave task context
- Managing strict finish-to-start dependencies (a task needing output from two others waits for both)

## When NOT To Use

- Feature is a single-task implementation (< 30k tokens) — one task, no waves needed
- `design.md` is not yet approved — do not decompose while spec is still changing
- Tasks are unknown until runtime (data-driven pipelines) — decomposition cannot be done upfront
- Experimental/spike work where implementation approach is undefined — discover first, decompose after

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | 100k token rule, INVEST criteria, wave-based execution, context budget allocation |
| `content/02-checklist.xml` | Six-phase decomposition checklist: pre-decomposition through documentation |
| `content/03-examples.xml` | Auth feature decomposition (good vs bad), full TASK-005 example, anti-patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-file.md` | Full TASK-XXX-*.md template with INVEST fields, token estimate, wave, dependency tree |
| `templates/task-list.md` | Feature-level task overview with dependency graph and wave status table |
| `templates/task-minimal.md` | Minimal template for simple tasks under 30k tokens |
| `templates/task-research.md` | Research task template producing ADR + next-task list |
| `templates/prompt-decompose.txt` | Prompts for decomposition, wave planning, AC generation, and task verification |
