# Data Analysis

## Summary

A structured approach to identifying, defining, and documenting data needs before system development. Covers data requirements gathering, data element definition, conceptual/logical/physical modeling, data quality assessment across six dimensions, and data business rules. Produces a data dictionary and data requirements document that developers and architects use as authoritative data contracts.

## Why

Data exists in multiple systems with inconsistent definitions; reports show conflicting numbers; integration projects fail due to undiscovered schema mismatches. By mapping data entities, attributes, quality dimensions, and ownership before development, the BA prevents costly rework and ensures systems share a common data language.

## When To Use

- Starting database or integration design and no shared data dictionary exists
- Reports from different systems show conflicting figures for the same metric
- Building ETL/integration layer between two or more systems
- Assessing data migration scope before cutover
- Data quality issues are causing operational problems and no baseline measurement exists
- Compliance requires documented data ownership and classification (GDPR, HIPAA)

## When NOT To Use

- Exploratory analytics spike where the data model will be thrown away — just query and iterate
- Event streaming architectures where schema-on-read is intentional; a rigid dictionary adds friction
- Frontend-only features with no new data persistence
- When an authoritative data dictionary already exists and is up to date — extend it, do not duplicate
- Pure UI/UX research where the output is a prototype, not a data model

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Data analysis components, five-step process, data modeling levels (conceptual/logical/physical), ER notation |
| `content/02-quality-rules.xml` | Six quality dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness) with measurable metrics |
| `content/03-examples.xml` | Customer entity definition, data quality assessment findings, common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-dictionary.md` | Per-entity template: attributes table, example records, relationships, business rules |
| `templates/data-requirements.md` | Project-level data requirements: entities, attributes, derived data, quality thresholds, volumes, integration, security |
| `templates/data-quality-assessment.md` | Assessment report per quality dimension with scoring table and recommendations |
