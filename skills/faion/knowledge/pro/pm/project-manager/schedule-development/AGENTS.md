# Schedule Development

## Summary

A deterministic process for building a project schedule from WBS work packages: define activities, sequence with dependency types (FS/FF/SS/SF), estimate durations using three-point PERT, run forward and backward pass to compute Early Start/Early Finish/Late Start/Late Finish per activity, identify the critical path (zero float), and place buffers at merge points and project end using Critical Chain methods rather than per-task padding.

## Why

Without a critical path, delays cascade invisibly. Near-critical paths (float &lt; 2 days) become critical after one slip and are invisible without slack analysis. Per-task padding hides slack and creates Student Syndrome and Parkinson's Law effects. PERT three-point estimation forces pessimistic cases into the conversation before they happen. The schedule is the primary coordination artefact for multi-resource projects.

## When To Use

- Building the initial schedule from a WBS at kickoff (activity definition through CPM baseline)
- Re-baselining after a change-control event (scope add, vendor slip, milestone shift)
- Producing PERT three-point estimates for stakeholder communications
- Solopreneur weekly capacity planning across multiple parallel projects

## When NOT To Use

- Pure agile teams with fixed-cadence sprints — velocity and roadmap replace CPM; critical path is overhead
- Highly creative / R&D work where activity duration is unknowable — use rolling-wave or Kanban instead
- Tasks under 2 weeks with a single owner — a checklist suffices
- Fixed-deadline projects where you back-plan from end date — use reverse-pass / time-boxed scope planning

## Content

| File | What's inside |
|------|---------------|
| `content/01-cpm-process.xml` | Five-step CPM process: activities, sequencing, PERT estimation, critical path forward/backward pass, buffer placement |
| `content/02-rules.xml` | Rules for effort vs duration, dependency types, re-baselining discipline, near-critical path tracking; antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/activity-list.md` | Activity table with ID, duration, dependencies, and resource columns |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/critical-path.py` | CPM forward/backward pass using networkx; validates DAG, computes ES/EF/LS/LF and float per activity |
