# Process Mining and Intelligent Automation Analysis

## Summary

Covers the fundamentals of process mining: discovery algorithms, event-log prerequisites, adoption gate criteria, and automation candidate assessment. Use before selecting a tool or vendor. Distinct from the operational four-stage pipeline in the business-analyst variant — this layer handles the go/no-go scoping decision and algorithm selection.

## Why

Process documentation relies on subjective input; actual execution differs from documented processes. RPA initiatives fail at high rates (58% of enterprises will use AI-enabled RPA by 2026) when automation targets are chosen from assumptions rather than event-log data. Three discovery algorithms — Alpha, Heuristic, Inductive — have distinct failure modes; picking by guess wastes months of debugging.

## When To Use

- Scoping a process-mining initiative for the first time and briefing a steering committee before tool selection.
- Pre-RFP phase comparing Celonis / UiPath Process Mining / Apromore / pm4py (vendors hide algorithm details behind UX).
- Validating that a candidate event log meets three minimum columns (case ID, activity, timestamp) before procurement.
- Choosing a discovery algorithm: Alpha/Heuristic/Inductive Miner each have different failure modes on real logs.
- Distinguishing conformance vs discovery vs enhancement — naming the mining question type before the artefact is produced.
- Diagnosing why an existing deployment produced a spaghetti Directly-Follows Graph.

## When NOT To Use

- The team already has process-mining tooling and a working event log — go to the business-analyst variant for the full pipeline.
- The question is "what should the process be?" (to-be design) — that is BPMN modelling, not mining.
- Single-system audit log with fewer than 200 cases — use SQL and a pivot table instead.
- Task-level desktop work (clicks, copy-paste between apps) — this is task mining, a different discipline.
- Knowledge work without a discrete activity vocabulary (writing, negotiation, R&D).

## Content

| File | What's inside |
|------|---------------|
| `content/01-mining-fundamentals.xml` | Algorithm comparison (Alpha/Heuristic/Inductive), event-log minimum requirements, mining question taxonomy. |
| `content/02-automation-assessment.xml` | Automation candidate scoring matrix, RPA vs intelligent automation comparison, adoption gate criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pm-feasibility-audit.py` | Python script that audits a CSV event log for mining readiness and recommends an algorithm. |
| `templates/automation-assessment.md` | Automation readiness scoring template with ROI estimate skeleton. |
