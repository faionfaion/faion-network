# Banking Core — Data Residency Rules

## Summary

**One-sentence:** Per-jurisdiction data residency spec for core banking workloads: PII residence, processor residence, cross-border transfer locks, supervisory-authority notification triggers.

**One-paragraph:** Per-jurisdiction data residency spec for core banking workloads: PII residence, processor residence, cross-border transfer locks, supervisory-authority notification triggers. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`spec`) at a deep complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Production core-banking workload (deposits, payments, ledger) operating in EU/UK or any jurisdiction with residency law.
- Personal data of customers crosses cloud-region boundaries OR is processed by a third-country processor.
- Subject to EBA / FCA / FINMA / equivalent supervisory framework.

## Skip If (ANY kills it)

- Pre-license fintech with no real customer funds — apply lighter playbook.
- Pure analytics workload with no PII — residency law does not bite.
- Single-jurisdiction workload with no cross-border transfer at all.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Jurisdiction list | Markdown | compliance team |
| Data map | Markdown / data-catalog tool | DPO + DBA |
| Processor list | Spreadsheet / vendor mgmt | procurement |
| Supervisor contact matrix | table | compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/multi-region-active-active-pattern` | How residency interacts with active-active topology. |
| `pro/dev/software-developer/gdpr-dsar-runbook-product-dev-team` | PII handling under DSAR / Article 15. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | One end-to-end worked example | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `residency_data_map` | sonnet | Multi-system data map produced from inventory. |
| `transfer_legality_check` | opus | Schrems II + SCC analysis. |
| `supervisor_notification_draft` | opus | Regulator-facing language; high-stakes synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/residency-spec.md` | Per-jurisdiction residency table + transfer locks. |
| `templates/transfer-impact-assessment.md` | TIA template per Schrems II. |
| `templates/supervisor-notification.md` | Pre-fill for EBA / FCA notification. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-banking-core-data-residency-rules.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[multi-region-active-active-pattern]]`
- `[[gdpr-dsar-runbook-product-dev-team]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether banking-core-data-residency-rules applies: root question — "Does customer PII cross a cloud-region OR third-country boundary?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
