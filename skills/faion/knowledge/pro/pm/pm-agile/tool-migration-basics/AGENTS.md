---
slug: tool-migration-basics
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spec for migrating project-management data between tools: pre-migration audit, field mapping, ETL execution, post-cutover validation.
content_id: "93b1cf06b275a89d"
complexity: medium
produces: spec
est_tokens: 4900
tags: [migration, pm-tools, data-etl, jira, linear]
---
# Cross-Tool Migration Basics

## Summary

**One-sentence:** Spec for migrating project-management data between tools: pre-migration audit, field mapping, ETL execution, post-cutover validation.

**One-paragraph:** Spec for migrating project-management data between tools: pre-migration audit, field mapping, ETL execution, post-cutover validation. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-tool-migration-basics.py` enforces the output contract.

**Ефективно для:**

- Migrating a single team from Jira → Linear / GitHub Projects / ClickUp.
- Consolidating ≤3 boards into one tool before a larger org-wide migration.
- Auditing whether a proposed migration is feasible without data loss.

## Applies If (ALL must hold)

- Source tool has a documented export API or CSV export.
- Target tool supports the source's field types (or you accept lossy mapping).
- <500 active issues and <5 custom fields — otherwise use tool-migration-process.

## Skip If (ANY kills it)

- Org-wide migration with >3 boards — use tool-migration-process.
- Source data quality is unknown — audit first.
- No business sponsor for the migration.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source export | CSV/JSON via API | source tool admin |
| Target field schema | JSON | target tool admin |
| Field-mapping table | Markdown/YAML | PM + admin |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tool-migration-process]] | for >3-board migrations, use the full process spec |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-field-map` | sonnet | Judgement on lossy mappings + default-on-miss. |
| `run-count-check` | haiku | Mechanical row-count diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/field-mapping.md` | Field-mapping template with source × target × transform × default-on-miss |
| `templates/count-check.py` | Pre/post count-check script to verify no rows lost |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-migration-basics.py` | Validate the spec artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[tool-migration-process]]
- [[scrum-ceremonies]]
- [[change-control]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

