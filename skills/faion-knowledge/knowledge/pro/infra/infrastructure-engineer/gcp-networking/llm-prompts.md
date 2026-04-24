# GCP Networking LLM Prompts

## VPC Design Prompts

### Prompt 1: VPC Architecture Design

```
Design a GCP VPC architecture for the following requirements:

Application: [describe application]
Regions: [list regions]
Environments: [prod/staging/dev]
Workloads: [VMs/GKE/Cloud Run/etc.]
Connectivity: [on-prem/other clouds/internet only]
Compliance: [HIPAA/PCI/SOC2/none]

Please provide:
1. VPC topology (single vs multiple VPCs, Shared VPC consideration)
2. Subnet design with CIDR ranges
3. Secondary ranges for GKE if applicable
4. Firewall strategy
5. NAT configuration
6. Private connectivity options
7. Terraform module structure

Consider GCP best practices:
- Custom mode VPCs (not auto)
- Global VPC with regional subnets
- Private Google Access enabled
- VPC Flow Logs for visibility
- Service account-based firewall filtering
```

### Prompt 2: Subnet CIDR Planning

```
Plan IP address ranges for a GCP VPC with the following requirements:

VPC peering targets: [list CIDRs that must not overlap]
Regions: [list regions]
Per-region resources:
- VMs: [estimated count]
- GKE nodes: [estimated count]
- GKE pods: [estimated count]
- GKE services: [estimated count]

Growth factor: [2x/3x/5x]

Provide:
1. Primary subnet ranges per region
2. Secondary ranges for GKE pods and services
3. Reserved ranges for future expansion
4. Documentation table showing all allocations
5. Validation that ranges don't overlap with peering targets

Use RFC 1918 ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).
Ensure pods get /14 or larger for GKE autopilot.
```

### Prompt 3: Multi-Environment VPC Strategy

```
Design a multi-environment networking strategy for GCP:

Environments: production, staging, development
Teams: [list teams that need access]
Shared services: [CI/CD, monitoring, DNS, etc.]
Isolation requirements: [describe]

Options to evaluate:
1. Single VPC with subnet-based isolation
2. Separate VPCs with peering
3. Shared VPC architecture
4. Combination approach

For each viable option, provide:
- Architecture diagram (text-based)
- Pros and cons
- Cost implications
- Management complexity
- Security considerations
- Recommendation with justification
```

---

## Firewall Prompts

### Prompt 4: Firewall Rules Design

```
Design firewall rules for a GCP VPC with these workloads:

Workloads:
- Web servers: ports [list], public access [yes/no]
- API servers: ports [list], sources [list]
- Databases: ports [list], internal only
- GKE cluster: [describe connectivity needs]

Requirements:
- IAP access for SSH administration
- Health check support for load balancers
- Internal communication between workloads
- Default deny with logging

Provide:
1. Complete firewall rule set with:
   - Name, priority, direction
   - Source/target (prefer service accounts)
   - Ports and protocols
   - Logging configuration
2. gcloud commands to create rules
3. Terraform code
4. Verification steps
```

### Prompt 5: Firewall Audit

```
Audit the following GCP firewall rules for security issues:

[paste firewall rules list or gcloud output]

Check for:
1. Overly permissive rules (0.0.0.0/0 sources)
2. Unused rules (no traffic in logs)
3. Rules without logging
4. Network tags vs service accounts
5. Missing default deny rule
6. Deprecated or legacy patterns
7. Priority conflicts
8. Compliance violations

Provide:
- Risk assessment for each finding
- Remediation steps
- Recommended firewall policy
- gcloud commands to fix issues
```

### Prompt 6: Hierarchical Firewall Policies

