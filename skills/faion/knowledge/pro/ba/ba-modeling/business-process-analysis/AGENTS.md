# Business Process Analysis

## Summary

5-stage analysis cycle for understanding how work actually flows through an organization: identify processes → document current state (with source citations) → analyze (value/time/cost tables) → design future state (diff table, not prose) → validate with stakeholders. Output artifacts are `process-documentation.md` and `process-analysis.md`; BPMN XML stored in version control alongside them.

## Why

Processes exist only in people's heads; different people execute them differently; inefficiencies are hidden in workarounds. BPA produces a numbers-backed case for change (NVA-minutes × frequency) before automation or system redesign, preventing the "paving the cowpath" failure where a manual mess is automated at scale. Pre-automation discovery is the highest-leverage use: model the as-is so the n8n workflow or backend service eliminates waste, not replicates it.

## When To Use

- Raw process evidence exists (SOP docs, Slack threads, ticket histories, support transcripts) and a normalized model is needed before redesign.
- A cross-team workflow shows symptoms of waste: rework loops, long approval queues, dual data entry.
- Pre-automation discovery: before writing an n8n workflow, RPA bot, or backend service replacing a manual process.
- Pre-spec stage of a BA-heavy SDD feature: BPA output becomes input to requirements-documentation and acceptance-criteria.
- Compliance / audit prep where regulators expect a documented process map with controls and exception handling.

## When NOT To Use

- Greenfield product where no current process exists — use `use-case-modeling` or `user-story-mapping` instead.
- One-off troubleshooting of a single broken instance — use 5-whys / fishbone root-cause tools.
- Tactical UI tweaks where the "process" is one click.
- Highly creative / knowledge-work flows (R&D, design, writing) where steps are non-deterministic.
- Team is already mid-redesign and stakeholders have agreed on future state — re-modelling as-is delays delivery.

## Content

| File | What's inside |
|------|---------------|
| `content/01-5stage-cycle.xml` | Stage-by-stage rules: evidence citation per step, VA/BN/NVA rubric, future-state diff table format, metrics-source requirement. |
| `content/02-agentic-workflow.xml` | State-machine subagent dispatch, stage-2 and stage-3 prompt patterns, discover_dfg.py for event-log mining. |
| `content/03-antipatterns.xml` | Ideal-vs-actual gap, hallucinated metrics, single-pool bias, future-state shopping list, LLM linear-flow bias. |

## Templates

| File | Purpose |
|------|---------|
| `templates/process-documentation.md` | Current-state doc template: overview, actors, inputs/outputs, process steps table with citation column, business rules, metrics. |
| `templates/process-analysis.md` | Analysis template: value classification table, pain points, bottlenecks, improvement opportunities ranked by NVA×frequency. |
| `templates/discover_dfg.py` | Event-log to directly-follows graph via pm4py; outputs dfg.svg and per-activity stats.csv. |
| `templates/bpa-state.json` | Workflow state file for resumable 5-stage pipeline: tracks completed stages and artifact paths. |
