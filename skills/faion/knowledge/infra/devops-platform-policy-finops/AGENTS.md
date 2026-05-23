# Platform Governance: Policy-as-Code + FinOps

## Summary

**One-sentence:** Generates a platform governance bundle: OPA/Gatekeeper admission policies, per-team cost visibility, pre-deployment cost estimation, and embedded policy gates in golden paths.

**One-paragraph:** Generates a platform governance bundle: OPA/Gatekeeper admission policies, per-team cost visibility, pre-deployment cost estimation, and embedded policy gates in golden paths. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- OPA / Gatekeeper як admission gate (labels, resource limits, security).
- Per-team cost visibility поверх chargeback / showback model.
- Pre-merge cost preview через Infracost / OpenCost.
- Policy gates вбудовані в golden paths, не як external review.

## Applies If (ALL must hold)

- Platform has multiple tenants (≥3 product teams) and cross-team standards matter.
- Cost spend per team is visible in billing data (tags or labels).
- OPA / Gatekeeper (or equivalent) is deployable in the substrate.

## Skip If (ANY kills it)

- Single-team platform — admission policies are bureaucracy at this scale.
- Cost data not yet labelled — implement tagging first (`finops-devops-cost-tagging`).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Policy backlog | list (must-have / nice-to-have) | Security / Platform |
| Cost data path | billing export source | FinOps |
| Golden-path inventory | list of templates | Platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-platform-idp-core/AGENTS.md` | IDP framing |

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
| `draft-devops-platform-policy-finops` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-platform-policy-finops.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-platform-idp-core]]
- [[finops]]
- [[finops-devops-cost-alerts]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
