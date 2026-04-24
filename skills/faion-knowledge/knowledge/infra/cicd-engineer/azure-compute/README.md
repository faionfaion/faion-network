# Azure Compute Services

## Overview

Azure compute services for containerized and VM-based workloads. Covers VMs, VMSS, AKS, Container Apps, and App Service with production best practices.

**Last Updated:** January 2026

## Service Comparison

| Service | Type | Best For | Scaling | Management |
|---------|------|----------|---------|------------|
| **VMs** | IaaS | Legacy apps, custom OS | Manual/VMSS | Full control |
| **VMSS** | IaaS | Stateless scale-out | Auto (flexible) | Some control |
| **AKS** | CaaS | Complex microservices | HPA/KEDA/Cluster | K8s expertise |
| **Container Apps** | Serverless | Event-driven microservices | KEDA (to zero) | Minimal |
| **App Service** | PaaS | Web apps/APIs | Auto/Manual | Minimal |

## Decision Tree

```
Start
 |
 +-- Need full OS control? --> VMs/VMSS
 |
 +-- Containers?
      |
      +-- Need K8s features/control? --> AKS
      |
      +-- Serverless/event-driven? --> Container Apps
      |
      +-- Simple web app? --> App Service (containers)
```

---

## Virtual Machines (VMs)

### When to Use
- Legacy applications requiring specific OS
- Applications with custom kernel requirements
- Lift-and-shift migrations
- Applications with licensing tied to VMs

### Best Practices

| Area | Recommendation |
|------|----------------|
| **Sizing** | Start small, use Azure Advisor recommendations |
| **Availability** | Use Availability Zones for HA (99.99% SLA) |
| **Storage** | Premium SSD for production, Standard for dev/test |
| **Security** | Enable Azure Defender, use Managed Identity |
| **Updates** | Enable Azure Update Manager for patching |
| **Backup** | Azure Backup with geo-redundant storage |

### VM Series Selection

| Series | Use Case | Notes |
|--------|----------|-------|
| **B-series** | Burstable workloads | Cost-effective for variable CPU |
| **D-series** | General purpose | Balanced CPU/memory |
| **E-series** | Memory optimized | Databases, caching |
| **F-series** | Compute optimized | Batch processing |
| **N-series** | GPU workloads | ML training/inference |
| **L-series** | Storage optimized | Big data, databases |

---

## Virtual Machine Scale Sets (VMSS)

### Orchestration Modes

| Mode | Description | Recommendation |
|------|-------------|----------------|
| **Flexible** | Standard VM APIs, mixed instance types | **Recommended for new workloads** |
| **Uniform** | Scale set VM APIs, identical instances | Legacy, being deprecated |

> **Note:** Flexible orchestration is the default since November 2023.

### Best Practices

| Area | Recommendation |
|------|----------------|
| **Orchestration** | Use Flexible mode for new deployments |
| **Fault Domains** | Enable max spreading across zones |
| **Spot Mix** | Use Spot Priority Mix for cost optimization |
| **Health** | Enable Application Health Extension |
| **Upgrades** | Configure rolling upgrades with health probes |
| **Scaling** | Use scaling profiles for predictable patterns |

### Spot Priority Mix

Configure hybrid Spot + On-Demand instances:

| Parameter | Description |
|-----------|-------------|
| `baseRegularPriorityCount` | Minimum on-demand VMs |
| `regularPriorityPercentageAboveBase` | % of on-demand above base |

**Example:** Base=2, Percentage=25%
- 10 VMs total: 2 + (8 * 0.25) = 4 on-demand, 6 spot
- 20 VMs total: 2 + (18 * 0.25) = 6.5 (~7) on-demand, 13 spot

---

## Azure Kubernetes Service (AKS)

### Architecture Components

| Component | Managed By | Notes |
|-----------|------------|-------|
| Control Plane | Microsoft | 99.95% SLA, free |
| Node Pools | Customer | VMs you pay for |
| Add-ons | Microsoft | KEDA, monitoring, policy |

### Node Pool Strategy

| Pool Type | Purpose | Configuration |
|-----------|---------|---------------|
| **System** | Core services | Small VMs, 2-3 nodes, taints |
| **User** | Application workloads | Autoscaling, zones |
| **Spot** | Batch/interruptible | Autoscale 0-N, tolerations |
| **GPU** | ML/AI workloads | N-series, KEDA scaling |

### Best Practices (2025-2026)

| Area | Recommendation |
|------|----------------|
| **Identity** | Workload Identity (not Pod Identity, deprecated) |
| **Scaling** | HPA for pods + Cluster Autoscaler for nodes |
| **KEDA** | Event-driven scaling for queues/events |
| **Networking** | Azure CNI Overlay for large clusters |
| **Security** | Azure Policy, Defender for Containers |
| **Upgrades** | Automatic patch upgrades, maintenance windows |
| **Monitoring** | Container Insights, Prometheus metrics |

