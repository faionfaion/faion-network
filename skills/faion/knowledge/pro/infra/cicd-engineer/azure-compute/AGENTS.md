---
slug: azure-compute
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "ADR that pins per-workload Azure compute tier (VM / VMSS / AKS / Container Apps / App Service) with managed identity, workload identity, Spot mix, reserved instance, and cost-optimisation choices."
content_id: "19239e32183ef141"
complexity: deep
produces: decision-record
est_tokens: 4200
tags: [azure, compute, aks, container-apps, vmss, decision-record, infra]
---
# Azure Compute Tier Selection

## Summary

**One-sentence:** ADR that pins per-workload Azure compute tier (VM / VMSS / AKS / Container Apps / App Service) with managed identity, workload identity, Spot mix, reserved instance, and cost-optimisation choices.

**One-paragraph:** ADR that pins per-workload Azure compute tier (VM / VMSS / AKS / Container Apps / App Service) with managed identity, workload identity, Spot mix, reserved instance, and cost-optimisation choices. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Workload is being placed (or re-placed) on Azure.
- Team has clear scaling shape (event-driven vs steady-state).
- Named architect owns the ADR.

## Skip If (ANY kills it)

- Workload is multi-cloud-by-default with cloud-agnostic tooling.
- Windows-container workloads on Container Apps (not supported).
- Latency-critical to non-Azure regions.

**Ефективно для:**

- Greenfield Azure workloads на дизайн-стадії.
- Lift-and-shift VM → containers (AKS or Container Apps).
- Event-driven сервіси з scale-to-zero (Container Apps + KEDA).
- Cost optimisation з Spot + Reserved + Savings Plans.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-adr` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-class-and-tradeoff` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-skeleton.md` | ADR skeleton with status / decision_class / context / decision / alternatives-rejected / consequences / rollback / signers. |
| `templates/_smoke-test.md` | Minimum viable filled-in ADR. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-azure-compute.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
