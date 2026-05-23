# Cross-Tool Migration

## Summary

**One-sentence:** Six-phase ETL for migrating a project-management tool portfolio (Jira/Linear/Asana/ClickUp/GitHub Projects/Azure DevOps) with field mapping, identity merge, cutover plan, and rollback gate.

**One-paragraph:** Six-phase ETL for migrating a project-management tool portfolio (Jira/Linear/Asana/ClickUp/GitHub Projects/Azure DevOps) with field mapping, identity merge, cutover plan, and rollback gate.

**Ефективно для:**

- Підняття workspaces після M&A, де дві компанії мали різні PM-стеки.
- Платформних консолідацій, де PMO зменшує tool-портфоліо з 4 до 1.
- Контрактних переходів від one tool до іншого (часто Jira→Linear, ADO→GitHub Projects).
- Tier-downgrade, коли організація зменшує team size і потребує легшого тулу.

## Applies If (ALL must hold)

- Source and target tools have stable export/import APIs.
- Migration window can be planned (≥2-week runway).
- Identity merge plan exists (SSO mapping users → users).
- Rollback path documented before cutover.

## Skip If (ANY kills it)

- <50 active work items — manual recreate is faster.
- Source tool will be decommissioned with no field-fidelity requirement.
- Target tool lacks at least 80% of field-type parity.
- Compliance regime forbids data movement (data residency).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-tool-selection]] | Why target was picked over alternatives. |
| [[change-control]] | Migration is a controlled change with rollback gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `field-mapper` | opus | Author target ↔ source field map with type coercions. |
| `export-runner` | haiku | Mechanical export from source API. |
| `import-runner` | haiku | Mechanical import into target API. |
| `identity-merger` | sonnet | Map source user IDs to target user IDs via SSO. |
| `cutover-orchestrator` | opus | Sequence freeze-export-import-verify-cutover-rollback gates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/migration-plan.md` | Six-phase plan: discover, map, dry-run, cutover, verify, decommission. |
| `templates/field-map.yaml` | Source → target field map with type coercions and defaults. |
| `templates/cutover-runbook.md` | Hour-by-hour runbook with rollback decision points. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-tool-migration.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[pm-tool-selection]]
- [[change-control]]
- [[jira-workflow-management]]
- [[azure-devops-boards]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (work_item_count, field_parity_pct, identity_merge_complexity) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