```
Design a hierarchical firewall policy for this GCP organization:

Organization structure:
- org-id: [ID]
- Folders: [list folders]
- Projects: [list projects per folder]

Security requirements:
- Block known malicious IPs org-wide
- Allow GCP health checks org-wide
- Environment-specific rules (prod more restrictive)
- Project-level exceptions for specific apps

Provide:
1. Organization-level policy
2. Folder-level policies
3. Project-level rules
4. Delegation model (who manages what)
5. Terraform code
6. Testing approach
```

---

## Cloud NAT Prompts

### Prompt 7: Cloud NAT Configuration

```
Configure Cloud NAT for the following scenario:

VPC: [name]
Regions: [list]
Private instances: [count per region]
Outbound traffic:
- Expected connections per VM: [number]
- Destinations: [internet/specific IPs]
- Protocol mix: [TCP/UDP percentages]

Requirements:
- [Static IPs for allowlisting / auto-allocated IPs]
- Port allocation strategy
- Logging requirements
- Cost optimization

Provide:
1. Cloud Router configuration
2. Cloud NAT configuration with optimal settings
3. Port allocation calculation
4. Monitoring and alerting setup
5. gcloud commands
6. Terraform code
7. Cost estimate
```

### Prompt 8: NAT Port Exhaustion Troubleshooting

```
Troubleshoot Cloud NAT port exhaustion with these symptoms:

Current configuration:
- NAT name: [name]
- Region: [region]
- Min ports per VM: [current]
- Max ports per VM: [current]
- Number of VMs: [count]

Symptoms:
- [describe errors/logs]
- Connection timeouts to: [destinations]
- Time of day pattern: [if any]

Provide:
1. Diagnostic commands to run
2. Root cause analysis approach
3. Recommended configuration changes
4. gcloud commands to apply fixes
5. Monitoring dashboard queries
6. Long-term scaling recommendations
```

---

## Load Balancing Prompts

### Prompt 9: Load Balancer Selection

```
Recommend the appropriate GCP load balancer for:

Application type: [web app/API/gRPC/TCP service/UDP]
Traffic source: [global users/regional/internal]
Backend type: [VMs/GKE/Cloud Run/Cloud Functions]
Protocol: [HTTP/HTTPS/TCP/UDP]
SSL termination: [at LB/at backend/both]
Session affinity: [required/not required]
WebSocket support: [yes/no]
Health check type: [HTTP/HTTPS/TCP/gRPC]

Additional requirements:
- [list any special requirements]

Provide:
1. Recommended load balancer type with justification
2. Alternative options and when to use them
3. Architecture diagram
4. Component list (forwarding rule, proxy, backend service, etc.)
5. gcloud commands to create
6. Terraform code
7. Estimated cost
```

### Prompt 10: Global HTTPS Load Balancer Setup

```
Set up a global HTTPS load balancer with these specifications:

Domains: [list domains]
SSL: [managed certificate/bring your own]
Backend regions: [list]
Backend type: [MIGs/NEGs/serverless]

Routing requirements:
- /api/* -> API backend
- /static/* -> CDN-enabled backend
- /* -> Web backend

Security requirements:
- Cloud Armor: [yes/no]
- Rate limiting: [requests per minute]
- WAF rules: [OWASP/custom]

Provide:
1. Complete architecture
2. Health check configuration
3. Backend service configuration
4. URL map with path matchers
5. SSL certificate setup
6. Cloud Armor policy
7. gcloud commands (in order)
8. Terraform code
9. DNS configuration steps
10. Verification checklist
```

### Prompt 11: Internal Load Balancer for Microservices

```
Design internal load balancing for microservices:

Services:
[list service name, port, protocol, replicas]

Requirements:
- Service discovery method: [DNS/service mesh/direct]
- Health check: [per service requirements]
- Session affinity: [per service]
- Failover: [regional/zonal]

VPC: [name]
Regions: [list]
GKE: [yes/no, if yes describe setup]

Provide:
1. Load balancer type for each service
2. Network endpoint groups configuration
3. Health check per service
4. Backend service configuration
5. Forwarding rules
6. DNS setup for service discovery
7. Terraform code
8. Testing approach
```

