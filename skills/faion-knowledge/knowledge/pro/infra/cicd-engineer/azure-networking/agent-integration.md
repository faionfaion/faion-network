# Agent Integration — Azure Networking

## When to use
- Designing landing-zone networks (Hub-Spoke, Virtual WAN) for new Azure subscriptions, with NSG / route tables / private DNS shipped via IaC.
- Migrating workloads from public PaaS endpoints to Private Link + Private Endpoints (compliance, data exfiltration controls).
- Putting Application Gateway WAF v2 or Azure Front Door Premium in front of AKS/App Service/Functions.
- Standardizing zero-trust east-west controls (Azure Firewall, NSG, deny-by-default subnet routing).
- Creating consistent egress IPs via NAT Gateway for third-party allowlisting.

## When NOT to use
- Single-region, single-VNet, single-team workload that doesn't cross subscriptions — full hub-spoke is overkill, use a flat VNet.
- Cost-sensitive POCs (App Gateway v2 + Front Door Premium combined ≈ hundreds USD/month idle).
- When the platform team can't operate Private DNS zones reliably — broken DNS makes Private Link a debugging nightmare.
- Anything time-sensitive in dev/test where Front Door's 5-15 min config propagation will eat your iteration time.

## Where it fails / limitations
- App Gateway v2 (since 2025) requires subnet delegation to `Microsoft.Network/applicationGateways`; agents that copy older Terraform fail at deploy.
- NSGs are stateful but the inbound/outbound default rules are easy to misread; agents add an "Allow 80" rule and forget that the implicit deny still wins for non-default direction.
- Private Endpoints break public DNS by default in the same VNet. Without `privatelink.blob.core.windows.net` zone linked to every consumer VNet, resolution lands on the public IP and connects fine — to the public endpoint, defeating the entire purpose.
- NAT Gateway has SNAT port exhaustion (~64k per public IP); high-fanout outbound (web scrapers, batch HTTP) silently drops connections at the edge.
- Front Door + App Gateway chained without Private Link sends traffic over the public internet between them — the docs imply but don't enforce private chaining.
- VNet peering does not transit through a third VNet by default; agents draw the diagram and forget UDR / Azure Firewall is needed for hub transit.
- Service Endpoints and Private Endpoints look interchangeable but aren't: Service Endpoints leak via subnet identity; Private Endpoints inject an IP into your VNet. Agents pick the wrong one.

## Agentic workflow
Network changes are blast-radius high. Have a planner agent produce a topology diff (current → target) including subnet CIDRs, NSG rules, peerings, route tables, DNS zones; an implementation agent emits Terraform/Bicep; a reviewer agent (Opus) runs `terraform plan` analysis and checks: (1) no public IPs added without justification, (2) every Private Endpoint has matching Private DNS zone link, (3) no NSG rule is `Any/Any/Allow`, (4) NAT Gateway IP count vs expected outbound concurrency. Always go through `what-if` (Bicep) or `terraform plan` review before apply; never run `az network ... create` ad-hoc.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → plan → review → apply.
- A custom `azure-network-blast-radius-auditor` (Opus, read-only) — given Terraform plan JSON, lists every resource that gains a public IP, every NSG rule loosened, every peering added, with risk score and rollback steps.
- `password-scrubber-agent` — Bicep param files often inline service-principal client secrets.

### Prompt pattern
```
Design Azure landing-zone network for <workload>.
Inputs: regions, subscription topology, expected RPS, compliance class, third-party allowlist needs.
Output: (1) VNet/subnet CIDR plan (Markdown table with growth headroom), (2) NSG ruleset (deny-by-default), (3) Private Endpoint + Private DNS zone matrix, (4) NAT Gateway sizing (SNAT ports/IP), (5) Front Door / App Gateway chaining diagram with WAF mode (prevention/detection), (6) Bicep or Terraform code, (7) rollback runbook.
Forbid: any-any NSG rules, public IP without justification, Service Endpoints when Private Endpoints fit, App Gateway without subnet delegation.
```

```
Review terraform plan JSON. Output JSON:
{public_ips_added: [...], nsg_loosened: [...], peerings_added: [...], pe_without_dns_zone: [...], nat_undersized: [...], approve: bool, blockers: [...]}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `az` (Azure CLI) | All Azure operations | https://learn.microsoft.com/cli/azure/ |
| `az network watcher` | Connection troubleshoot, packet capture | https://learn.microsoft.com/azure/network-watcher/ |
| `az bicep` / Bicep CLI | DSL for ARM | https://learn.microsoft.com/azure/azure-resource-manager/bicep/ |
| `terraform` + `azurerm`/`azapi` providers | IaC | https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs |
| `kubelogin` | AKS auth | https://github.com/Azure/kubelogin |
| `psping` / `tcping` (Sysinternals) | TCP-level reachability checks | https://learn.microsoft.com/sysinternals/downloads/psping |
| `nslookup` / `dig` | Validate Private DNS resolution | builtin / bind-utils |
| `nmap` | Confirm NSG behavior from peer VNet | https://nmap.org/ |
| `az network watcher next-hop` | Confirm UDR / firewall path | builtin |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Azure Virtual Network | SaaS | Yes | Foundation; CRUD via az/bicep/terraform. |
| Azure NSG | SaaS | Yes | API-driven; rule order matters. |
| NAT Gateway | SaaS | Yes | Sizing = number of public IPs × 64k SNAT ports. |
| Application Gateway v2 | SaaS | Yes | WAF v2; subnet delegation required (2025). |
| Azure Front Door Standard/Premium | SaaS | Yes | Premium needed for Private Link + advanced WAF. |
| Private Link / Private Endpoint | SaaS | Yes | Always pair with Private DNS zone. |
| Azure Firewall (Standard/Premium) | SaaS | Yes | TLS inspection in Premium; agents must set up CA cert in KV. |
| Azure DNS / Private DNS Zone | SaaS | Yes | Zone-to-VNet links are the hidden footgun. |
| Network Watcher | SaaS | Yes | Connection Monitor + flow logs (NSG → Storage → Log Analytics). |
| Azure Virtual WAN | SaaS | Yes | Replaces hub-spoke for global mesh; SaaS-managed hub. |

## Templates & scripts
See `templates.md` and `examples.md` for full Bicep/Terraform. Inline diagnostic snippet (≤30 lines) — agents run before apply to verify Private Endpoint resolves privately:

```bash
#!/usr/bin/env bash
# scripts/check_private_endpoint.sh
set -euo pipefail

