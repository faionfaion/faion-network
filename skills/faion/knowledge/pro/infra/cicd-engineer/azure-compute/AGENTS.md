---
slug: azure-compute
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Azure compute covers five service tiers — VMs, VMSS (Flexible mode only for new workloads), AKS, Container Apps (serverless, KEDA-based), and App Service.
content_id: "0ebe70c62b901376"
tags: [azure, compute, aks, container-apps, vmss]
---
# Azure Compute Services

## Summary

**One-sentence:** Azure compute covers five service tiers — VMs, VMSS (Flexible mode only for new workloads), AKS, Container Apps (serverless, KEDA-based), and App Service.

**One-paragraph:** Azure compute covers five service tiers — VMs, VMSS (Flexible mode only for new workloads), AKS, Container Apps (serverless, KEDA-based), and App Service. Choose based on control vs operational overhead: VMs for legacy/custom OS, AKS for complex Kubernetes workloads, Container Apps for event-driven microservices that can scale to zero. Always use Managed Identity instead of credentials in code; use Workload Identity (not the deprecated Pod Identity) in AKS.

## Applies If (ALL must hold)

- Already on Azure (AAD / Entra ID is the IdP, billing is in Azure, networking is in vNets) and need to pick between VMs / VMSS / AKS / Container Apps / App Service.
- Lifting an existing AD-integrated workload that needs Windows VMs, Active Directory, or Azure-specific services (Storage, Service Bus, Key Vault) on the same backbone.
- Greenfield containerized workloads where Container Apps' KEDA + scale-to-zero saves real money vs always-on AKS node pools.
- Regulated workloads needing Azure-native compliance (FedRAMP, HIPAA BAA, regional sovereignty); cross-cloud migration would lose attestations.
- Designing new cloud-native workloads on Azure.
- Migrating existing VM-based applications to containers (AKS or Container Apps).
- Building event-driven microservices that must scale to zero (Container Apps + KEDA).
- Setting up autoscaling for batch processing or ML inference (AKS + KEDA or VMSS Spot Mix).
- Optimizing Azure compute costs with Spot/Reserved/Savings Plans.

## Skip If (ANY kills it)

- Multi-cloud-by-default org with a vendor-neutral platform (Crossplane, Terraform-only, Kubernetes everywhere) — pure Azure abstractions (Container Apps, App Service slots, ARM/Bicep) lock you in.
- Tiny solo project — App Service Free / Container Apps Consumption are fine, but a single VM on a cheaper provider is often simpler.
- Latency-critical to non-Azure regions / users; Azure's edge story is weaker than AWS CloudFront / Cloudflare.
- Multi-cloud or AWS/GCP-primary environments — use cloud-agnostic tooling (Terraform modules, Kubernetes) instead of Azure-specific APIs.
- Windows container workloads on Container Apps — no Windows support; use AKS or App Service.
- ARM64 container workloads on Container Apps — not supported as of 2026.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
