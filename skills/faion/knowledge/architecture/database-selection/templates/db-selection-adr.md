<!--
purpose: Database selection ADR template.
consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
produces: a database-selection artefact validating against scripts/validate-database-selection.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~400-1500 tokens once filled
variables:
  - name: bounded_context
    type: string
    required: true
    description: The one bounded context this database serves, kebab-case - "checkout", "search-index". One decision per context; if you cannot name a single one, the decision is drawn too wide to defend.
  - name: owner
    type: string
    required: true
    description: The person accountable for this choice - whoever gets paged when the storage engine turns out to be the reason. A team alias here means the page has no destination.
  - name: email
    type: string
    required: true
    description: The owner's email, reachable after they change teams. This is the address the next engineer writes to before undoing what this document decided.
  - name: date
    type: string
    required: true
    description: The day this was agreed, ISO - not the day it was typed up. Downstream reviews are scheduled off it, so a placeholder date silently disables the review.
  - name: chosen_db
    type: string
    required: true
    description: Product and major version you are committing to - "PostgreSQL 16". Give the version - the feature you are counting on may not exist in the one ops actually installs.
  - name: reversibility
    type: enum
    required: true
    options: [partial_two_way, one_way_door_costly, one_way_door_irrevocable]
    description: How hard is leaving? partial_two_way = dual-write then migrate. one_way_door_costly = months of work and a data rewrite. one_way_door_irrevocable = the old model cannot be reconstructed.
  - name: access_pattern
    type: text
    required: true
    description: The read/write shape this must serve - query patterns, hot keys, consistency requirement, peak QPS, dataset size and growth. Numbers you measured or projected. "High scale" is not an access pattern.
  - name: rollback_cost
    type: text
    required: true
    description: What leaving would actually cost - engineering weeks, contract exit fees, customer-visible downtime. Estimate it now, while nobody is angry and the estimate is still honest.
-->
---
artefact_id: db-selection-{{bounded_context}}-{{date}}
owner: {{owner}} <{{email}}>
version: 1.0.0
last_reviewed: 2026-05-23
adr_id: NNN
chosen_db: {{chosen_db}}
reversibility: {{reversibility}}
---

## Context

{{access_pattern}}

## Decision

Use **{{chosen_db}}** for the {{bounded_context}} bounded context.

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
| [option] | [reason] |

## Rollback path

- Estimated cost: {{rollback_cost}}
- Reversibility tier: {{reversibility}}
