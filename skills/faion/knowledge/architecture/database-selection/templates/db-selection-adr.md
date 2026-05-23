# purpose: Database selection ADR template.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a database-selection artefact validating against scripts/validate-database-selection.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: db-selection-<context>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
adr_id: NNN
chosen_db: <product + version>
reversibility: <partial_two_way|one_way_door_costly|one_way_door_irrevocable>
---

## Context

<access pattern + consistency + scale + operational constraints>

## Decision

Use **<product>** version <version> for <bounded context>.

## Scoring matrix

| Criterion | Postgres | Mongo | DynamoDB | <selected> |
|-----------|----------|-------|----------|------------|
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

- Estimated cost: <X engineering weeks + $Y contract exit + customer impact>.
- Reversibility tier: <as tagged above>.