---

## Security Prompts

### Prompt 12: VPC Service Controls

```
Implement VPC Service Controls for sensitive data:

Sensitive projects: [list]
Services to protect: [BigQuery/Cloud Storage/etc.]
Allowed access:
- Users: [list]
- Service accounts: [list]
- IP ranges: [list]
- VPCs: [list]

Ingress requirements: [describe]
Egress requirements: [describe]

Provide:
1. Access level definitions
2. Service perimeter configuration
3. Ingress/egress policies
4. Dry-run configuration for testing
5. gcloud commands
6. Terraform code
7. Testing procedure
8. Monitoring setup for violations
```

### Prompt 13: Private Connectivity Design

```
Design private connectivity for:

Scenario: [choose one]
a) Private access to Google APIs only
b) Hybrid connectivity to on-premises
c) Multi-cloud connectivity
d) All of the above

Current state:
- VPC: [name and CIDR]
- On-prem network: [CIDR if applicable]
- Other cloud: [provider and CIDR if applicable]

Requirements:
- Bandwidth: [Gbps]
- Latency: [ms requirements]
- Redundancy: [HA requirements]
- Budget: [if relevant]

Provide:
1. Recommended connectivity options
2. Private Google Access configuration
3. Private Service Connect setup
4. VPN or Interconnect design (if applicable)
5. Routing configuration
6. DNS setup for private zones
7. Architecture diagram
8. Implementation steps
9. Cost estimate
```

---

## Monitoring and Troubleshooting Prompts

### Prompt 14: Network Monitoring Setup

```
Set up comprehensive network monitoring for GCP VPC:

VPC: [name]
Critical workloads: [list]
Compliance requirements: [list]

Monitor for:
- Firewall denies
- NAT port exhaustion
- Load balancer errors
- Latency issues
- Traffic anomalies

Provide:
1. VPC Flow Logs configuration
2. Firewall rules logging
3. Cloud Monitoring dashboard definition
4. Alert policies with thresholds
5. Log-based metrics
6. BigQuery export for long-term analysis
7. Terraform code for monitoring resources
8. Sample queries for common issues
```

### Prompt 15: Network Troubleshooting

```
Troubleshoot this GCP networking issue:

Symptom: [describe]
Source: [VM/GKE pod/Cloud Run/external]
Destination: [VM/service/internet/Google API]
Error message: [if any]
When it started: [time/change that preceded]

Environment:
- VPC: [name]
- Firewall rules: [relevant rules]
- Routes: [custom routes if any]
- NAT: [yes/no, config if yes]
- Load balancer: [yes/no, type if yes]

Provide:
1. Diagnostic steps in order
2. gcloud commands to gather information
3. Connectivity test commands
4. Log queries to run
5. Most likely causes ranked by probability
6. Resolution steps for each cause
7. Prevention recommendations
```

---

## Migration Prompts

### Prompt 16: VPC Migration Planning

```
Plan VPC migration/restructuring:

Current state:
- VPC: [describe current setup]
- Workloads: [what's running]
- Issues: [why migrating]

Target state:
- New VPC design: [describe]
- Goals: [list]

Constraints:
- Downtime tolerance: [minutes/hours/zero]
- Change windows: [when]
- Dependencies: [list]

Provide:
1. Migration strategy options
2. Recommended approach with justification
3. Detailed migration steps
4. Rollback plan
5. Testing checklist
6. Communication plan
7. Timeline with milestones
8. Risk assessment
```

---

## Usage Tips

1. **Be specific**: Include actual values, not placeholders
2. **Provide context**: Current state helps generate accurate solutions
3. **State constraints**: Budget, compliance, existing infrastructure
4. **Request format**: Specify if you need gcloud, Terraform, or both
5. **Follow up**: Ask for clarification or alternatives

---

*GCP Networking LLM Prompts | faion-infrastructure-engineer*
