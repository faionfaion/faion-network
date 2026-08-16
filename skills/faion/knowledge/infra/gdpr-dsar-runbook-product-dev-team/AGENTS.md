# GDPR DSAR Runbook — Product Dev Team

## Summary

**One-sentence:** Engineer-friendly Data-Subject-Access-Request runbook: intake, identity verify, system-by-system extraction, redaction, packaging, 30-day SLA delivery + audit.

**One-paragraph:** Engineer-friendly Data-Subject-Access-Request runbook: intake, identity verify, system-by-system extraction, redaction, packaging, 30-day SLA delivery + audit. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`playbook-step`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Controller status under GDPR (EU/UK personal data subjects).
- ≥1 DSAR per quarter expected at scale; ad-hoc handling not sustainable.
- Multiple systems (DB, blob storage, CRM, analytics) hold subject data.

## Skip If (ANY kills it)

- Processor-only status — controller handles DSAR; provide raw export only.
- No EU/UK subjects — different framework applies.
- Single-system small startup — manual SQL export sufficient; runbook is overhead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Data map | Markdown / data-catalog | DPO + DBA |
| Identity verification mechanism | email + secondary check | support team |
| Subject-id ↔ internal-id mapping | DB | engineering |
| Redaction policy | Markdown | DPO |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/infra/banking-core-data-residency-rules` | Residency rules constrain processing of DSAR data. |
| `pro/infra/devops-engineer/data-retention-policy-template` | Defines retention windows DSAR draws from. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intake_normalise` | haiku | Mechanical request parse. |
| `identity_verify_check` | sonnet | Compose verification challenge from data on file. |
| `system_extraction_orchestrate` | sonnet | Run per-system extracts; reconcile. |
| `redaction_pass` | opus | Cross-document third-party + secret redaction. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dsar-intake.md.j2` | Intake form + initial reply template. |
| `templates/dsar-intake.md` | Intake form + initial reply template. Generated from `templates/dsar-intake.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/extract-orchestration.md.j2` | Per-system extraction checklist. |
| `templates/extract-orchestration.md` | Per-system extraction checklist. Generated from `templates/extract-orchestration.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/redaction-policy.md.j2` | Redaction policy and pass criteria. |
| `templates/redaction-policy.md` | Redaction policy and pass criteria. Generated from `templates/redaction-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/delivery-letter.md.j2` | Final delivery cover letter template. |
| `templates/delivery-letter.md` | Final delivery cover letter template. Generated from `templates/delivery-letter.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum-viable filled-in example (smoke test). |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gdpr-dsar-runbook-product-dev-team.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/infra/`
- `[[banking-core-data-residency-rules]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether gdpr-dsar-runbook-product-dev-team applies: root question — "Is the requester a verified data subject AND we are the controller for their personal data?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
