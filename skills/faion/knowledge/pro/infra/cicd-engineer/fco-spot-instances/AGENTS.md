---
slug: fco-spot-instances
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a spot / preemptible instance plan (with checkpointing + interruption handler + instance diversification) delivering 70-90% cost reduction on fault-tolerant workloads.
content_id: "ed3ec088847cf776"
complexity: medium
produces: config
est_tokens: 4200
tags: ["finops", "spot-instances", "preemptible", "cloud-cost", "fault-tolerant"]
---
# FinOps — Spot / Preemptible Instances for Fault-Tolerant Workloads

## Summary

**One-sentence:** Generates a spot / preemptible instance plan (with checkpointing + interruption handler + instance diversification) delivering 70-90% cost reduction on fault-tolerant workloads.

**One-paragraph:** FinOps — Spot / Preemptible Instances for Fault-Tolerant Workloads — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Workload is fault-tolerant: stateless / idempotent / checkpointed / queue-driven.
- Service tolerates 2-minute warning interruptions (AWS Spot, GCP preemptible, Azure Spot).
- Cost saving (70-90%) materially impacts the unit economics of the workload.

## Applies If (ALL must hold)

- Workload is fault-tolerant: stateless / idempotent / checkpointed / queue-driven.
- Service tolerates 2-minute warning interruptions (AWS Spot, GCP preemptible, Azure Spot).
- Cost saving (70-90%) materially impacts the unit economics of the workload.

## Skip If (ANY kills it)

- Long-running stateful services with no checkpoint capability.
- Workloads with strict latency SLO that cannot tolerate replacement gap.

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
| `content/01-core-rules.xml` | essential | 6 testable rules (checkpointing-required, interruption-handler, instance-diversification, max-price-on-demand, on-demand-fallback-for-base, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-fco-spot-instances` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ec2-fleet.json` | EC2 Fleet launch template with spot + on-demand mix + diversification |
| `templates/interruption-handler.sh` | Interruption handler skeleton draining via SIGTERM in 90s |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fco-spot-instances.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[fco-commitment-pricing]]
- [[fco-cost-allocation]]
- [[fco-rightsizing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
