---
slug: process-mining-automation
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers the fundamentals of process mining: discovery algorithms, event-log prerequisites, adoption gate criteria, and automation candidate assessment.
content_id: "63c361296bd7dd91"
tags: [process-mining, automation, rpa, discovery, analysis]
---
# Process Mining and Intelligent Automation Analysis

## Summary

**One-sentence:** Covers the fundamentals of process mining: discovery algorithms, event-log prerequisites, adoption gate criteria, and automation candidate assessment.

**One-paragraph:** Covers the fundamentals of process mining: discovery algorithms, event-log prerequisites, adoption gate criteria, and automation candidate assessment. Use before selecting a tool or vendor. Distinct from the operational four-stage pipeline in the business-analyst variant — this layer handles the go/no-go scoping decision and algorithm selection.

## Applies If (ALL must hold)

- Scoping a process-mining initiative for the first time and briefing a steering committee before tool selection
- Pre-RFP phase comparing Celonis / UiPath Process Mining / Apromore / pm4py (vendors hide algorithm details behind UX)
- Validating that a candidate event log meets three minimum columns (case ID, activity, timestamp) before procurement
- Choosing a discovery algorithm: Alpha/Heuristic/Inductive Miner each have different failure modes on real logs
- Distinguishing conformance vs discovery vs enhancement — naming the mining question type before the artefact is produced
- Diagnosing why an existing deployment produced a spaghetti Directly-Follows Graph

## Skip If (ANY kills it)

- The team already has process-mining tooling and a working event log — go to the business-analyst variant for the full pipeline
- The question is "what should the process be?" (to-be design) — that is BPMN modelling, not mining
- Single-system audit log with fewer than 200 cases — use SQL and a pivot table instead
- Task-level desktop work (clicks, copy-paste between apps) — this is task mining, a different discipline
- Knowledge work without a discrete activity vocabulary (writing, negotiation, R&D)

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ba/ba-core/`
