# Azure Architecture

Azure enterprise architecture patterns covering the Well-Architected Framework, Landing Zones, and Governance.

## Overview

This methodology provides comprehensive guidance for designing and implementing enterprise-grade Azure infrastructure following Microsoft's best practices and the Cloud Adoption Framework.

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklists for all design areas |
| [examples.md](examples.md) | Terraform/Bicep code examples |
| [templates.md](templates.md) | Reusable infrastructure templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted architecture prompts |

## Azure Well-Architected Framework

The Well-Architected Framework provides guidance across five pillars for designing reliable, secure, and efficient cloud workloads.

### Five Pillars

| Pillar | Focus | Key Questions |
|--------|-------|---------------|
| **Reliability** | Resilience, availability, recovery | Can the system recover from failures? |
| **Security** | Threat protection, data security | How is the workload protected? |
| **Cost Optimization** | Value delivery, waste elimination | Are resources right-sized? |
| **Operational Excellence** | DevOps, monitoring, automation | How are operations managed? |
| **Performance Efficiency** | Scaling, load handling | Can the system adapt to demand? |

### Pillar Details

#### Reliability

- Design for failure recovery at any scale
- Implement highly available architectures
- Plan for data loss, downtime, and ransomware recovery
- Use availability zones and geo-redundancy
- Implement circuit breakers and retry patterns

#### Security

- Protect data at rest and in transit
- Implement Zero Trust architecture
- Use Microsoft Entra ID for identity management
- Enable Microsoft Defender for Cloud
- Encrypt with customer-managed keys where required

#### Cost Optimization

- Right-size resources based on actual usage
- Use Azure Reservations and Savings Plans
- Implement auto-scaling to match demand
- Monitor with Azure Cost Management
- Use spot instances for interruptible workloads

#### Operational Excellence

- Implement Infrastructure as Code (IaC)
- Automate deployments with CI/CD pipelines
- Use Azure Monitor and Log Analytics
- Define runbooks for common operations
- Practice chaos engineering

#### Performance Efficiency

- Scale horizontally before vertically
- Use caching strategies (Redis, CDN)
- Optimize database queries and indexing
- Implement async processing where appropriate
- Monitor performance baselines

## Azure Landing Zones

Landing zones provide the foundation for workload deployment with proper governance, security, and networking.

### Landing Zone Types

| Type | Purpose | Example |
|------|---------|---------|
| **Platform** | Centralized services | Identity, networking, management |
| **Application** | Workload deployment | Production apps, dev environments |

### 8 Design Areas

| # | Design Area | Focus |
|---|-------------|-------|
| 1 | Azure Billing & Entra Tenant | Tenant setup, cost management |
| 2 | Identity & Access Management | Microsoft Entra ID, RBAC, PIM |
| 3 | Management Groups & Subscriptions | Resource organization hierarchy |
| 4 | Network Topology & Connectivity | Hub-spoke, vWAN, Private Link |
| 5 | Security | Microsoft Defender, policies |
| 6 | Management | Monitoring, backup, patching |
| 7 | Governance | Azure Policy, compliance |
| 8 | Platform Automation & DevOps | IaC, CI/CD pipelines |

### Design Principles

| Principle | Description |
|-----------|-------------|
| **Subscription Democratization** | Enable workload teams to manage subscriptions within guardrails |
| **Policy-Driven Governance** | Use Azure Policy for automated compliance |
| **Single Control Plane** | Consistent experience for AppOps and DevOps teams |
| **Application-Centric Migration** | Design around workload requirements |

## Governance Framework

### Management Group Hierarchy

```
Tenant Root Group
├── Platform
│   ├── Identity
│   ├── Management
│   └── Connectivity
├── Landing Zones
│   ├── Corp (internal workloads)
│   └── Online (internet-facing)
├── Sandbox (dev/test)
└── Decommissioned
```

### Best Practices

| Area | Recommendation |
|------|----------------|
| **Hierarchy Depth** | Max 3-4 levels |
| **Policy Assignment** | Assign at management group level, not subscription |
| **RBAC** | Use PIM for privileged access, avoid management group RBAC for app teams |
| **New Subscriptions** | Configure default management group (not root) |
| **Governance as Code** | Deploy policies via CI/CD pipelines |

### Azure Policy Strategy

| Policy Type | Use Case |
|-------------|----------|
| **Built-in** | Prefer over custom where possible |
| **Initiatives** | Group related policies for easier management |
| **Remediation** | Enable automatic remediation where safe |
| **Exemptions** | Use sparingly, set expiration dates |

## Modern Tooling (2025+)

### IaC Recommendations

| Tool | Status | Use Case |
|------|--------|----------|
| **AVM (Azure Verified Modules)** | Recommended | New deployments |
| **ALZ Accelerator** | Recommended | Landing zone setup |
| **Bicep** | Recommended | Native Azure IaC |
| **Terraform** | Supported | Multi-cloud scenarios |
| **ESLZ Module** | Deprecated Aug 2026 | Legacy migrations only |

### Monitoring & Observability

| Tool | Purpose |
|------|---------|
| Azure Monitor | Metrics and logs |
| Log Analytics | Centralized logging |
| Azure Resource Graph | Cross-subscription queries |
| Microsoft Sentinel | Security monitoring |
| Azure Advisor | Recommendations |

## Quick Reference

### Network Patterns

| Pattern | Use Case | Components |
|---------|----------|------------|
| **Hub-Spoke** | Traditional enterprise | VNet peering, Azure Firewall |
| **Virtual WAN** | Global enterprise | vWAN hub, SD-WAN integration |
| **Private Link** | PaaS security | Private endpoints |

### Identity Patterns

| Pattern | Use Case |
|---------|----------|
| **Workload Identity** | AKS pod authentication |
| **Managed Identity** | Azure resource authentication |
| **Service Principal** | CI/CD and automation |

### Cost Optimization Patterns

| Pattern | Savings |
|---------|---------|
| Azure Reservations | Up to 72% |
| Savings Plans | Up to 65% |
| Spot VMs | Up to 90% |
| Right-sizing | 20-40% |

## Related Methodologies

| Methodology | Location |
|-------------|----------|
| AKS Best Practices | [aks-production.md](../aks-production.md) |
| Terraform Patterns | [terraform-modules.md](../../faion-infrastructure-engineer/methodologies/terraform-modules.md) |
| CI/CD for Azure | [github-actions.md](../../faion-cicd-engineer/methodologies/github-actions.md) |

## Sources

- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [Azure Well-Architected Framework Pillars](https://learn.microsoft.com/en-us/azure/well-architected/pillars)
- [Azure Landing Zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/)
- [Landing Zone Design Areas](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas)
- [Azure Governance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/governance)
- [Management Groups](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview)
- [Azure Policy Overview](https://learn.microsoft.com/en-us/azure/governance/policy/overview)
- [Enterprise-Scale GitHub](https://github.com/Azure/Enterprise-Scale)
