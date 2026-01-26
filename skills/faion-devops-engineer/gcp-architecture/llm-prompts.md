# GCP Architecture LLM Prompts

Prompts for automating GCP architecture design and implementation tasks with AI assistants.

---

## Landing Zone Design Prompts

### Design Landing Zone

```
Design a GCP landing zone for:

Organization: {ORGANIZATION_NAME}
Industry: {INDUSTRY}
Compliance requirements: {SOC2|HIPAA|PCI-DSS|GDPR|None}

Current state:
- Existing cloud: {None|AWS|Azure|Other GCP}
- Number of teams: {NUMBER}
- Expected workloads: {Describe workloads}

Requirements:
- Environments: {production, staging, development, ...}
- Multi-region: {yes|no, list regions if yes}
- Hybrid connectivity: {none|VPN|Interconnect}
- On-premises CIDR: {CIDR if applicable}

Provide:
1. Organization hierarchy (folders, projects)
2. IAM strategy (groups, roles)
3. Network architecture (VPC pattern, IP planning)
4. Security controls (org policies, logging)
5. Diagram of the architecture
6. Implementation priority order
7. Terraform module structure
```

### Resource Hierarchy Design

```
Design GCP resource hierarchy for:

Organization ID: {ORG_ID}
Number of business units: {NUMBER}
Environments per unit: {LIST}
Shared services needed: {networking, monitoring, security, CI/CD}

Constraints:
- Budget isolation: {by team|by environment|both}
- Network isolation: {strict|moderate|minimal}
- Admin delegation: {centralized|federated}

Provide:
1. Folder structure diagram
2. Project naming convention
3. IAM role assignments per level
4. Billing account structure
5. Terraform code for hierarchy
```

### IP Address Planning

```
Create IP address plan for:

Environments: {LIST}
Regions: {LIST}
GKE clusters: {NUMBER per environment}
Cloud SQL instances: {NUMBER per environment}
Other services: {LIST}

Constraints:
- On-premises CIDR (avoid): {CIDR}
- Other cloud CIDRs (avoid): {LIST}
- Future growth: {percentage}

Requirements:
- Pod CIDR per cluster
- Service CIDR per cluster
- Private service access range
- VPN/Interconnect considerations

Provide:
1. Complete IP allocation table
2. Subnet design per region
3. Secondary ranges for GKE
4. Validation of no overlaps
5. Future expansion recommendations
```

---

## Architecture Review Prompts

### Well-Architected Review

```
Perform Google Cloud Well-Architected review:

Project: {PROJECT_ID}
Architecture description:
{Describe current architecture}

Current configuration:
{Paste relevant config or describe}

Review against all five pillars:
1. Operational Excellence
2. Security, Privacy, Compliance
3. Reliability
4. Cost Optimization
5. Performance Optimization

For each pillar provide:
- Current state assessment
- Gaps identified
- Recommendations with priority
- Implementation effort (Low/Medium/High)
- Terraform/gcloud commands for fixes
```

### Security Architecture Review

```
Review GCP security architecture:

Project: {PROJECT_ID}
Compliance requirements: {LIST}

Current IAM policy:
{Paste output of: gcloud projects get-iam-policy PROJECT}

Service accounts:
{Paste output of: gcloud iam service-accounts list}

Network configuration:
{Describe VPC, firewall rules, etc.}

Analyze and provide:
1. IAM security issues
   - Overly permissive roles
   - Service account key usage
   - Missing least privilege
2. Network security gaps
   - Firewall rule issues
   - Missing network controls
   - Public exposure risks
3. Data security concerns
   - Encryption status
   - Access controls
4. Compliance gaps
5. Remediation commands for each issue
```

### Cost Architecture Review

```
Review GCP architecture for cost optimization:

Project: {PROJECT_ID}
Monthly spend: {AMOUNT}

Current resources:
{List or describe current infrastructure}

Billing breakdown:
{Paste top cost drivers}

Analyze and recommend:
1. Resource right-sizing opportunities
2. Reserved/committed use candidates
3. Spot VM opportunities
4. Idle resource identification
5. Storage optimization
6. Network cost reduction
7. Architecture changes for cost savings

For each recommendation provide:
- Current cost
- Estimated savings
- Implementation complexity
- Risk assessment
- Implementation commands
```

---

## GKE Architecture Prompts

### Design GKE Architecture

```
Design GKE architecture for:

Application: {DESCRIPTION}
Traffic: {REQUESTS/second, USERS}
Environment: {production|staging|development}

Requirements:
- Availability: {99.9%|99.95%|99.99%}
- Latency: {p50, p95, p99}
- Region(s): {LIST}
- Compliance: {LIST}

Workload characteristics:
- Stateless services: {NUMBER}
- Stateful services: {NUMBER}
- Batch jobs: {yes|no}
- ML/GPU workloads: {yes|no}

Provide:
1. Cluster mode recommendation (Autopilot vs Standard)
2. Cluster topology (zonal vs regional vs multi-cluster)
3. Node pool strategy
4. Networking design (ingress, service mesh)
5. Security configuration
6. Scaling strategy (HPA, VPA, cluster autoscaler)
7. Terraform configuration
```

