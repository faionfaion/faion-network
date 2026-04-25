# Agent Integration — Azure Compute

## When to use
- Already on Azure (AAD / Entra ID is the IdP, billing is in Azure, networking is in vNets) and need to pick between VMs / VMSS / AKS / Container Apps / App Service.
- Lifting an existing AD-integrated workload that needs Windows VMs, Active Directory, or Azure-specific services (Storage, Service Bus, Key Vault) on the same backbone.
- Greenfield containerized workloads where Container Apps' KEDA + scale-to-zero saves real money vs. always-on AKS node pools.
- Regulated workloads needing Azure-native compliance (FedRAMP, HIPAA BAA, regional sovereignty); cross-cloud migration would lose attestations.

## When NOT to use
- Multi-cloud-by-default org with a vendor-neutral platform (Crossplane, Terraform-only, K8s everywhere) — pure Azure abstractions (Container Apps, App Service slots, ARM/Bicep) lock you in.
- Tiny solo project — App Service Free / Container Apps Consumption are fine, but a single VM on a cheaper provider is often simpler.
- Latency-critical to non-Azure regions / users; Azure's edge story is weaker than AWS CloudFront / Cloudflare.

## Where it fails / limitations
- VMSS Uniform mode is being deprecated; agents copy old Terraform that still defaults to Uniform. Force Flexible orchestration on every new VMSS.
- AKS Pod Identity is deprecated in favor of Workload Identity (OIDC + federated credentials). Agents still scaffold Pod Identity from old blog posts.
- KEDA add-on must be enabled AFTER Workload Identity on AKS — wrong order leaves KEDA without an identity, scalers fail silently.
- Container Apps: no Windows containers, no ARM64, no privileged containers. Agents reach for `--privileged` and the deploy fails late.
- Container Apps revisions: setting `min-replicas: 0` triggers cold starts (5-30s on first request). For latency-sensitive APIs use `min-replicas: 1` and accept the cost.
- App Service slot swap WITHOUT warmup → first requests after swap hit cold workers and 5xx. Always configure `WEBSITE_SWAP_WARMUP_PING_PATH` + `WEBSITE_SWAP_WARMUP_PING_STATUSES`.
- VM/VMSS Spot evictions: 30-second notice via Scheduled Events; agents forget to wire the metadata endpoint and lose work mid-task.
- AKS Cluster Autoscaler vs. Karpenter (now AKS Node Auto-Provisioning preview) — agents mix recommendations, end up with neither truly enabled.
- Quotas (vCPU per region, public IPs, NIC count) bite at scale. New subscriptions have absurdly low defaults; agents file ARM templates that hit quota mid-deploy and leave half-created resources.

## Agentic workflow
Compute selection is THE consequential decision. Have a planning agent produce a decision matrix (workload type, traffic shape, scale-to-zero need, OS reqs, identity model, regulatory constraints) BEFORE any IaC is written. A second agent codifies the choice in Bicep/Terraform with module pinning + `terraform plan` / `bicep build` checks. A reviewer agent diffs the plan against the matrix and flags drift (e.g. matrix said "Container Apps" but the module created an App Service Plan). For day-2 changes (scale rules, image updates) prefer GitOps via ACR webhook → ArgoCD/Flux on AKS, or Container Apps revision-based traffic split — agents should never `az` directly into prod compute.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the spec → IaC → review loop; quality gate must include `az deployment what-if` or `terraform plan` artifact.
- `password-scrubber-agent` — Bicep/Terraform files attract `subscription_id`, SAS tokens, connection strings, AAD app secrets.
- A custom `azure-cost-projector` (Sonnet, read-only) — given a Bicep/TF plan, calls Azure Pricing API and emits monthly burn estimate broken down by SKU.
- A custom `azure-policy-auditor` — runs `az policy state list` against the proposed resources to catch denied SKUs / regions before deploy.

