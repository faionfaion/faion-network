# Azure Networking Checklists

## VNet Planning Checklist

- [ ] Address space planned (non-overlapping with on-premises/other VNets)
- [ ] Subnet sizing calculated (reserve IPs for Azure services)
- [ ] Hub-spoke topology considered for multi-app environments
- [ ] VNet peering or Virtual WAN planned for connectivity
- [ ] DNS strategy defined (Azure DNS, custom DNS, hybrid)
- [ ] Service endpoints enabled for required Azure services
- [ ] Subnet delegations configured for managed services

## NSG Security Checklist

- [ ] Default deny rule at lowest priority (4096)
- [ ] Allow rules use specific ports/protocols (no wildcards)
- [ ] Source/destination use service tags where possible
- [ ] Management ports (22, 3389) restricted to bastion/jumpbox
- [ ] NSG flow logs enabled and sent to Log Analytics
- [ ] NSG associated with all subnets (except Gateway subnet)
- [ ] Application Security Groups used for VM grouping
- [ ] Rules documented with clear naming convention

### NSG Rule Naming Convention

```
{Allow|Deny}{Direction}{Protocol}{Description}
```

Examples:
- `AllowInboundHTTPS`
- `DenyInboundAllTraffic`
- `AllowOutboundSQL`

## NAT Gateway Checklist

- [ ] Standard SKU public IP (static allocation)
- [ ] Zone-redundant public IP for HA
- [ ] Idle timeout configured appropriately (default: 4 min)
- [ ] Associated with private subnets requiring outbound access
- [ ] Outbound IP documented for external allowlisting
- [ ] Monitoring alerts configured for SNAT exhaustion

## Application Gateway Checklist

### Infrastructure

- [ ] Dedicated subnet (no other resources)
- [ ] Subnet size minimum /26 (recommended /24)
- [ ] Subnet delegation to `Microsoft.Network/applicationGateways`
- [ ] Standard_v2 or WAF_v2 SKU selected
- [ ] Autoscaling configured (min: 2, max: based on load)
- [ ] Zone redundancy enabled (zones: 1, 2, 3)

### Security

- [ ] WAF enabled in Prevention mode
- [ ] WAF policy with OWASP 3.2 ruleset
- [ ] Custom WAF rules for application-specific threats
- [ ] SSL policy set to minimum TLS 1.2
- [ ] End-to-end SSL configured
- [ ] SSL certificates managed via Key Vault
- [ ] Diagnostic logs sent to Log Analytics

### Routing

- [ ] Health probes configured for all backends
- [ ] Connection draining enabled
- [ ] Request timeout set appropriately
- [ ] Rewrite rules for header manipulation
- [ ] URL path-based routing where needed

## Front Door Checklist

### Basic Setup

- [ ] Premium tier selected (for Private Link support)
- [ ] Custom domain configured with managed certificate
- [ ] Origin groups configured (separate for public/private)
- [ ] Health probes configured for all origins
- [ ] Caching rules defined per route

### Security

- [ ] WAF policy enabled
- [ ] Bot protection enabled (Premium)
- [ ] Rate limiting configured
- [ ] Geo-filtering rules if required
- [ ] Origin locked to Front Door traffic only

### Private Link (Premium)

- [ ] Private Link enabled for backend origins
- [ ] Multiple origins in different regions for redundancy
- [ ] Private endpoints approved on origin side
- [ ] No mixing of public/private origins in same group

## Private Link / Private Endpoint Checklist

- [ ] Private endpoint created in appropriate subnet
- [ ] Network policy on subnet disabled (or use newer preview)
- [ ] Private DNS zone created for service type
- [ ] Private DNS zone linked to VNet
- [ ] DNS A record automatically registered
- [ ] Connection approved on target resource
- [ ] Public network access disabled on target resource
- [ ] Tested connectivity from within VNet

### Private DNS Zone Names

| Service | Zone Name |
|---------|-----------|
| Storage Blob | `privatelink.blob.core.windows.net` |
| Storage File | `privatelink.file.core.windows.net` |
| SQL Database | `privatelink.database.windows.net` |
| PostgreSQL | `privatelink.postgres.database.azure.com` |
| Key Vault | `privatelink.vaultcore.azure.net` |
| Container Registry | `privatelink.azurecr.io` |
| App Service | `privatelink.azurewebsites.net` |

## Monitoring & Diagnostics Checklist

- [ ] Diagnostic settings enabled on all networking resources
- [ ] Logs sent to Log Analytics workspace
- [ ] NSG flow logs enabled (Version 2)
- [ ] Traffic Analytics enabled
- [ ] Alerts configured for:
  - [ ] NSG rule hits
  - [ ] Application Gateway unhealthy hosts
  - [ ] Front Door origin health
  - [ ] NAT Gateway SNAT exhaustion
  - [ ] Private endpoint connectivity issues

## Security Review Checklist

- [ ] No public IPs on backend VMs/services
- [ ] All PaaS services use private endpoints
- [ ] NSG rules follow least privilege
- [ ] No allow-all rules except for Azure Load Balancer
- [ ] Management access via Azure Bastion only
- [ ] Network Watcher enabled for diagnostics
- [ ] Azure Firewall considered for east-west inspection
- [ ] DDoS Protection Standard for public-facing workloads

## Cost Optimization Checklist

- [ ] Right-size Application Gateway (autoscaling)
- [ ] Front Door caching rules optimized
- [ ] NAT Gateway instances minimized
- [ ] Reserved capacity for predictable workloads
- [ ] Unused public IPs removed
- [ ] VNet peering vs VPN Gateway cost compared
- [ ] Data transfer costs analyzed

---

*Azure Networking Checklists | faion-cicd-engineer*
