# Cloud Waste Elimination and Non-Production Scheduling

## Summary

**One-sentence:** Generates a waste-elimination plan (idle resources audit list + non-prod scheduling config + cleanup automation policy) that targets 25%+ waste reduction and 70% non-prod compute savings.

**One-paragraph:** Generates a waste-elimination plan (idle resources audit list + non-prod scheduling config + cleanup automation policy) that targets 25%+ waste reduction and 70% non-prod compute savings. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Першої FinOps-дії в будь-якому середовищі — zero-risk, immediate ROI.
- Non-prod (dev/staging/QA) що використовується тільки в робочий час.
- Аудиту коли nothing-cleaned >30 днів і waste-rate невідомий.
- Pre-quarterly review: чистимо waste спершу, потім дивимось на справжній spend.

## Applies If (ALL must hold)

- Cloud bill is non-trivial (≥$5k/month) and resource inventory exists.
- First FinOps action in this environment — no waste sweep in past 30 days.
- Non-production environments run 24/7 but are used only during business hours.
- Stakeholder has authority to schedule shutdown and approve deletes.

## Skip If (ANY kills it)

- Automated deletion without a dry-run step first — always audit before destroying.
- Non-prod requires 24/7 (on-call demos, overnight jobs) and no exception process is documented.
- Environment is already running scheduled shutdowns with <30% non-prod waste rate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource inventory snapshot | CSV/JSON from CSP API | Cloud Cost Tool |
| Tag policy | YAML / OPA bundle | Cloud Platform team |
| Non-prod schedule constraints | table (env, on-hours, exceptions) | App owners |
| Approval workflow definition | DAG / RACI | FinOps Lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-fco-waste-elimination` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fco-waste-elimination.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config-instance.json`

```json
{
  "scope": {
    "accounts": [
      "aws:111122223333"
    ],
    "regions": [
      "eu-central-1"
    ],
    "environments": [
      "dev",
      "staging",
      "qa"
    ]
  },
  "idle_audit": [
    {
      "resource_type": "ebs_volume",
      "detector": "status==available AND age_days>7",
      "action": "snapshot-then-delete"
    },
    {
      "resource_type": "elastic_ip",
      "detector": "association==null",
      "action": "release"
    },
    {
      "resource_type": "stopped_instance",
      "detector": "state==stopped AND age_days>30",
      "action": "terminate-with-approval"
    }
  ],
  "schedules": [
    {
      "env": "dev",
      "begin": "08:00",
      "end": "20:00",
      "weekdays": "mon-fri",
      "timezone": "Europe/Warsaw"
    },
    {
      "env": "staging",
      "begin": "06:00",
      "end": "22:00",
      "weekdays": "mon-fri",
      "timezone": "Europe/Warsaw"
    }
  ],
  "exceptions_policy": {
    "tag_key": "waste-exception",
    "required_fields": [
      "reason",
      "owner",
      "expiry"
    ],
    "expiry_days": 90
  },
  "automation": {
    "scanner": "lambda:idle-hunter",
    "frequency": "weekly",
    "dry_run_default": true,
    "notification_channel": "slack:#finops"
  },
  "kpi_targets": {
    "waste_rate_max_pct": 25,
    "untagged_max_pct": 5,
    "non_prod_savings_min_pct": 70
  },
  "owner": "jane@team.io",
  "last_reviewed": "2026-05-23"
}
```