### KEDA Integration

Enable KEDA with Workload Identity:
```bash
az aks create \
  --enable-workload-identity \
  --enable-keda \
  --enable-oidc-issuer
```

> **Important:** Enable workload identity add-on BEFORE KEDA add-on.

### AKS Automatic (Preview)

New managed experience where Microsoft manages:
- System node pools
- CoreDNS, KEDA, VPA, Metrics Server
- Core cluster components

Benefits: No system node management, reduced operational overhead.

---

## Azure Container Apps (ACA)

### Architecture

Built on Kubernetes with:
- **Dapr** - Service discovery, state, pub/sub
- **KEDA** - Event-driven autoscaling
- **Envoy** - Traffic management

### Best Practices

| Area | Recommendation |
|------|----------------|
| **Scaling** | Configure min/max replicas, use KEDA rules |
| **Networking** | Use internal ingress for service-to-service |
| **Dapr** | Enable for microservices communication |
| **Secrets** | Use Key Vault references |
| **Revisions** | Use revision labels for traffic splitting |
| **Resilience** | Configure Dapr component resiliency |

### Pricing Plans

| Plan | Description | Best For |
|------|-------------|----------|
| **Consumption** | Pay per vCPU-seconds, GiB-seconds | Variable workloads |
| **Dedicated** | Reserved capacity | Predictable workloads |

### Scale-to-Zero

Container Apps can scale to zero when idle:
- Near-zero cost during idle periods
- First request has cold start latency
- Use min replicas > 0 for latency-sensitive apps

### What's New (2025)

| Feature | Status | Description |
|---------|--------|-------------|
| Confidential Computing | Preview | TEE for data-in-use encryption |
| Rule-based Routing | GA | A/B testing, blue-green |
| Serverless GPUs | GA | AI/ML workloads |
| Code Interpreter | GA | AI agents |

### Limitations

- No Windows container support
- No ARM64 support
- Best for Linux containers only

---

## Azure App Service

### Pricing Tiers

| Tier | Slots | Instances | Features |
|------|-------|-----------|----------|
| **Free/Shared** | 0 | Shared | Development only |
| **Basic** | 0 | 3 | Custom domains |
| **Standard** | 5 | 10 | Slots, autoscale, VNet |
| **Premium** | 20 | 30 | More scale, better perf |
| **Isolated** | 20 | 100 | Full isolation, compliance |

### Deployment Slots Best Practices

| Practice | Description |
|----------|-------------|
| **Never deploy to production directly** | Use staging slot, then swap |
| **Smoke test in staging** | Validate before swap |
| **Configure slot settings** | Mark env-specific settings as "slot setting" |
| **Use auto-swap** | For CD pipelines |
| **Warm up before swap** | Prevents cold start issues |

### Scaling Best Practices

| Type | When to Use |
|------|-------------|
| **Scale Up** | Need more CPU/memory per instance |
| **Scale Out** | Need more instances for load |
| **Automatic Scaling** | Traffic varies unpredictably |

### Cost Optimization

| Strategy | Savings |
|----------|---------|
| Reserved Instances | Up to 55% |
| Dev/Test pricing | Up to 55% |
| Right-size plans | Variable |
| Scale down non-prod | Variable |
| Use slots efficiently | Avoid unused slot instances |

---

## Security Best Practices (All Services)

| Practice | Description |
|----------|-------------|
| **Managed Identity** | No credentials in code |
| **Key Vault** | Secrets management |
| **Private Endpoints** | Keep traffic on Azure backbone |
| **Network Policies** | Restrict pod-to-pod traffic (AKS) |
| **Azure Policy** | Enforce compliance |
| **Defender for Cloud** | Threat detection |
| **TLS 1.3** | Encrypt in transit |

---

## Cost Optimization (All Services)

| Strategy | Description |
|----------|-------------|
| **Spot/Preemptible** | Up to 90% savings for interruptible workloads |
| **Reserved Capacity** | 1-3 year commitments |
| **Right-sizing** | Use Azure Advisor |
| **Scale to Zero** | Container Apps, AKS spot pools |
| **Dev/Test Pricing** | Reduced rates for non-prod |
| **Savings Plans** | Flexible commitment discounts |

---

## References

- [Choose Azure Compute Service](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree)
- [AKS Best Practices](https://learn.microsoft.com/en-us/azure/aks/best-practices)
- [Container Apps Documentation](https://learn.microsoft.com/en-us/azure/container-apps/)
- [App Service Best Practices](https://learn.microsoft.com/en-us/azure/app-service/deploy-best-practices)
- [VMSS Orchestration Modes](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-orchestration-modes)
- [AKS Engineering Blog](https://blog.aks.azure.com/)

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Service-specific checklists |
| [examples.md](examples.md) | Terraform/Bicep examples |
| [templates.md](templates.md) | Reusable templates |
| [llm-prompts.md](llm-prompts.md) | AI assistance prompts |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |

