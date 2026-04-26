# Azure Management Group Hierarchy

## Standard Enterprise Structure

```
Tenant Root Group
└── {{org-name}}-root  (Intermediate Root)
    ├── platform
    │   ├── management        ← Log Analytics, Defender, Automation
    │   ├── connectivity      ← Hub VNet, Firewall, ExpressRoute/VPN
    │   └── identity          ← AD DS, ADFS (if needed)
    ├── landing-zones
    │   ├── corp              ← Corpnet-connected workloads
    │   │   ├── production
    │   │   └── non-production
    │   └── online            ← Internet-facing workloads
    │       ├── production
    │       └── non-production
    ├── sandboxes             ← Dev/Explore — relaxed policy, auto-expire
    └── decommissioned        ← Quarantine before deletion
```

## Design Principles

| Principle | Guideline |
|-----------|-----------|
| Depth | Max 6 levels (Azure limit). Keep to 3-4 in practice. |
| Policy scope | Assign Azure Policy at MG level, never at subscription |
| RBAC scope | Prefer MG-level role assignments for platform team |
| Subscription purpose | One workload / one environment per subscription (isolation) |
| Naming | `{{org}}-{{type}}-{{env}}` e.g. `contoso-corp-prod` |

## Policy Assignment Points

| Management Group | Key Policies |
|------------------|-------------|
| Tenant Root | Deny classic resources, require tags |
| platform/connectivity | Deny VNet creation outside hub pattern |
| landing-zones/corp | Require private endpoints, deny public IP on NICs |
| landing-zones/online | Allow public IP (controlled), enforce WAF on App GW |
| sandboxes | Allow most, enforce spend budget alert |

## Subscription Vending Checklist

- [ ] Subscription placed in correct MG (corp vs online)
- [ ] Budget alert set (email + action group)
- [ ] Defender for Cloud enabled (inherited from MG policy)
- [ ] Diagnostic settings → central Log Analytics workspace
- [ ] Tags: `environment`, `team`, `cost-center`, `data-classification`
- [ ] Network: peer to hub VNet (corp) or stand-alone (online)

## IaC Reference

Manage hierarchy via AVM (Azure Verified Modules):
```
module "management_groups" {
  source  = "Azure/avm-ptn-alz/azurerm"
  version = "~> 0.10"
  # ... ALZ pattern config
}
```

Note: ESLZ (Enterprise-Scale Landing Zone) deprecated August 2026 → migrate to AVM.
