# Azure Networking LLM Prompts

## VNet Design Prompts

### Design Hub-Spoke Network

```
Design an Azure hub-spoke network architecture for the following requirements:

Project: {project_name}
Environments: {dev, staging, prod}
Workloads: {AKS, App Service, PostgreSQL, Redis, Storage}
Connectivity: {VPN to on-premises / ExpressRoute / Internet only}
Compliance: {HIPAA, SOC2, PCI-DSS, none}

Requirements:
- Address space planning with no overlaps
- Subnet sizing for each tier
- NSG rules following least privilege
- Private endpoints for all PaaS services
- NAT Gateway for outbound connectivity
- Azure Bastion for secure access

Output:
1. Network diagram (text-based)
2. IP address allocation table
3. Terraform code for VNet and subnets
4. NSG rules matrix
```

### Subnet Sizing Calculator

```
Calculate subnet sizes for Azure VNet with these requirements:

Services:
- AKS cluster: {node_count} nodes, {pods_per_node} pods per node
- Application Gateway: {instance_count} instances
- Azure Bastion: 1 instance
- Private Endpoints: {pe_count} endpoints
- VMs: {vm_count} virtual machines

Constraints:
- Reserve 5 IPs per subnet (Azure reserved)
- Allow 50% growth headroom
- Keep subnet boundaries on /24, /25, /26, /27

Output:
1. Recommended CIDR blocks for each subnet
2. IP count breakdown
3. VNet total address space
```

## NSG Configuration Prompts

### Generate NSG Rules

```
Generate NSG rules for a {tier_type} subnet in Azure with these requirements:

Tier: {web / app / data / management}
Traffic Sources:
- {source_1}: {protocol}:{port}
- {source_2}: {protocol}:{port}

Security Requirements:
- Follow Azure NSG best practices
- Use service tags where applicable
- Include explicit deny-all rule
- Document each rule purpose

Output:
1. Terraform azurerm_network_security_group resource
2. Rule priority assignments
3. Justification for each rule
```

### NSG Rule Audit

```
Audit the following NSG rules for security issues:

{paste NSG rules here}

Check for:
- Overly permissive rules (0.0.0.0/0, any/any)
- Missing deny-all rules
- Rules allowing management ports from internet
- Redundant or conflicting rules
- Missing service tags (using IPs instead)

Output:
1. Risk assessment for each rule
2. Recommended fixes
3. Updated Terraform code
```

## Application Gateway Prompts

### Configure Application Gateway

```
Configure Azure Application Gateway v2 for:

Application: {app_name}
Backend: {AKS / App Service / VMs}
SSL: {managed certificate / Key Vault certificate}
WAF: {enabled / disabled}
Scaling: {min_instances} to {max_instances}

Requirements:
- HTTPS listener with TLS 1.2+
- Health probes for backend
- URL path-based routing: {yes / no}
- Rewrite rules: {header rewrites needed}
- Connection draining enabled

Output:
1. Terraform code for Application Gateway
2. WAF policy configuration
3. Backend pool configuration
4. Listener and routing rules
```

### WAF Rule Tuning

```
Tune WAF rules for Application Gateway protecting a {app_type} application.

Current issues:
- False positives on: {describe blocked requests}
- Specific paths need exclusion: {paths}
- Custom rules needed for: {requirements}

Application characteristics:
- API endpoints: {yes / no}
- File uploads: {yes / no}
- Rich text input: {yes / no}

Output:
1. Rule exclusions configuration
2. Custom WAF rules
3. Updated WAF policy Terraform code
4. Monitoring queries for WAF logs
```

## Front Door Prompts

### Configure Front Door Premium

```
Configure Azure Front Door Premium for global load balancing:

Origins:
- Region 1: {region_1} - {origin_type}
- Region 2: {region_2} - {origin_type}

Requirements:
- Private Link to origins
- Global WAF policy
- Caching: {caching_rules}
- Custom domain: {domain}

Output:
1. Terraform code for Front Door Premium
2. Origin group configuration
3. WAF policy with managed rules
4. Caching rules configuration
5. Custom domain and certificate setup
```

### Front Door + App Gateway Integration

```
Design Front Door + Application Gateway architecture for:

Use case: {global distribution / DR / both}
Regions: {region_list}
WAF strategy: {Front Door only / both layers}

Architecture requirements:
- Lock App Gateway to Front Door traffic only
- End-to-end TLS
- Health probes at both layers
- Failover strategy

Output:
1. Architecture diagram
2. Front Door configuration
3. App Gateway configuration
4. NSG rules to restrict traffic
5. Health probe configuration
```

