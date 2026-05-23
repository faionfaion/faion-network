# Helm Chart Authoring

## Summary

**One-sentence:** Helm chart scaffold: Chart.yaml v2 with kubeVersion, values.schema.json, pinned dependencies, lint-clean templates and test hooks.

**One-paragraph:** Helm chart scaffold: Chart.yaml v2 with kubeVersion, values.schema.json, pinned dependencies, lint-clean templates and test hooks. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `code` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-helm-charts.py` before publication.

**Ефективно для:**

- Авторинг нового Helm-chart для in-house сервісу.
- Додавання values.schema.json до існуючого chart.
- Pinning + Chart.lock для chart з зовнішніми залежностями.

## Applies If (ALL must hold)

- Input matches the methodology scope (helm-charts) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `code` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Application spec | container image + ports + env contract | service team |
| Target cluster constraint | min Kubernetes version + ingress class | platform team |
| Values surface | list of operator-tunable knobs | owner of the app |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kubernetes]] | upstream context likely already loaded when this methodology fires |

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
| draft-code-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Chart.yaml` | Working scaffold (Chart.yaml / Jenkinsfile / nginx.conf depending on slug) |
| `templates/_smoke-test.yaml` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-helm-charts.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[kubernetes]]
- [[kubernetes-deployment]]
- [[gitops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `chart-yaml-v2-strict` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
