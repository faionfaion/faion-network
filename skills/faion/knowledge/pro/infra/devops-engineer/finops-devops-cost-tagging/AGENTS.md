---
slug: finops-devops-cost-tagging
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Mandatory cost-tagging policy: required keys, normalisation rules, untagged-resource quarantine and chargeback-ready exports."
content_id: "29608e79ecf40f5e"
complexity: light
produces: config
est_tokens: 3200
tags: [finops, tagging, chargeback, cost-allocation, governance]
---
# Cloud Cost Tagging Policy

## Summary

**One-sentence:** Mandatory cost-tagging policy: required keys, normalisation rules, untagged-resource quarantine and chargeback-ready exports.

**One-paragraph:** Mandatory cost-tagging policy: required keys, normalisation rules, untagged-resource quarantine and chargeback-ready exports. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `config` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-finops-devops-cost-tagging.py` before publication.

**Ефективно для:**

- Запуск обов'язкової tag-policy на новому акаунті.
- Чистка untagged-resource хвоста перед закриттям місяця.
- Підготовка chargeback-експорту для фінансів.

## Applies If (ALL must hold)

- Input matches the methodology scope (finops-devops-cost-tagging) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `config` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing resource inventory | CSV from Config / Asset Inventory | cloud provider |
| Cost-centre catalogue | list of approved owner / env / app values | finance |
| Tag-policy enforcement target | SCP or org-policy stub | security team |

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
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-config-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | Annotated configuration skeleton with required keys + comments per knob |
| `templates/_smoke-test.json` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-devops-cost-tagging.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[finops-devops-cost-rightsizing]]
- [[finops-devops-cost-commitments]]
- [[iac-pr-review-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `required-tag-set` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
