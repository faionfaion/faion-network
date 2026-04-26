# Business Analysis Planning

## Summary

BABOK Knowledge Area 1: defines how BA work will be performed across five tasks — plan BA approach, plan stakeholder engagement, plan BA governance, plan BA information management, and identify BA performance improvements. Produces five task-scoped artifacts that seed all other ba-core methodologies.

## Why

BA work performed ad-hoc without structure results in inconsistent analysis, missed stakeholders, uncoordinated activities, and unclear deliverables. KA1 is the seeding ceremony that governs everything downstream — without it, stakeholder-analysis, ba-governance, requirements-lifecycle, and elicitation-techniques each use different assumptions and produce incoherent outputs.

## When To Use

- A new initiative crosses from discovery to planned delivery and needs an explicit BA approach, stakeholder map, governance, information management, and performance plan.
- Programs that must demonstrate BABOK conformance to certifying bodies or internal QA (CCBA/CBAP audits, IIBA-aligned PMOs).
- Hybrid plan-driven + change-driven engagements where per-task baselined vs. living artifact declarations are needed.
- Activating sibling ba-core methodologies — KA1 is their prerequisite seeding ceremony.
- When introducing BA performance metrics (rework rate, requirement defect density, elicitation throughput).

## When NOT To Use

- Solo MVP, prototype, or research spike — five KA1 tasks are heavier than the work itself; use a one-page lean canvas.
- Pure backlog-driven Scrum where the Definition of Ready already encodes the BA approach.
- Continuous-discovery contexts where requirements churn weekly — KA1 baselines go stale faster than they can be reviewed.
- When the sponsor will not name a governance approver — without one, KA1 governance becomes decorative.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ka1-tasks.xml` | Five BABOK KA1 tasks, approach selection (plan-driven/change-driven/hybrid), stakeholder categories, elicitation technique selection. |
| `content/02-monitoring-and-performance.xml` | Performance metrics, monitoring cadence per task, replan triggers, ordering constraints between tasks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-approach-document.md` | BA approach document covering initiative overview, approach selection, stakeholders, elicitation plan, deliverables, governance. |
| `templates/ka1_check.py` | Python script validating that all five BABOK KA1 artifacts are present, coherent, and within review cadence. |
