<!--

purpose: Database selection ADR template.
consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
produces: a database-selection artefact validating against scripts/validate-database-selection.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~400-1500 tokens once filled
-->


---
artefact_id: db-selection-<bounded_context>-<date>
owner: <owner> <email>
version: 1.0.0
last_reviewed: 2026-05-23
adr_id: NNN
chosen_db: <chosen_db>
reversibility: <reversibility>
---

## Context

<access_pattern>

## Decision

Use **<chosen_db>** for the <bounded_context> bounded context.

## Scoring matrix

| Criterion | Postgres | Mongo | DynamoDB | Selected |
|-----------|----------|-------|----------|----------|
| Access pattern fit | 4 | 3 | 5 | 5 |
| Consistency | 5 | 3 | 4 | 5 |
| Scale envelope | 4 | 4 | 5 | 5 |
| Operational fit | 5 | 4 | 3 | 5 |
| Total | 18 | 14 | 17 | 20 |

## Alternatives Rejected

| Option | Reason rejected |
|--------|-----------------|
| <option> | <reason> |

## Rollback path

- Estimated cost: <rollback_cost>
- Reversibility tier: <reversibility>
