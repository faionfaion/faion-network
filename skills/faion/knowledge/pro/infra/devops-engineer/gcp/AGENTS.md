---
slug: gcp
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Decision record selecting GKE Autopilot vs Standard, Cloud Run sizing, Workload Identity Federation and Private Service Connect for production GCP workloads."
content_id: "3832a3057e05703a"
complexity: medium
produces: decision-record
est_tokens: 4000
tags: [gcp, kubernetes, cloud-run, workload-identity, iam]
---
# GCP Production Deployments

## Summary

**One-sentence:** Decision record selecting GKE Autopilot vs Standard, Cloud Run sizing, Workload Identity Federation and Private Service Connect for production GCP workloads.

**One-paragraph:** Decision record selecting GKE Autopilot vs Standard, Cloud Run sizing, Workload Identity Federation and Private Service Connect for production GCP workloads. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `decision-record` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-gcp.py` before publication.

**Ефективно для:**

- Greenfield GKE / Cloud Run deployment на GCP.
- Зняття service-account ключів через Workload Identity Federation.
- Вибір між VPC Peering та Private Service Connect.

## Applies If (ALL must hold)

- Input matches the methodology scope (gcp) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `decision-record` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload classification | table of services with state / GPU / privilege flags | architecture review |
| Org hierarchy snapshot | folder + project list | gcloud organizations list |
| Identity inventory | list of external CI / SaaS callers | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-gke-architecture]] | upstream context likely already loaded when this methodology fires |

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
| `scripts/validate-gcp.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[gcp-gke-architecture]]
- [[gcp-landing-zone]]
- [[gcp-network-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `autopilot-default` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
