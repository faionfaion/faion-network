# Data Analysis

## Summary

**One-sentence:** Identify, define, and document data needs before system development — data dictionary, conceptual/logical model, quality dimensions, and business rules as a versioned contract.

**One-paragraph:** Pre-development discovery for data entities: harvest sources, build a normalized data dictionary, derive conceptual and logical models, assess data quality on six dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness), and surface business rules. Output is a `spec` artefact: data_dictionary, ERD, and quality_baseline. Becomes the contract developers, architects, and integration teams build against.

**Ефективно для:**

- Pre-database design коли немає shared data dictionary.
- ETL / integration layer між двома+ системами.
- Pre-migration scope assessment.
- Data-quality baseline для GDPR / HIPAA compliance.

## Applies If (ALL must hold)

- Starting database or integration design and no shared data dictionary exists.
- Reports from different systems show conflicting figures for the same metric.
- Building ETL/integration layer between two or more systems.
- Compliance requires documented data ownership and classification.

## Skip If (ANY kills it)

- Exploratory analytics spike where the data model will be thrown away.
- Event-streaming architectures with schema-on-read by design.
- Frontend-only features with no new data persistence.
- Authoritative data dictionary already exists and is current — extend, do not duplicate.
- Tiny CRUD apps with fewer than 10 entities — ceremony costs more than it saves.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-system inventory | YAML / Markdown table | architecture team |
| Sample data exports | CSV / Parquet | data engineering |
| Compliance classification rubric | doc | DPO / legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[interface-analysis]] | Sibling that maps the integration surface this data lives behind |
| [[ba-planning]] | Upstream plan that scopes data-analysis effort + governance |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: every field typed + sourced, six DQ dimensions scored, business rules as predicates, owner per entity, version pinned | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: free-text type, anonymous owner, missing DQ baseline, single-system bias | 850 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example: customer entity across CRM + billing | 700 |
| `content/06-decision-tree.xml` | essential | Routing on system count + DQ baseline status | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `field_normalization` | haiku | Mechanical mapping CSV header → field row. |
| `model_derivation` | sonnet | Conceptual → logical → physical with constraints. |
| `dq_assessment` | opus | Multi-dimensional quality scoring with rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-dictionary.md` | Markdown skeleton with field/source/type/owner/DQ columns |
| `templates/_smoke-test.json` | Minimum viable data-dictionary fixture |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[interface-analysis]]
- [[business-process-analysis]]
- [[ba-planning]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (source-system count, DQ baseline presence, compliance flag) to the right rule. Use when in doubt whether the dictionary is ready to hand off to developers.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "dictionary_id": "smoke-customer",
  "version_tag": "v0.1.0",
  "entities": [
    {
      "name": "customer",
      "owner_name": "Maria Lopes",
      "owner_role": "Data Steward",
      "fields": [
        {
          "name": "customer_id",
          "type": "uuid",
          "source_system": "crm",
          "source_ref": "crm.customers.id",
          "nullable": false,
          "pii": false
        },
        {
          "name": "email",
          "type": "string",
          "source_system": "crm",
          "source_ref": "crm.customers.email",
          "nullable": false,
          "pii": true
        }
      ],
      "dq_baseline": {
        "accuracy": 90,
        "completeness": 85,
        "consistency": 80,
        "timeliness": 95,
        "validity": 92,
        "uniqueness": 100
      }
    }
  ],
  "business_rules": [
    {
      "id": "br-01",
      "entity": "customer",
      "predicate": "regex(email, '^[^@]+@[^@]+$')",
      "severity": "block"
    }
  ]
}
```