PE_FQDN="${1:?usage: $0 <fqdn> <vnet> <subnet>}"
VNET="${2}"
SUBNET="${3}"

# 1. Public DNS — should NOT resolve to your private IP.
PUBLIC_IP=$(dig +short "$PE_FQDN" @1.1.1.1 | tail -1)

# 2. Spawn a debug pod / VM in target subnet.
DEBUG_VM=$(az vm create -g rg-net-debug -n debug-$RANDOM \
  --image Ubuntu2204 --size Standard_B1s \
  --vnet-name "$VNET" --subnet "$SUBNET" \
  --admin-username azureuser --generate-ssh-keys --public-ip-address "" \
  --query 'privateIpAddress' -o tsv)

# 3. From inside, resolve and compare.
az vm run-command invoke -g rg-net-debug -n "$DEBUG_VM" \
  --command-id RunShellScript \
  --scripts "getent hosts $PE_FQDN | awk '{print \$1}'" \
  --query 'value[0].message' -o tsv

# 4. Compare: private resolution must NOT equal $PUBLIC_IP.
echo "Public IP from internet: $PUBLIC_IP"
echo "Expect private VNet IP from debug VM (10.x or 172.16.x or 192.168.x)."
```

## Best practices
- CIDR plan with /22 per spoke and /24 per subnet — leave headroom for NAT GW, App Gateway, Bastion, AKS pod CIDR (AKS pods need a lot).
- One Private DNS zone per service, linked to every consumer VNet — automate the link via policy, not click-ops.
- App Gateway WAF starts in **Detection** mode for one week, review logs, only then move to **Prevention**.
- NAT Gateway over Load Balancer outbound rules — LB outbound is per-NIC and runs out of SNAT ports faster.
- Tag every networking resource with `cost-center`, `owner`, `env`, `data-class`. Networking bills are otherwise unallocatable.
- Flow logs on every NSG → Storage → Log Analytics. Without flow logs, an East-West incident is unsolvable.
- Use Azure Policy to enforce: no public IPs in spoke subnets, all PEs have DNS zone, all NSGs have flow logs.
- Test failover: stop one AZ App Gateway / Front Door origin and confirm traffic reroutes within SLA.

## AI-agent gotchas
- LLMs generate NSG rules based on legacy "Allow 80, 443" examples and forget HTTP/3 (UDP/443 / QUIC). For Front Door/AGW frontends, allow UDP/443 too.
- Agents drop `network_security_group_id` reference inside the subnet block in Terraform — works but on plan re-apply NSG associations flap.
- Subscription scope confusion: `az network vnet peering` requires both directions; LLMs create one side, plan looks clean, traffic still fails.
- Private Endpoints in module/Bicep loops without unique `name` collide silently — last-write-wins.
- Agents propose Service Tags (`Storage`, `Sql`) for tight allow-rules then forget those tags are regional; cross-region traffic ignored.
- Front Door rules engine syntax differs from App Gateway URL Path Map — agents copy rules between them and break routing.
- Human-in-loop checkpoint: any change touching public IPs, peerings, or DNS zones goes through human approval — even a 1-rule NSG change that opens 0.0.0.0/0 should block automation.
- App Gateway certificate rotation: agents update Key Vault certificate but forget Managed Identity needs `get`/`list` perms on the new version → Gateway falls back to old cert.
- AKS + Private Cluster gotcha: agents enable Private Cluster, then can't reach the API server from CI; they fix by adding a public endpoint, undoing the security goal.

## References
- Azure VNet docs — https://learn.microsoft.com/azure/virtual-network/
- Azure Application Gateway — https://learn.microsoft.com/azure/application-gateway/
- Azure Front Door — https://learn.microsoft.com/azure/frontdoor/
- Private Link — https://learn.microsoft.com/azure/private-link/
- Azure Well-Architected: Networking — https://learn.microsoft.com/azure/well-architected/service-guides/azure-networking
- Hub-spoke reference architecture — https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/hub-spoke
- Network security best practices — https://learn.microsoft.com/azure/security/fundamentals/network-best-practices
- AzAdvertizer (community) — https://www.azadvertizer.net/
