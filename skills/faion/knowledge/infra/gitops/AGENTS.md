# GitOps Delivery Pattern

## Summary

**One-sentence:** GitOps spec for declarative delivery: repo layout (apps + envs), reconciler choice (Argo CD vs Flux), drift policy and progressive rollout gating.

**One-paragraph:** GitOps spec for declarative delivery: repo layout (apps + envs), reconciler choice (Argo CD vs Flux), drift policy and progressive rollout gating. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `spec` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-gitops.py` before publication.

**Ефективно для:**

- Запуск Argo CD або Flux на новому платформенному кластері.
- Перехід з push-based deploy до Git-as-truth.
- Налаштування progressive rollout для traffic-bearing сервісів.

## Applies If (ALL must hold)

- Input matches the methodology scope (gitops) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `spec` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cluster inventory | cluster name → environment + tenancy | platform team |
| App catalogue | Helm chart + values per app | service teams |
| Promotion policy | manual gates + required approvers per env | release manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[github-actions-cicd]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-spec-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Spec skeleton with scope / components / decisions / risks sections |
| `templates/_smoke-test.md` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitops.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[github-actions-cicd]]
- [[helm-charts]]
- [[kubernetes-deployment]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `git-is-source-of-truth` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
