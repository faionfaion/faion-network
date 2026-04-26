# Work Breakdown Structure (WBS)

## Summary

A hierarchical decomposition of total project scope into deliverable-oriented (noun-led) work packages. Each leaf is assignable to one owner, estimable in 8–80 hours, and produces a tangible output. The 100% rule requires every parent to equal the sum of its children with no overlap or gaps.

## Why

Without structured scope decomposition, projects face invisible scope creep, missed deliverables discovered late, and inaccurate estimates from unclear work. WBS establishes a reusable scope-baseline artefact that integrates with cost, schedule, and EVM — and gives every work item a stable ID traceable across contracts, schedules, and change requests.

## When To Use

- Establishing a contractual scope baseline for fixed-bid or government-style work.
- Cost estimation for proposals where each work package needs an hours/$ line.
- Programs spanning multiple teams or vendors needing a single ID schema (1.2.3) for integration.
- Compliance or audit contexts where every deliverable must be traceable to a parent objective.

## When NOT To Use

- Backlog-driven product teams — the product backlog plus epics already plays the WBS role.
- Discovery or R&D where deliverables are emergent and unknowable up front.
- Sub-2-week tasks — a checklist or kanban swimlane suffices.
- Steady-state operations work — use a service catalog, not a WBS.

## Content

| File | What's inside |
|------|---------------|
| `content/01-wbs-process.xml` | Four-step process: start with major deliverables, decompose to work packages (8–80h rule), create WBS dictionary, validate with 100% rule. |
| `content/02-examples-antipatterns.xml` | Worked examples (MVP launch, solo content product); antipatterns for verb-led names, missing 100% rule, no dictionary, confusing WBS with schedule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-outline.md` | Hierarchical WBS template for six standard phases (PM, Requirements, Design, Development, Testing, Deployment). |
| `templates/wbs-dictionary-entry.md` | WBS dictionary entry form: ID, parent, description, acceptance criteria, owner, estimate, dependencies, deliverable. |
| `templates/wbs-check.py` | Lint script enforcing noun-led names, max depth 5, and 8–80 hours per leaf. |
