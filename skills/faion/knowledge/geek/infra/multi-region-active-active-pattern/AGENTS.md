---
slug: multi-region-active-active-pattern
tier: geek
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Active-active multi-region architecture spec: write conflict policy, eventual-consistency budget, partition-tolerance plan, regional failover drill cadence."
content_id: "ae39fb467d635b63"
complexity: deep
produces: spec
est_tokens: 4600
tags: [multi-region, active-active, ha, disaster-recovery, geek, infra]
---

# Multi-Region Active-Active Pattern

## Summary

**One-sentence:** Active-active multi-region architecture spec: write conflict policy, eventual-consistency budget, partition-tolerance plan, regional failover drill cadence.

**One-paragraph:** Active-active multi-region architecture spec: write conflict policy, eventual-consistency budget, partition-tolerance plan, regional failover drill cadence. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`spec`) at a deep complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Service requires RTO <1h AND RPO ≤5min across a regional failure.
- Customer SLA OR regulatory obligation mandates cross-region resilience.
- Engineering org has appetite for eventual-consistency trade-offs OR a CRDT/conflict-free design.

## Skip If (ANY kills it)

- Single-region SLA is sufficient — active-passive suffices.
- Strict-consistency requirement (e.g. ledger) without acceptable eventual-consistency window.
- Cost-bounded workload that cannot justify ≥2× regional infra.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Region selection | Markdown | compliance + infra |
| Data model + consistency requirements | Spec | engineering |
| Conflict-resolution policy | Markdown | this methodology |
| Drill cadence | calendar | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/disaster-recovery-baseline` | Underlying DR strategy. |
| `geek/infra/banking-core-data-residency-rules` | Residency constraints on region selection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | One end-to-end worked example | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `region_selection_spec` | opus | Cross-input regulatory + latency + cost synthesis. |
| `conflict_policy_draft` | sonnet | Per-data-class conflict rules. |
| `drill_runbook` | sonnet | Bounded procedure write. |

## Templates

| File | Purpose |
|------|---------|
| `templates/topology-spec.md` | Region map + traffic policy + data plane. |
| `templates/conflict-policy.md` | Per-data-class conflict rules. |
| `templates/failover-drill.md` | Quarterly drill runbook. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-region-active-active-pattern.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[disaster-recovery-baseline]]`
- `[[banking-core-data-residency-rules]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether multi-region-active-active-pattern applies: root question — "Does the workload require RTO <1h AND RPO ≤5min AND residency allows multi-region?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
