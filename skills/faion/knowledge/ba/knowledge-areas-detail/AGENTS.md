# BA Knowledge Areas Detail

## Summary

**One-sentence:** Reference catalog for all six BABOK Knowledge Areas (KA-1..KA-6) producing a per-KA task table, canonical workflow sequence, and routing map back into the BA methodology library.

**One-paragraph:** Detailed reference for all six BABOK Knowledge Areas: BA Planning & Monitoring (KA-1), Elicitation & Collaboration (KA-2), Requirements Lifecycle (KA-3), Strategy Analysis (KA-4), Requirements Analysis & Design (KA-5), Solution Evaluation (KA-6). Produces a routing decision-record from the user's situation (greenfield, change request, transformation) to the right KA and its tasks.

**Ефективно для:**

- Greenfield kickoff: треба обрати правильну послідовність KA-1 → KA-6.
- Change request triage: routing з ask до конкретного KA task.
- Аудит: mapping deliverables до KA tasks як evidence для SOX / ISO.
- Onboarding junior BA з прогресивним KA learning path.

## Applies If (ALL must hold)

- Greenfield engagement: pick KA sequence + methodologies to apply.
- Change request triage: route to the right KA tasks.
- Transformation programme: orchestrate KA-1..KA-6 with explicit dependencies.
- Audit prep: map deliverables to KA tasks for SOX 404 / ISO compliance evidence.
- Onboarding a junior BA: learning path keyed to KA progression.

## Skip If (ANY kills it)

- Single fix / hot patch — KA process is overhead.
- Pure design review (no requirements work).
- Project already mid-flight with a different framework (PMBOK-only).
- When a more specific BA methodology already routes the task.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Situation description | Markdown (greenfield / change / transformation) | BA / sponsor |
| Existing BA artifacts inventory | Markdown | knowledge management |
| BABOK v3 reference | PDF / docs | IIBA |
| Methodology registry | JSON | this skill |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/knowledge-areas-overview` | Provides L1 summary; this is L2 detail. |
| `pro/ba/business-analyst/methodologies-detail` | Per-KA methodology drilldown. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `situation-classification` | sonnet | Map ask to greenfield/change/transformation class. |
| `ka-task-routing` | sonnet | Pick KA tasks for the classified situation. |
| `workflow-sequence-build` | sonnet | Order KA tasks per canonical dependency map. |
| `audit-mapping` | haiku | Map existing deliverables to KA evidence rows. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ka-route.sh` | Shell helper to print KA → method list for a situation. |
| `templates/ka-detail.md` | Per-KA detail page skeleton. |
| `templates/workflow-sequence.md` | Workflow sequence table for greenfield/change/transformation. |
| `templates/_smoke-test.md` | Minimum filled-in routing record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-knowledge-areas-detail.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[knowledge-areas-overview]]
- [[methodologies-detail]]
- [[modern-ba-framework]]
- [[requirements-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
