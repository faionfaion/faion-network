# Workflow: Design Phase

## Summary

Step-by-step procedures for the SDD design phase: writing design documents (spec → AD-X →
file table → data models → API contracts → testing strategy), writing implementation plans
(context load → complexity analysis → work units → 100k rule → dependency graph → wave
analysis), creating TASK_NNN.md files from the plan, and running parallelization analysis.
Prerequisite: `spec.md` must be approved before starting.

## Why

Design phase without explicit procedures produces design docs where AD choices are made
without listing alternatives, file tables include files not required by any FR, and
implementation plans have incorrect wave assignments because the dependency graph was not
built first. The procedure enforces: research before decisions, files-first before task
descriptions, reviewer gate before approval.

## When To Use

- Approved `spec.md` exists and the feature needs a technical blueprint before coding starts
- Choosing between 2+ architecture options with real trade-offs
- Codebase has existing patterns that new work must follow — design phase surfaces them
- Feature spans multiple services or data models requiring explicit data flow

## When NOT To Use

- Spec is still Draft or unapproved — design decisions will be based on shifting requirements
- Tiny bugfixes or single-file changes where a full design doc adds zero value
- Pure infrastructure changes (server config, CI tweaks) that don't affect application architecture
- Greenfield spikes where the goal is learning, not committing to an approach

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-doc-workflow.xml` | 11-phase procedure for writing design.md: prereqs, spec extraction, codebase research, AD decisions, file table, testing, risks, review, save |
| `content/02-impl-plan-workflow.xml` | 8-phase procedure: context load, complexity analysis, work units, 100k rule, dependency mapping, draft, review, save |
| `content/03-task-and-parallel.xml` | Task creation workflow (subagent calls, 4-pass review) and parallelization analysis (wave pattern, checkpoint types) |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/find-shared-files.py` | Detect implicit task dependencies: files touched by multiple tasks |
