---
slug: image-digest-pinning-policy
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Policy config pinning container images by SHA256 digest in production manifests with documented rotation cadence and exception register."
content_id: "7a847e4e1acd831f"
complexity: light
produces: config
est_tokens: 3200
tags: [supply-chain, containers, digest, policy, kubernetes]
---
# Container Image Digest Pinning Policy

## Summary

**One-sentence:** Policy config pinning container images by SHA256 digest in production manifests with documented rotation cadence and exception register.

**One-paragraph:** Policy config pinning container images by SHA256 digest in production manifests with documented rotation cadence and exception register. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `config` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-image-digest-pinning-policy.py` before publication.

**Ефективно для:**

- Впровадження digest-pinning у production cluster.
- Налаштування Kyverno / OPA admission gate.
- Документація exception register для legacy images.

## Applies If (ALL must hold)

- Input matches the methodology scope (image-digest-pinning-policy) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `config` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Image inventory | image → tag → digest table from registry | platform team |
| Allowed registry list | registry → trust level mapping | security team |
| Rotation cadence agreement | max-age before re-pin per image class | release manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[iac-pr-review-checklist]] | upstream context likely already loaded when this methodology fires |

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
| `scripts/validate-image-digest-pinning-policy.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[iac-pr-review-checklist]]
- [[kubernetes-deployment]]
- [[helm-charts]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `prod-manifests-by-digest` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
