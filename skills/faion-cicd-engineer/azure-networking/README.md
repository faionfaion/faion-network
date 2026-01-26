# Azure Networking

## Overview

Azure networking infrastructure including Virtual Network (VNet), Network Security Groups (NSG), NAT Gateway, Application Gateway, Azure Front Door, and Private Link. Follows the Azure Well-Architected Framework pillars.

## When to Use

- Network isolation and segmentation with VNet
- Security rules and network policies with NSG
- Outbound connectivity with NAT Gateway
- Layer 7 load balancing with Application Gateway
- Global load balancing and CDN with Front Door
- Private connectivity to PaaS services with Private Link

## Azure Well-Architected Pillars

| Pillar | Focus Areas |
|--------|-------------|
| Reliability | Availability zones, multi-region, recovery |
| Security | Network segmentation, NSG, Private Link |
| Cost Optimization | Right-sizing, reserved capacity |
| Operational Excellence | Monitoring, diagnostics, automation |
| Performance Efficiency | Scaling, caching, CDN |

## Core Components

### Virtual Network (VNet)

Foundation of Azure networking. Provides network isolation and segmentation.

| Component | Purpose |
|-----------|---------|
| Address Space | CIDR blocks (e.g., 10.0.0.0/16) |
| Subnets | Network segmentation (public, private, database) |
| Service Endpoints | Direct connectivity to Azure PaaS |
| Delegations | Subnet dedication for specific services |

### Network Security Group (NSG)

Stateful packet inspection using 5-tuple (source IP, source port, destination IP, destination port, protocol).

| Rule Type | Priority Range | Use Case |
|-----------|----------------|----------|
| Allow Rules | 100-4095 | Permit specific traffic |
| Deny Rules | 4096 | Explicit deny all |
| Default Rules | 65000+ | Azure-managed defaults |

### NAT Gateway

Managed outbound connectivity for private subnets.

| Feature | Benefit |
|---------|---------|
| Static Public IP | Consistent egress IP for allowlisting |
| Zone Redundancy | High availability across AZs |
| Idle Timeout | Configurable (4-120 minutes) |

### Application Gateway

Layer 7 load balancer with WAF capabilities.

| Feature | Use Case |
|---------|----------|
| WAF v2 | OWASP protection, bot mitigation |
| SSL Termination | Certificate management |
| URL-based Routing | Path-based backend selection |
| Autoscaling | Dynamic capacity adjustment |
| Private Link | Private frontend connectivity |

**Key Requirement (2025+):** Subnet delegation to `Microsoft.Network/applicationGateways` required.

### Azure Front Door

Global load balancer with CDN and WAF.

| Tier | Features |
|------|----------|
| Standard | CDN, basic routing, caching |
| Premium | Private Link, advanced WAF, bot protection |

**Private Link Integration:**
- Connect to origins via Azure backbone
- No public exposure required for backends
- Separate origin groups for public vs private origins

### Private Link / Private Endpoint

Private connectivity to Azure PaaS services.

| Component | Purpose |
|-----------|---------|
| Private Endpoint | NIC in your VNet with private IP |
| Private DNS Zone | DNS resolution for private endpoints |
| Private Link Service | Expose your own services privately |

## Architecture Patterns

### Hub-Spoke Topology

```
                    ┌─────────────┐
                    │   Hub VNet  │
                    │  (Shared)   │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │ Spoke VNet 1│ │ Spoke VNet 2│ │ Spoke VNet 3│
    │   (App A)   │ │   (App B)   │ │   (App C)   │
    └─────────────┘ └─────────────┘ └─────────────┘
```

### Front Door + Application Gateway

```
    Internet
        │
        ▼
┌───────────────┐
│  Front Door   │  ← Global LB, CDN, WAF
│   (Premium)   │
└───────┬───────┘
        │ Private Link
        ▼
┌───────────────┐
│  App Gateway  │  ← Regional LB, SSL, WAF
│    (v2)       │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  AKS/App Svc  │  ← Backend workloads
└───────────────┘
```

### Zero Trust Network

1. All traffic encrypted (TLS 1.3)
2. No implicit trust between subnets
3. NSG rules follow least privilege
4. Private endpoints for all PaaS services
5. Azure Firewall for east-west traffic inspection

## Best Practices Summary

| Area | Recommendation |
|------|----------------|
| VNet | Plan address space for growth, use /16 for VNet, /24 for subnets |
| NSG | Deny by default, allow specific, use service tags |
| NAT Gateway | Use for consistent outbound IP, enable zone redundancy |
| App Gateway | Dedicated subnet, enable WAF, use autoscaling |
| Front Door | Use Premium for Private Link, separate origin groups |
| Private Link | Use for all PaaS services in production |
| DNS | Private DNS zones for private endpoints |

## Files in This Folder

| File | Purpose |
|------|---------|
| README.md | This overview document |
| checklist.md | Implementation and security checklists |
| examples.md | Terraform code examples |
| templates.md | Ready-to-use IaC templates |
| llm-prompts.md | AI assistant prompts for Azure networking |

## References

- [Azure Virtual Network Documentation](https://learn.microsoft.com/azure/virtual-network/)
- [Azure Application Gateway](https://learn.microsoft.com/azure/application-gateway/)
- [Azure Front Door](https://learn.microsoft.com/azure/frontdoor/)
- [Azure Private Link](https://learn.microsoft.com/azure/private-link/)
- [Azure Well-Architected Framework - Networking](https://learn.microsoft.com/azure/well-architected/service-guides/)
- [Network Security Best Practices](https://learn.microsoft.com/azure/security/fundamentals/network-best-practices)

---

*Azure Networking | faion-cicd-engineer*
