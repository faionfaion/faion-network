# FinOps Cost Alerts and Anomaly Workflow

## Summary

**One-sentence:** Generates a cost-alert + anomaly investigation spec: threshold alerts (50/75/90/100% of budget), anomaly detector, LLM-assisted investigation prompts, and executive report template.

**One-paragraph:** Generates a cost-alert + anomaly investigation spec: threshold alerts (50/75/90/100% of budget), anomaly detector, LLM-assisted investigation prompts, and executive report template. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Budget threshold alerts (50/75/90/100%) per service / team.
- Anomaly detection через AWS Cost Anomaly / GCP recommender / native.
- LLM-assisted investigation на cost-explorer data dump.
- Executive weekly / monthly cost report з action items.

## Applies If (ALL must hold)

- FinOps Inform phase already running (tagging + dashboards).
- Budgets per team or service can be defined.
- Alert channels (Slack / email / PagerDuty) exist.

## Skip If (ANY kills it)

- No tagging baseline yet — alerts will misfire.
- Budgets cannot be set per team — alert volume will overwhelm.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Budget table | per-team / per-service monthly budget | Finance |
| Anomaly detector source | AWS Cost Anomaly / GCP / native | FinOps |
| Alert channels | table (channel → routing) | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/finops/AGENTS.md` | FinOps cycle context |

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
| `draft-finops-devops-cost-alerts` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-devops-cost-alerts.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[finops]]
- [[devops-platform-policy-finops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
