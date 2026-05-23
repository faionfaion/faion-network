# SOC2 Control-to-Repo Artifact Map

## Summary

**One-sentence:** Per-SOC2-control mapping to live repo artifacts (CI config, runbook, IaC file, audit log path) — so auditors and engineers reference the same evidence.

**One-paragraph:** Per-SOC2-control mapping to live repo artifacts (CI config, runbook, IaC file, audit log path) — so auditors and engineers reference the same evidence. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`spec`) at a deep complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Org is pursuing or maintaining SOC2 Type II.
- Engineering team owns infrastructure + change management.
- Auditor expects auditable evidence repeatable across periods.

## Skip If (ANY kills it)

- No SOC2 obligation OR using a vCISO that produces evidence externally.
- Pre-product company — controls not yet operating.
- Existing GRC tool (Vanta / Drata) already maps controls to artifacts and engineers consume it.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| SOC2 control list | Markdown / spreadsheet | compliance team |
| Repo + IaC + CI | GitHub / GitLab | engineering |
| Audit log catalogue | Markdown | audit-logging-baseline |
| Evidence retention SLA | Markdown | compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/audit-logging-baseline` | Source of audit log evidence. |
| `geek/infra/banking-core-data-residency-rules` | Residency artifacts overlap with SOC2 evidence. |

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
| `artifact_search` | sonnet | Find repo artifact matching control. |
| `evidence_freshness_check` | haiku | Mechanical check of last-modified. |
| `control_gap_analysis` | opus | Cross-control synthesis to find uncovered areas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/control-map.yaml` | Per-control mapping to repo artifacts. |
| `templates/evidence-bundle.md` | Audit-ready evidence bundle template. |
| `templates/gap-analysis.md` | Per-quarter gap-analysis report. |
| `templates/_smoke-test.yaml` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-soc2-control-to-repo-artifact-map.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[audit-logging-baseline]]`
- `[[banking-core-data-residency-rules]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether soc2-control-to-repo-artifact-map applies: root question — "Does the org hold SOC2 Type II OR is in audit window AND engineering owns infrastructure?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
