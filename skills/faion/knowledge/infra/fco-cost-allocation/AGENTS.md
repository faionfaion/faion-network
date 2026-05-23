# FinOps — Cloud Cost Allocation via Tagging

## Summary

**One-sentence:** Generates a tagging policy + enforcement (SCP/Org Policy) + chargeback report wiring so every cloud resource carries accurate metadata for cost attribution to team, service, environment.

**One-paragraph:** FinOps — Cloud Cost Allocation via Tagging — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Multi-team cloud account where shared spend cannot be attributed without tags.
- FinOps / Finance needs to chargeback or showback to product / team owners.
- Compliance regime requires resource ownership traceability.

## Applies If (ALL must hold)

- Multi-team cloud account where shared spend cannot be attributed without tags.
- FinOps / Finance needs to chargeback or showback to product / team owners.
- Compliance regime requires resource ownership traceability.

## Skip If (ANY kills it)

- Single-team account where all spend is owned by that team.
- Spend < $5k/mo where allocation overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[fco-commitment-pricing]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (mandatory-tag-set, enforce-at-creation-not-ex-post, controlled-vocabulary, untagged-resource-alarm, cost-allocation-tags-activated, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-fco-cost-allocation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tag-policy.json` | AWS Tag Policy / GCP Org Policy skeleton enforcing required tag keys |
| `templates/scp-tag-enforcement.json` | SCP skeleton denying resource creation without required tags |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fco-cost-allocation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[fco-commitment-pricing]]
- [[fco-rightsizing]]
- [[fco-spot-instances]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