### GKE Migration Assessment

```
Assess migration to GKE:

Current platform: {Kubernetes|VMs|Containers|Other}
Current configuration:
{Describe current infrastructure}

Workloads:
{List services with resource requirements}

Questions to answer:
1. GKE mode recommendation (Autopilot vs Standard)
2. Migration strategy (lift-and-shift vs refactor)
3. Workload compatibility issues
4. Resource mapping (current to GKE)
5. Network changes required
6. Security adjustments
7. Cost comparison
8. Migration steps
9. Rollback plan
```

### Multi-Cluster Strategy

```
Design GKE multi-cluster strategy:

Use case: {DR|Multi-region|Multi-tenant|Traffic distribution}
Regions: {LIST}
Traffic split: {PERCENTAGE per region}

Requirements:
- Failover time: {RTO}
- Data consistency: {requirements}
- Cost constraints: {BUDGET}

Provide:
1. Cluster topology
2. Service mesh configuration (if applicable)
3. Multi-cluster ingress setup
4. Data replication strategy
5. Failover procedure
6. Traffic management
7. Cost estimate
8. Terraform configuration
```

---

## Database Architecture Prompts

### Cloud SQL Architecture

```
Design Cloud SQL architecture:

Database type: {PostgreSQL|MySQL|SQL Server}
Application: {DESCRIPTION}
Environment: {production|staging|development}

Requirements:
- Size: {DATA_SIZE}
- Connections: {MAX_CONNECTIONS}
- Read/write ratio: {RATIO}
- Availability: {SLA}
- RPO/RTO: {VALUES}

Provide:
1. Instance tier recommendation
2. Storage configuration
3. HA configuration
4. Read replica strategy
5. Backup configuration
6. Security setup (private IP, SSL)
7. Monitoring setup
8. Cost estimate
9. Terraform configuration
```

### Database Migration

```
Plan Cloud SQL migration:

Source: {Database type, version, size}
Target: Cloud SQL {PostgreSQL|MySQL}
Data size: {SIZE}
Downtime tolerance: {HOURS|ZERO}

Current environment:
{Describe source database setup}

Provide:
1. Migration method (DMS, pgloader, native tools)
2. Pre-migration checklist
3. Schema migration steps
4. Data migration procedure
5. Cutover procedure
6. Validation steps
7. Rollback plan
8. Timeline estimate
```

---

## Network Architecture Prompts

### VPC Design

```
Design VPC architecture:

Scope: {Single project|Multi-project|Organization-wide}
Environments: {LIST}
Regions: {LIST}

Requirements:
- Shared VPC: {yes|no}
- Hybrid connectivity: {none|VPN|Interconnect}
- Private Google Access: {yes|no}
- Service endpoints: {LIST}

Constraints:
- Existing CIDRs to avoid: {LIST}
- Security requirements: {DESCRIBE}

Provide:
1. VPC design (single vs multiple)
2. Subnet layout per region
3. IP address plan
4. Firewall strategy
5. NAT configuration
6. DNS setup
7. Private connectivity (PSC, Private Access)
8. Terraform configuration
```

### Hybrid Connectivity

```
Design hybrid connectivity:

On-premises environment:
- Location: {LOCATION}
- Bandwidth: {CURRENT_BANDWIDTH}
- Latency requirement: {MS}
- Redundancy: {REQUIRED_LEVEL}

GCP environment:
- Region: {REGION}
- Services to access: {LIST}
- Traffic volume: {GB/month}

Options to evaluate:
- Cloud VPN
- Partner Interconnect
- Dedicated Interconnect

Provide:
1. Connectivity recommendation
2. Redundancy design
3. IP routing configuration
4. Firewall rules
5. DNS resolution strategy
6. Cost comparison
7. Implementation steps
8. Terraform configuration
```

### Load Balancing Architecture

```
Design load balancing architecture:

Application type: {Web|API|gRPC|WebSocket}
Traffic pattern: {GLOBAL|REGIONAL}
Protocol: {HTTP(S)|TCP|UDP}

Requirements:
- SSL termination: {yes|no}
- CDN: {yes|no}
- WAF/DDoS protection: {yes|no}
- Health check requirements: {DESCRIBE}

Backend type: {GKE|Cloud Run|VMs|Hybrid}

Provide:
1. Load balancer type recommendation
2. Backend configuration
3. Health check setup
4. SSL certificate management
5. CDN configuration (if applicable)
6. Cloud Armor policies (if applicable)
7. URL map design
8. Terraform configuration
```

---

## Disaster Recovery Prompts

