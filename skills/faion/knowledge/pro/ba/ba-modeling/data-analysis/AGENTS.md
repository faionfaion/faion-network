---
slug: data-analysis
tier: pro
group: ba
domain: ba-modeling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured approach to identifying, defining, and documenting data needs before system development.
content_id: "29ca58ceccac3e3f"
tags: [data-analysis, data-modeling, data-dictionary, erd, data-quality]
---
# Data Analysis

## Summary

**One-sentence:** A structured approach to identifying, defining, and documenting data needs before system development.

**One-paragraph:** A structured approach to identifying, defining, and documenting data needs before system development. Covers data requirements gathering, data element definition, conceptual/logical/physical modeling, data quality assessment across six dimensions, and data business rules. Produces a data dictionary and data requirements document that developers and architects use as authoritative data contracts.

## Applies If (ALL must hold)

- Starting database or integration design and no shared data dictionary exists.
- Reports from different systems show conflicting figures for the same metric.
- Building ETL/integration layer between two or more systems.
- Assessing data migration scope before cutover.
- Data quality issues are causing operational problems and no baseline measurement exists.
- Compliance requires documented data ownership and classification (GDPR, HIPAA).

## Skip If (ANY kills it)

- Exploratory analytics spike where the data model will be thrown away — just query and iterate.
- Event streaming architectures where schema-on-read is intentional; a rigid dictionary adds friction.
- Frontend-only features with no new data persistence.
- When an authoritative data dictionary already exists and is up to date — extend it, do not duplicate.
- Pure UI/UX research where the output is a prototype, not a data model.
- Greenfield prototypes pre-PMF where the schema changes weekly — formal data dictionaries become stale faster than written.
- Statistical / exploratory data analysis (EDA, pandas, notebooks) — that is data science, not BA Data Analysis.
- Pure ML feature engineering — features evolve through training pipelines, not through a BA-owned dictionary.
- Tiny CRUD apps with under 10 entities — the ceremony costs more than it saves.
- One-off ad-hoc reports where data lives only in a spreadsheet for a week.
- High-trust regulated domains (HIPAA, PCI, SOX) where data classification MUST be human-signed — agents may draft, humans must approve.

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

- parent skill: `pro/ba/ba-modeling/`