### Prompt pattern
```
Choose Azure compute for <workload>. Inputs: traffic profile (peak QPS, idle %, latency budget ms), OS req, container vs. VM, identity model (Managed Identity preferred), region, compliance constraints, monthly budget USD.
Output: (1) decision matrix (Markdown), (2) chosen service + 2nd-best alternative, (3) high-level Bicep/Terraform skeleton (modules only), (4) scale config (HPA/KEDA rule, min/max), (5) monthly cost projection at p50 and p99 traffic, (6) failure modes specific to chosen service.
Forbid: VMSS Uniform mode, Pod Identity (use Workload Identity), Spot without scheduled-event handler, App Service slot swap without warmup, hardcoded subscription IDs.
```

```
Generate `terraform plan -out=plan.bin` then `terraform show -json plan.bin`. For every resource in the plan, emit JSON {address, type, sku, region, est_monthly_usd, identity_type, network_exposure}. Reject if any compute resource has identity_type == "SystemAssigned-only" AND requires access to Key Vault / SQL — must use Workload Identity / federated credential.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `az` (Azure CLI) | All Azure mgmt; agent-driven via `--query` (JMESPath) and `-o json` | https://learn.microsoft.com/cli/azure |
| `az aks get-credentials` / `kubelogin` | Pull AKS kubeconfig with AAD auth | https://azure.github.io/kubelogin/ |
| `az containerapp` | Container Apps lifecycle, revisions, traffic split | https://learn.microsoft.com/cli/azure/containerapp |
| `az deployment what-if` | ARM/Bicep dry-run; show what changes before apply | https://learn.microsoft.com/azure/azure-resource-manager/bicep/deploy-what-if |
| `bicep` CLI | Compile Bicep → ARM, lint, decompile | https://learn.microsoft.com/azure/azure-resource-manager/bicep/install |
| Azure Developer CLI (`azd`) | App-template-driven deploys for Container Apps / App Service / AKS | https://learn.microsoft.com/azure/developer/azure-developer-cli/ |
| Terraform AzureRM provider | Multi-cloud-style IaC for Azure | https://registry.terraform.io/providers/hashicorp/azurerm/latest |
| `kubectl` + `helm` + `kustomize` | AKS day-2 ops | upstream |
| `kured` | Auto-reboot AKS nodes after kernel patch | https://kured.dev |
| `Azure Pricing API` (REST) | Cost projection inside agent loop | https://learn.microsoft.com/rest/api/cost-management/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Azure VMs / VMSS | IaaS (SaaS-mgmt) | Yes | Full `az vm` / `az vmss` CLI; Flexible orchestration is the only sane choice for new VMSS. |
| Azure Kubernetes Service (AKS) | Managed K8s | Yes | Standard kubectl/Helm; agents drive via Workload Identity → KV / SB / Storage. |
| Azure Container Apps | Serverless containers | Yes | KEDA built-in, Dapr optional; revisions enable safe canary. No Windows / ARM64. |
| Azure Container Apps Jobs | Serverless batch | Yes | Run-to-completion containers — perfect for agentic LLM batch workloads. |
| Azure App Service | PaaS | Yes | Slot swap is killer feature; agents must add warmup. |
| Azure Functions | Serverless | Partial | Great for event-driven glue; cold starts under Consumption hurt. |
| Azure Container Registry (ACR) | SaaS | Yes | Tasks for in-cloud builds; works with cosign + Notary v2. |
| Azure Key Vault | SaaS | Yes | Pair with Workload Identity / Managed Identity — never inline secrets. |
| Azure Monitor / Log Analytics | SaaS | Yes | KQL via `az monitor log-analytics query`; agents can ingest pipeline logs. |
| Azure Front Door / Application Gateway | SaaS | Partial | WAF rules work; agent diffing of rule sets is fragile, prefer Bicep modules. |
| Bicep + Azure Verified Modules | OSS | Yes | Curated module registry; pin versions, agents read inputs/outputs reliably. |

## Templates & scripts
See `templates.md` and `examples.md` for Bicep + Terraform modules. Cost-projection one-liner agents can wire into a CI gate (≤25 lines):

```bash
#!/usr/bin/env bash
# scripts/azure-plan-cost.sh — emits JSON cost projection from a terraform plan.
set -euo pipefail
PLAN="${1:-tfplan.bin}"
REGION="${AZURE_REGION:-westeurope}"

