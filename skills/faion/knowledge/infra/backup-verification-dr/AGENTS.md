# Backup Verification + Disaster Recovery Drills

## Summary

**One-sentence:** Produces an automated backup verification report (restore-drill cron + Prometheus alerting on age/size anomalies + DR runbook) that proves the RPO/RTO target before an incident.

**One-paragraph:** Backup Verification + Disaster Recovery Drills — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a report that the downstream agent can verify with the included validator.

**Ефективно для:**

- An existing backup pipeline (database, filesystem, K8s) needs proof-of-restore before relying on it for DR.
- Compliance regime (SOC2, ISO27001, HIPAA) requires quarterly restore drills.
- RPO/RTO objectives are documented and need observable verification.

## Applies If (ALL must hold)

- An existing backup pipeline (database, filesystem, K8s) needs proof-of-restore before relying on it for DR.
- Compliance regime (SOC2, ISO27001, HIPAA) requires quarterly restore drills.
- RPO/RTO objectives are documented and need observable verification.

## Skip If (ANY kills it)

- Backup pipeline is not yet in place — implement the producer methodology first.
- Toy/dev environment with no recovery objective.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[backup-database-postgres]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (restore-drill-cron, alert-on-stale-backup, alert-on-size-anomaly, dr-runbook-as-code, rpo-rto-measured, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the report + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-backup-verification-dr` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dr-runbook.md.j2` | DR runbook skeleton with tagged steps |
| `templates/dr-runbook.md` | DR runbook skeleton with tagged steps Generated from `templates/dr-runbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/backup-config.example.json` | Filled report artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backup-verification-dr.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/infra/cicd-engineer/`
- [[backup-database-postgres]]
- [[backup-filesystem-restic]]
- [[backup-kubernetes-velero]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/backup-config.example.json`

```json
{
  "drill_schedule": {
    "cron": "x",
    "rpo_seconds_target": "x",
    "rto_seconds_target": "x"
  },
  "metrics": [
    "x",
    "x",
    "x"
  ],
  "alerts": [
    "x",
    "x",
    "x"
  ],
  "runbook_path": "example-value",
  "last_drill_pass": "example-value"
}
```
