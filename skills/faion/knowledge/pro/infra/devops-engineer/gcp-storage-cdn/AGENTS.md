---
slug: gcp-storage-cdn
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Configuration for Cloud Storage classes, lifecycle policies, versioning and Cloud CDN cache rules sized to access pattern and retention policy."
content_id: "8e0286e4c94d48d1"
complexity: medium
produces: config
est_tokens: 4000
tags: [gcp, cloud-storage, cloud-cdn, lifecycle, retention]
---
# GCS and Cloud CDN Configuration

## Summary

**One-sentence:** Configuration for Cloud Storage classes, lifecycle policies, versioning and Cloud CDN cache rules sized to access pattern and retention policy.

**One-paragraph:** Configuration for Cloud Storage classes, lifecycle policies, versioning and Cloud CDN cache rules sized to access pattern and retention policy. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `config` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-gcp-storage-cdn.py` before publication.

**Ефективно для:**

- Виставлення lifecycle-правил для production buckets.
- Налаштування retention + bucket lock для регульованих даних.
- Конфігурація Cloud CDN з custom cache keys.

## Applies If (ALL must hold)

- Input matches the methodology scope (gcp-storage-cdn) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `config` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bucket inventory | bucket → access pattern / retention / sensitivity | platform team |
| Retention policy | regulated buckets + minimum retention days | compliance |
| Cache-key requirements | list of static + dynamic asset hosts | frontend team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp]] | upstream context likely already loaded when this methodology fires |

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
| `scripts/validate-gcp-storage-cdn.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[gcp]]
- [[gcp-landing-zone]]
- [[gcp-network-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `lifecycle-rules-mandatory` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