terraform show -json "$PLAN" \
  | jq -r '
      .resource_changes[]
      | select(.change.actions[] | IN("create","update"))
      | select(.type | startswith("azurerm_"))
      | {addr: .address, type: .type, sku: (.change.after.sku_name // .change.after.sku // "n/a")}
    ' \
  | while read -r line; do
      sku=$(echo "$line" | jq -r '.sku')
      type=$(echo "$line" | jq -r '.type')
      [[ "$sku" == "n/a" ]] && continue
      price=$(curl -s "https://prices.azure.com/api/retail/prices?\$filter=armRegionName eq '$REGION' and skuName eq '$sku'" \
        | jq -r '.Items[0].retailPrice // 0')
      echo "{\"resource\": \"$type\", \"sku\": \"$sku\", \"hourly_usd\": $price, \"monthly_usd\": $(echo "$price * 730" | bc -l)}"
    done | jq -s 'sort_by(-.monthly_usd)'
```

## Best practices
- Default to Managed Identity / Workload Identity. Any access key, SAS, or AAD client secret in IaC is a review-blocker.
- Use Availability Zones for production VMs/AKS — single-region single-zone gives 99.9% best case.
- Pin AKS Kubernetes version + node image; let auto-upgrade run on a maintenance window, not arbitrary.
- KEDA scalers: pin to one of (CPU, queue depth, HTTP RPS, custom). Multiple competing scalers thrash.
- App Service: enable "Always On" for non-Consumption tiers, configure slot warmup, set `WEBSITE_RUN_FROM_PACKAGE=1` for atomic deploys.
- Container Apps: pin `min-replicas: 1` for any user-facing API (cold start tax otherwise); use `min-replicas: 0` for batch / async only.
- Use Azure Policy + Defender for Cloud as guardrails; agents read policy assignments before generating IaC to avoid denied-by-policy SKUs.
- Pin Bicep modules to AVM (Azure Verified Modules) versions; do not embed inline `Microsoft.Compute/...` API versions copy-pasted from old samples.
- Tag every resource with `{owner, env, costCenter, purpose}` — agents must add tags or the FinOps audit fails.

## AI-agent gotchas
- Agents pick a region by name without checking SKU availability — `Standard_D4ds_v5` exists in `westeurope` but not in `swedencentral` Spot. Force a `az vm list-skus -l <region>` check before generating IaC.
- Quota limits cause partial deploys: agents apply, hit a vCPU quota, leave half-created NICs / disks. Always run `az deployment group what-if` AND check `az vm list-usage` first.
- "Subscription" vs. "tenant" vs. "management group" confusion → agents create resources in the wrong subscription. Bind subscription ID via `az account set --subscription` at the very top of any script and assert via `az account show`.
- Service principal vs. managed identity: agents default to creating a SP because samples do; SP secrets expire and rotate poorly. Prefer Managed Identity / Workload Identity; only use SP for cross-tenant edge cases.
- Soft-delete on Key Vault / Storage: agents `terraform destroy` and the next `apply` fails because the name is reserved for 7-90 days. Use `--purge` or rename — and document the choice.
- Human-in-loop checkpoints: any AAD app registration, role assignment at subscription scope, or `Owner` grant MUST require explicit human approval. These are credential-equivalent.
- Costs creep silently: agents add a Premium SSD + GRS Storage + always-on App Service Plan; no one notices for a billing cycle. Wire cost projection into the PR check.

## References
- Azure compute decision tree — https://learn.microsoft.com/azure/architecture/guide/technology-choices/compute-decision-tree
- AKS best practices — https://learn.microsoft.com/azure/aks/best-practices
- Container Apps docs — https://learn.microsoft.com/azure/container-apps/
- App Service deploy best practices — https://learn.microsoft.com/azure/app-service/deploy-best-practices
- Workload Identity on AKS — https://learn.microsoft.com/azure/aks/workload-identity-overview
- VMSS Flexible orchestration — https://learn.microsoft.com/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-orchestration-modes
- Azure Verified Modules (Bicep + Terraform) — https://aka.ms/avm
- Bicep what-if — https://learn.microsoft.com/azure/azure-resource-manager/bicep/deploy-what-if
- Azure Pricing API — https://learn.microsoft.com/rest/api/cost-management/
