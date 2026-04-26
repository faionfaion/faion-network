# Azure Compute Services

## Summary

Azure compute covers five service tiers — VMs, VMSS (Flexible mode only for new workloads), AKS, Container Apps (serverless, KEDA-based), and App Service. Choose based on control vs operational overhead: VMs for legacy/custom OS, AKS for complex K8s workloads, Container Apps for event-driven microservices that can scale to zero. Always use Managed Identity instead of credentials in code; use Workload Identity (not the deprecated Pod Identity) in AKS.

## Why

Azure's service spectrum eliminates the false IaaS-vs-PaaS binary: teams pick the exact level of control they need. Spot Priority Mix on VMSS achieves up to 90% cost savings while maintaining a minimum on-demand baseline. Container Apps' scale-to-zero eliminates idle compute costs for variable workloads.

## When To Use

- Designing new cloud-native workloads on Azure
- Migrating existing VM-based applications to containers (AKS or Container Apps)
- Building event-driven microservices that must scale to zero (Container Apps + KEDA)
- Setting up autoscaling for batch processing or ML inference (AKS + KEDA or VMSS Spot Mix)
- Optimizing Azure compute costs with Spot/Reserved/Savings Plans

## When NOT To Use

- Multi-cloud or AWS/GCP-primary environments — use cloud-agnostic tooling (Terraform modules, Kubernetes) instead of Azure-specific APIs
- Windows container workloads on Container Apps — no Windows support; use AKS or App Service
- ARM64 container workloads on Container Apps — not supported as of 2026

## Content

| File | What's inside |
|------|---------------|
| `content/01-service-selection.xml` | Decision rules for VM vs VMSS vs AKS vs Container Apps vs App Service with trade-offs |
| `content/02-aks-practices.xml` | Node pool strategy, Workload Identity setup, KEDA integration, upgrade policy, networking |
| `content/03-container-apps.xml` | Scale-to-zero rules, KEDA scalers, Dapr integration, revision traffic splitting |
| `content/04-cost-security.xml` | Spot Priority Mix calculation, Reserved Instances, Managed Identity pattern, private endpoints |

## Templates

| File | Purpose |
|------|---------|
| `templates/aks-create.sh` | az aks create with workload identity, KEDA, OIDC issuer enabled |
| `templates/vmss-spot-mix.json` | VMSS Flexible orchestration with Spot Priority Mix configuration |