### DR Architecture Design

```
Design DR architecture:

Application: {NAME}
Criticality: {Critical|High|Medium|Low}

Requirements:
- RTO: {HOURS}
- RPO: {MINUTES|HOURS}
- Budget: {MONTHLY_DR_BUDGET}

Primary region: {REGION}
DR region: {REGION}

Components:
- Compute: {GKE|Cloud Run|VMs}
- Database: {Cloud SQL|Spanner|Firestore}
- Storage: {GCS|Filestore}
- Other: {LIST}

Provide:
1. DR strategy (cold|warm|hot standby)
2. Data replication design
3. Failover procedure
4. Failback procedure
5. Testing strategy
6. Automation scripts
7. Cost estimate
8. Terraform configuration
```

### DR Testing Plan

```
Create DR test plan:

DR architecture:
{Describe current DR setup}

Test scope: {Full failover|Partial|Data recovery only}
Test window: {DATE/TIME}
Participants: {TEAMS}

Provide:
1. Pre-test checklist
2. Communication plan
3. Step-by-step test procedure
4. Validation criteria
5. Rollback steps if needed
6. Post-test documentation template
7. Success/failure criteria
8. Lessons learned template
```

---

## Migration Prompts

### Cloud Migration Assessment

```
Assess migration to GCP:

Source environment:
- Current cloud/platform: {DESCRIBE}
- Applications: {LIST with descriptions}
- Data stores: {LIST}
- Dependencies: {DESCRIBE}

Requirements:
- Timeline: {MONTHS}
- Budget: {AMOUNT}
- Downtime tolerance: {DESCRIBE}
- Compliance: {REQUIREMENTS}

Provide:
1. Application assessment (6R analysis)
2. GCP service mapping
3. Migration waves
4. Network connectivity plan
5. Data migration strategy
6. Testing strategy
7. Cutover procedures
8. Risk assessment
9. Cost comparison (current vs GCP)
```

### Modernization Assessment

```
Assess application modernization:

Current architecture:
{Describe current application}

Pain points:
{List current issues}

Goals:
- Cost reduction: {TARGET}
- Scalability: {REQUIREMENTS}
- Developer productivity: {GOALS}

Evaluate options:
- Containerization (GKE)
- Serverless (Cloud Run, Cloud Functions)
- Managed services

Provide:
1. Current vs target architecture comparison
2. Modernization path recommendation
3. Code changes required
4. Infrastructure changes
5. CI/CD updates
6. Team skill gaps
7. Timeline estimate
8. Cost analysis
```

---

## Monitoring and Operations Prompts

### Observability Design

```
Design observability stack:

Environment: {PROJECT_ID}
Services: {LIST}

Requirements:
- Metrics: {CUSTOM_METRICS}
- Logs: {RETENTION_DAYS}
- Traces: {yes|no}
- Alerting: {CHANNELS}

SLOs to track:
- {SERVICE}: {SLO_DEFINITION}
- {SERVICE}: {SLO_DEFINITION}

Provide:
1. Cloud Monitoring configuration
2. Custom metrics design
3. Log-based metrics
4. Alert policies
5. Dashboard design
6. SLO configuration
7. Notification channels
8. Terraform configuration
```

### Incident Response Setup

```
Design incident response for:

Services: {LIST}
Criticality: {LEVELS}
On-call team: {SIZE}

Requirements:
- Alert routing: {DESCRIBE}
- Escalation: {LEVELS}
- Communication: {CHANNELS}

Provide:
1. Alerting policy design
2. Severity classification
3. Escalation procedures
4. Runbook templates
5. Communication templates
6. Post-incident review process
7. PagerDuty/Opsgenie integration (if applicable)
8. Automation opportunities
```

---

## Cost Optimization Prompts

### FinOps Implementation

```
Implement FinOps practices:

Organization: {ORG_ID}
Current monthly spend: {AMOUNT}
Optimization target: {PERCENTAGE}

Current state:
- Cost visibility: {DESCRIBE}
- Budget controls: {DESCRIBE}
- Optimization practices: {DESCRIBE}

Provide:
1. Billing export setup (BigQuery)
2. Cost allocation strategy (labels)
3. Budget configuration per project/team
4. Recommender setup
5. Custom cost dashboards
6. Cost anomaly detection
7. Chargeback/showback model
8. Optimization automation
```

### Committed Use Analysis

```
Analyze committed use discounts:

Project(s): {LIST}
Time period: {MONTHS to analyze}

Current usage:
{Paste billing data or describe}

Analyze:
1. Steady-state vs variable workloads
2. CUD candidates by service
3. 1-year vs 3-year recommendation
4. Spend-based vs resource-based
5. Flexible vs standard CUDs
6. ROI calculation
7. Risk assessment
8. Purchase recommendation
```

---

*GCP Architecture LLM Prompts v2.0 | Updated: 2026-01*
