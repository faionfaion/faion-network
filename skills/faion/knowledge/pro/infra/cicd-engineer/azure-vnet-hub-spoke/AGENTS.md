---
slug: azure-vnet-hub-spoke
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Hub-spoke topology spec: /16 per VNet, /24 per subnet, no CIDR overlap, bidirectional peering, mandatory subnet delegations, Terraform-only changes."
content_id: "f985f627412b4e91"
complexity: deep
produces: spec
est_tokens: 5000
tags: [azure, vnet, hub-spoke, networking, peering, infra]
---
# Azure VNet Hub-Spoke Topology

## Summary

**One-sentence:** Hub-spoke topology spec: /16 per VNet, /24 per subnet, no CIDR overlap, bidirectional peering, mandatory subnet delegations, Terraform-only changes.

**One-paragraph:** Hub-spoke topology spec: /16 per VNet, /24 per subnet, no CIDR overlap, bidirectional peering, mandatory subnet delegations, Terraform-only changes. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Workload spans ≥ 2 VNets and needs east-west connectivity.
- Hub-centralised services (Firewall, Bastion, DNS) are planned.
- AKS or PostgreSQL Flexible Server require subnet delegations.

## Skip If (ANY kills it)

- Single-VNet workload — flat topology suffices.
- Mesh peering policy with no hub.
- Cloud-agnostic platform (Kubernetes everywhere) where the hub-spoke model adds friction.

**Ефективно для:**

- Multi-spoke Azure middle-large enterprise networks.
- Команди де peering одностороннє і трафік silently fails.
- Hub-centralised firewall / Bastion / DNS.
- AKS pod CIDR planning з ≥ /22 reservation.

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
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-azure-vnet-hub-spoke.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
