# FinOps INFORM Phase — Cost Visibility

## Summary

**One-sentence:** Generates an INFORM-phase config (tag taxonomy + cost allocation rules + dashboard sources + KPI baselines) establishing the visibility foundation before any optimization work.

**One-paragraph:** Generates an INFORM-phase config (tag taxonomy + cost allocation rules + dashboard sources + KPI baselines) establishing the visibility foundation before any optimization work. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Старт FinOps-програми: BEFORE будь-який rightsizing / spot / RI.
- Multi-team chargeback / showback де accountability потрібен.
- Audit квартальних cloud-bill сюрпризів.
- M&A integration: уніфікація tag policy між акаунтами.

## Applies If (ALL must hold)

- No tag taxonomy is enforced OR tag coverage <80%.
- Cloud spend lacks per-team / per-product attribution.
- Quarterly cost reviews rely on raw billing files instead of dashboards.
- Stakeholders cannot answer 'what did product X cost last month' in one click.

## Skip If (ANY kills it)

- Tag coverage ≥95% AND dashboards exist AND chargeback already operational — move to OPTIMIZE phase.
- Single-team / single-product account — attribution overhead exceeds the value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Billing export feed | CUR / Billing Export / Cost Mgmt API | Cloud Platform |
| Org structure | YAML (team → products → owners) | Eng leadership |
| Existing tag inventory | CSV (key, value, coverage%) | Cloud Platform |
| Dashboard target | tool (Grafana / Looker / native) + URL | BI team |

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
| `draft-finops-cost-visibility` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-cost-visibility.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
