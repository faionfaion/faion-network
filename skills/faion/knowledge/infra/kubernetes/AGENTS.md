# Kubernetes Production Readiness

## Summary

**One-sentence:** Production-readiness checklist for Kubernetes workloads: resource requests + limits, three probes, hardened security context, PDB, image pinning and HPA wiring.

**One-paragraph:** Production-readiness checklist for Kubernetes workloads: resource requests + limits, three probes, hardened security context, PDB, image pinning and HPA wiring. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `checklist` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-kubernetes.py` before publication.

**Ефективно для:**

- Production readiness review для нового сервісу.
- Аудит resource requests / limits / probes на існуючих Deployment.
- Виставлення PDB + HPA + security context на бойових namespaces.

## Applies If (ALL must hold)

- Input matches the methodology scope (kubernetes) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `checklist` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload manifest | Deployment / StatefulSet YAML under review | service team |
| Observed utilisation | P95 CPU / memory from prior staging run | observability team |
| Cluster constraints | PodSecurityStandard level + admission policies | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kubernetes-deployment]] | upstream context likely already loaded when this methodology fires |

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
| draft-checklist-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/checklist.md` | Checklist skeleton with id / rule / MUST/SHOULD / evidence columns |
| `templates/_smoke-test.md` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kubernetes.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[kubernetes-deployment]]
- [[helm-charts]]
- [[image-digest-pinning-policy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `requests-limits-on-every-container` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
