---
slug: data-analysis
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Identify, define, and document data needs before system development — data dictionary, conceptual/logical model, quality dimensions, and business rules as a versioned contract.
content_id: "29ca58ceccac3e3f"
complexity: deep
produces: spec
est_tokens: 4400
tags: [data-analysis, data-dictionary, erd, data-quality, requirements]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-data-analysis.py` | Validate dictionary JSON against output-contract | Pre-commit; CI gate before handoff to developers |

## Related

- [[interface-analysis]]
- [[business-process-analysis]]
- [[ba-planning]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (source-system count, DQ baseline presence, compliance flag) to the right rule. Use when in doubt whether the dictionary is ready to hand off to developers.
