# Schedule Development

## Summary

A process for converting WBS work packages into a sequenced, resourced, and buffered schedule with an identified critical path. Use three-point estimation (PERT) for any activity over 5 days, explicit dependency types (FS/SS/FF/SF), and CCPM-style project and feeding buffers. Buffers must be visible and named — never hidden inside individual estimates.

## Why

Without critical-path analysis, teams apply equal focus to all tasks and are surprised when non-critical delays cascade. Hidden padding inside task estimates makes buffer management impossible. Three-point estimation forces honest pessimistic scenarios and catches the "optimistic by 30%" bias that causes late projects.

## When To Use

- Programs with hard external deadlines (regulatory, market, contractual) requiring critical-path defense.
- Multi-team or multi-vendor work with cross-team dependencies needing FS/SS/FF links.
- Fixed-bid proposals where the schedule baseline drives the price.
- Resource-constrained programs needing leveling and conflict detection.

## When NOT To Use

- Pure-Scrum cadence with empowered PO — sprint plan replaces schedule.
- Continuous-flow or Kanban product teams.
- Projects shorter than 2 weeks — a checklist beats a Gantt.
- Discovery or R&D where activity duration is fundamentally unknowable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-schedule-process.xml` | Five-step process: define activities, sequence (dependency types), estimate with PERT/analogous/parametric, identify critical path (CPM), add buffers. |
| `content/02-examples-antipatterns.xml` | Worked MVP schedule example and solopreneur time allocation; five scheduling antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/activity-list.md` | Activity list table with ID, duration, dependencies, and resources. |
| `templates/cpm.py` | Minimal CPM script: forward/backward pass, float, critical path output from YAML. |
