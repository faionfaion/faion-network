# Implementation Plan: 100k Token Rule

## Summary

Every task assigned to an agent must fit within a 100k token context budget. The budget has fixed overhead (agent prompt ~8k, project context ~12k, task file ~3k, buffer ~15k) plus variable codebase reading. Tasks exceeding 80k tokens must be split before any TASK file is written. Three splitting strategies: by component, by layer, by dependency wave.

## Why

Agents assigned tasks exceeding their effective context window produce incomplete output, higher hallucination rates, and longer execution times — and the executor does not abort mid-task. Budget enforcement is entirely a planning-phase responsibility. Wave-based task creation (create Wave 1, execute, then create Wave 2 using patterns learned) further reduces token waste from early task files that become stale when Wave 1 reveals wrong assumptions.

## When To Use

- Before assigning any task to `faion-sdd-executor-agent` — validate context budget fits.
- When decomposing a large design into tasks and unsure whether to split or combine.
- Auditing an existing implementation plan where tasks seem to exceed context window.
- Estimating total project token cost before committing to an implementation approach.

## When NOT To Use

- Micro-tasks under 5k tokens — budget calculation overhead is not worth it.
- Reading-only research passes — context budget still applies but failure mode is less severe.
- Attempting to skip the rule for Claude 200k context — focus degrades at high utilization even within window limits.

## Content

| File | What's inside |
|------|---------------|
| `content/01-budget-breakdown.xml` | Token budget breakdown table; complexity levels (simple/normal/complex) with context ranges; three worked estimation examples (single-file, multi-file, complex refactoring). |
| `content/02-splitting-strategies.xml` | When to split rules; three splitting strategies (by component, by layer, by dependency wave); WBS principles and example tree; wave-based creation pattern and benefits. |

## Templates

| File | Purpose |
|------|---------|
| `templates/estimate-context.sh` | Bash script: sums token estimates for a task's file list using byte count proxy; flags tasks over 100k. |