## Private Link Prompts

### Configure Private Endpoints

```
Configure Private Endpoints for the following Azure PaaS services:

Services:
- Storage Account (blob, file): {storage_name}
- Key Vault: {keyvault_name}
- PostgreSQL Flexible Server: {postgres_name}
- Container Registry: {acr_name}

VNet: {vnet_name}
Subnet for endpoints: {subnet_name}

Requirements:
- Private DNS zones with VNet links
- Disable public access on all services
- Test connectivity from VNet

Output:
1. Terraform code for private endpoints
2. Private DNS zone configuration
3. VNet link configuration
4. Validation commands
```

### Private Link Service Setup

```
Configure Private Link Service to expose an internal application:

Application: {app_description}
Load Balancer: {internal_lb_name}
Frontend IP: {frontend_ip}

Requirements:
- Allow connections from specific subscriptions: {subscription_ids}
- Auto-approve connections: {yes / no}
- NAT IP configuration

Output:
1. Terraform code for Private Link Service
2. Consumer private endpoint configuration
3. Connection approval workflow
4. DNS configuration for consumers
```

## Monitoring and Diagnostics Prompts

### Network Monitoring Setup

```
Set up comprehensive monitoring for Azure networking:

Resources to monitor:
- VNet: {vnet_name}
- NSG: {nsg_names}
- Application Gateway: {appgw_name}
- Front Door: {fd_name}

Requirements:
- NSG flow logs with Traffic Analytics
- Application Gateway access and WAF logs
- Front Door access and WAF logs
- Metric alerts for:
  - Unhealthy backend instances
  - High latency
  - Failed requests
  - SNAT port exhaustion

Output:
1. Terraform for diagnostic settings
2. Log Analytics workspace queries
3. Alert rules configuration
4. Grafana dashboard JSON
```

### Troubleshooting Network Issues

```
Help troubleshoot the following Azure networking issue:

Symptom: {describe the issue}
Resources involved: {list resources}
Error messages: {paste errors}
Recent changes: {describe changes}

Diagnostic information needed:
- NSG flow logs query
- Effective security rules
- Route table configuration
- DNS resolution test
- Network Watcher tools to use

Output:
1. Step-by-step troubleshooting guide
2. Kusto queries for logs
3. Azure CLI commands for diagnostics
4. Potential root causes
5. Resolution steps
```

## Migration and Optimization Prompts

### Migrate to Private Endpoints

```
Plan migration from service endpoints to private endpoints:

Current state:
- Services using service endpoints: {service_list}
- VNets: {vnet_list}
- Applications: {app_list}

Migration requirements:
- Zero downtime
- Rollback plan
- DNS transition strategy
- Testing checklist

Output:
1. Migration plan with phases
2. Terraform code for private endpoints
3. DNS transition steps
4. Testing and validation steps
5. Rollback procedure
```

### Cost Optimization Review

```
Review Azure networking costs and suggest optimizations:

Current resources:
- VPN Gateways: {count} x {sku}
- NAT Gateways: {count}
- Public IPs: {count}
- Application Gateways: {count} x {sku}
- Front Door: {tier}
- Data transfer: {monthly_gb} GB

Usage patterns:
- Peak hours: {hours}
- Traffic distribution: {intra-region}% / {inter-region}% / {internet}%

Output:
1. Cost breakdown analysis
2. Optimization recommendations
3. Right-sizing suggestions
4. Reserved capacity opportunities
5. Estimated savings
```

## Compliance and Security Prompts

### Security Assessment

```
Perform security assessment of Azure network configuration:

Resources:
{paste Terraform code or resource list}

Compliance framework: {HIPAA / SOC2 / PCI-DSS / CIS Benchmark}

Check for:
- Network segmentation adequacy
- NSG rule compliance
- Encryption in transit
- Private endpoint usage
- Logging and monitoring
- DDoS protection

Output:
1. Security findings with severity
2. Compliance gaps
3. Remediation recommendations
4. Updated Terraform code
5. Security monitoring queries
```

### Zero Trust Implementation

```
Implement Zero Trust network architecture in Azure:

Current state:
- VNet topology: {hub-spoke / flat}
- Workloads: {workload_list}
- Identity: {Entra ID / hybrid}

Zero Trust requirements:
- Verify explicitly
- Use least privilege access
- Assume breach

Output:
1. Zero Trust architecture design
2. Network segmentation strategy
3. NSG rules implementation
4. Azure Firewall policy (if applicable)
5. Identity-based access controls
6. Monitoring and threat detection setup
```

---

*Azure Networking LLM Prompts | faion-cicd-engineer*
