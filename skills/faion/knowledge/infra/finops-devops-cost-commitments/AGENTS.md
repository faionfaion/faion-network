# Cloud Commitment Discounts: RIs, Savings Plans, and Spot

## Summary

**One-sentence:** Decision record for cloud commitment portfolio (Reserved Instances, Savings Plans, Spot) sized to workload shape after rightsizing.

**One-paragraph:** Decision record for cloud commitment portfolio (Reserved Instances, Savings Plans, Spot) sized to workload shape after rightsizing. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `decision-record` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-finops-devops-cost-commitments.py` before publication.

**Ефективно для:**

- Planування RI/SP/Spot портфеля після rightsizing.
- Квартальний перегляд commitment-покриття та утилізації.
- Вибір між Convertible та Standard RI під час архітектурного refactor.

## Applies If (ALL must hold)

- Input matches the methodology scope (finops-devops-cost-commitments) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `decision-record` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 90-day cost-and-usage report | CSV/Parquet from cloud billing export | AWS Cost Explorer / GCP BQ billing |
| Workload stability classification | table of services tagged stable/variable/batch | team architecture review |
| Rightsizing output | list of instance families and target sizes | finops-devops-cost-rightsizing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[finops-devops-cost-rightsizing]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-decision-record-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | ADR-style skeleton with context / options / decision / consequences |
| `templates/_smoke-test.md` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-devops-cost-commitments.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[finops-devops-cost-rightsizing]]
- [[finops-devops-cost-tagging]]
- [[finops-devops-cost-kubernetes]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `savings-plan-floor` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
