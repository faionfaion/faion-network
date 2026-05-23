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
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fco-waste-elimination.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
