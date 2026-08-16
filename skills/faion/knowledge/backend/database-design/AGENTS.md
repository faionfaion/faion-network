# Database Design (PostgreSQL)

## Summary

**One-sentence:** Produces a PostgreSQL schema spec: 3NF tables, access-pattern indexes, DB-layer constraints (FK / CHECK / NOT NULL / UNIQUE), forward + backward migrations, TIMESTAMPTZ + PK type policy.

**Ефективно для:**

- New entities in an existing PostgreSQL schema.
- Migration from prototype-grade schema to production.
- OLTP workloads with mixed read/write patterns.
- Multi-tenant schemas needing tenant-id discipline.

**One-paragraph:** Relational schema design for PostgreSQL: normalize to 3NF first; derive indexes from a stated query workload, not assumptions; enforce integrity at the database layer (FK, CHECK, NOT NULL, UNIQUE); emit both forward and backward migrations in the project's migration tool. PK type, ON DELETE semantics, and TIMESTAMPTZ vs TIMESTAMP are decided globally and consistently.

## Applies If (ALL must hold)

- Stack uses PostgreSQL ≥14.
- Workload mix is OLTP (transactional, indexable).
- Migration tool present (Alembic, dbmate, Flyway, ActiveRecord, Goose, Atlas).
- Project agreed on global PK type + ON DELETE policy.

## Skip If (ANY kills it)

- Read-heavy analytics workloads — use a columnar store / OLAP.
- Document-oriented schemas — switch to MongoDB / DynamoDB / JSONB.
- Single-table designs — see NoSQL design instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Entity inventory + relationships | domain doc | PM / BA |
| Query workload sample | EXPLAIN report | team |
| Global type policy (UUID v7 vs bigint) | decision record | tech lead |
| Migration tool selection | ADR | tech lead |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 testable rules with rationale + source | ~1300 |
| `content/02-output-contract.xml` | essential | artefact JSON Schema + schema-spec contract + forbidden schema shapes | ~1400 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom / root-cause / fix | ~1100 |
| `content/04-procedure.xml` | essential | 5-step artefact procedure + 6-step schema-authoring sub-procedure | ~1500 |
| `content/05-examples.xml` | recommended | two end-to-end worked examples | ~1000 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-tables` | sonnet | 3NF tables from entity inventory. |
| `derive-indexes` | sonnet | Maps workload sample to indexes. |
| `write-migrations` | haiku | Mechanical: forward + backward DDL. |

## Templates

| File | Purpose |
|------|---------|
| `templates/database-design.json` | JSON Schema for the Database Design (PostgreSQL) output contract |
| `templates/database-design.md.j2` | Markdown skeleton with the required fields |
| `templates/database-design.md` | Markdown skeleton with the required fields Generated from `templates/database-design.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a database-design record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a database-design record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ecommerce_schema.sql` | Reference PostgreSQL schema: UUID PKs, TIMESTAMPTZ, named constraints, partial indexes, soft-delete view, audit trigger |
| `templates/audit_trigger.sql` | Audit-log table + trigger function — the one legitimate use of a trigger |
| `templates/alembic_migration.py` | Alembic expand-then-contract migration with explicit revision ids and a real `downgrade` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-database-design.py` | Enforce the Database Design (PostgreSQL) output contract | After subagent returns, before downstream consumer reads |
| `scripts/schema_diff.sh` | Diff two schema dumps to see exactly what a migration changes | Before approving any migration PR |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[caching-invalidation]]
- [[error-handling]]
- [[go-error-handling-patterns]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/database-design.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/database-design.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^dbd\\-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
