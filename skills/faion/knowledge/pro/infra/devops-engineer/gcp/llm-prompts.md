# GCP LLM Prompts

Prompts for automating Google Cloud Platform tasks with AI assistants.

---

## GKE Prompts

### Create GKE Cluster

```
Create a GKE cluster with the following requirements:

Project: {PROJECT_ID}
Region: {REGION}
Environment: {production|staging|development}

Requirements:
- Mode: {Autopilot|Standard}
- Private cluster: {yes|no}
- Workload Identity: enabled
- VPC: {VPC_NAME}
- Pod CIDR: {POD_CIDR}
- Service CIDR: {SERVICE_CIDR}

For Standard mode also include:
- Node pool configuration with autoscaling
- Spot node pool for batch workloads
- Appropriate machine types

Output:
1. Terraform configuration
2. gcloud commands as alternative
3. Post-creation verification commands
```

### GKE Cost Optimization Analysis

```
Analyze GKE cluster for cost optimization:

Cluster: {CLUSTER_NAME}
Project: {PROJECT_ID}
Region: {REGION}

Current configuration:
{Paste output of: gcloud container clusters describe CLUSTER}

Node pools:
{Paste output of: gcloud container node-pools list --cluster=CLUSTER}

Analyze and recommend:
1. Node pool right-sizing opportunities
2. Spot/preemptible VM candidates
3. Autoscaling configuration improvements
4. HPA/VPA recommendations
5. Committed Use Discount eligibility
6. Unused resources to remove

Provide:
- Current estimated monthly cost
- Estimated savings per recommendation
- Implementation commands
```

### Migrate to GKE Autopilot

```
Create migration plan from GKE Standard to Autopilot:

Current cluster:
{Paste cluster configuration}

Workloads:
{Paste deployment manifests or describe key workloads}

Provide:
1. Autopilot compatibility assessment
2. Workloads that need modification
3. Migration strategy (in-place or new cluster)
4. Step-by-step migration plan
5. Rollback procedure
6. Testing checklist
```

---

## Cloud Run Prompts

### Deploy Cloud Run Service

```
Create Cloud Run service deployment:

Service name: {SERVICE_NAME}
Project: {PROJECT_ID}
Region: {REGION}

Container:
- Image: {IMAGE_URL}
- Port: {PORT}

Resources:
- CPU: {CPU}
- Memory: {MEMORY}
- Min instances: {MIN}
- Max instances: {MAX}
- Concurrency: {CONCURRENCY}

Configuration:
- Public access: {yes|no}
- VPC connector: {CONNECTOR_NAME or none}
- Environment variables: {KEY=VALUE, ...}
- Secrets: {SECRET_NAME:VERSION, ...}

Output:
1. gcloud deployment command
2. Terraform configuration
3. GitHub Actions workflow for CI/CD
```

### Cloud Run Cost Optimization

```
Optimize Cloud Run service costs:

Service: {SERVICE_NAME}
Project: {PROJECT_ID}
Region: {REGION}

Current metrics (last 30 days):
- Request count: {REQUESTS}
- Average latency: {LATENCY}
- Cold start frequency: {PERCENTAGE}
- Instance hours: {HOURS}
- Current cost: {COST}

Current configuration:
{Paste output of: gcloud run services describe SERVICE}

Analyze and recommend:
1. Min/max instance optimization
2. CPU/memory right-sizing
3. Concurrency tuning
4. CPU allocation strategy (request-based vs always-on)
5. Committed Use Discount eligibility
6. Cold start reduction strategies

Provide implementation commands for each recommendation.
```

### Cloud Run Traffic Management

```
Configure Cloud Run traffic splitting:

Service: {SERVICE_NAME}
Region: {REGION}

Current revision: {CURRENT_REVISION}
New revision: {NEW_REVISION}

Strategy: {canary|blue-green|gradual}

For canary:
- Initial percentage: {PERCENTAGE}
- Increment: {INCREMENT}
- Interval: {INTERVAL}

Provide:
1. Deployment commands
2. Traffic split commands
3. Monitoring commands
4. Rollback commands
5. Automation script for gradual rollout
```

---

## IAM Prompts

### Setup Workload Identity Federation

```
Configure Workload Identity Federation:

Project: {PROJECT_ID}
Source: {GitHub Actions|GitLab CI|AWS|Azure|Other OIDC}

For GitHub Actions:
- Organization: {ORG}
- Repository: {REPO}
- Branch restrictions: {BRANCHES or none}

For AWS:
- Account ID: {ACCOUNT_ID}
- Role ARN: {ROLE_ARN}

Required GCP roles:
{List of roles needed}

Provide:
1. Workload Identity Pool creation
2. Provider configuration
3. Service account setup
4. IAM bindings
5. Client configuration (GitHub Actions workflow, AWS CLI, etc.)
6. Testing commands
```

### IAM Audit and Cleanup

```
Audit IAM permissions for project:

Project: {PROJECT_ID}

Current IAM policy:
{Paste output of: gcloud projects get-iam-policy PROJECT}

Service accounts:
{Paste output of: gcloud iam service-accounts list}

Analyze and identify:
1. Overly permissive bindings (primitive roles)
2. Unused service accounts
3. Service accounts with keys (should use WIF)
4. Members with excessive permissions
5. IAM Recommender suggestions

Provide:
1. Risk assessment for each finding
2. Remediation commands
3. Replacement roles for primitive roles
4. Service account cleanup commands
```

### Create Least Privilege Role

```
Create minimal IAM role for:

Use case: {Describe the specific use case}

Resources needed:
- {Resource type 1}: {operations needed}
- {Resource type 2}: {operations needed}
...

Provide:
1. List of minimum required permissions
2. Custom role definition (YAML)
3. gcloud command to create role
4. Terraform configuration
5. Comparison with existing predefined roles
```

---

## Networking Prompts

### Design VPC Architecture

```
Design VPC architecture for:

Project scope: {Single project|Multi-project with Shared VPC}
Regions: {List of regions}
Environments: {production, staging, development}

Requirements:
- GKE clusters: {yes|no}
- Private connectivity to Google APIs: {yes|no}
- Hybrid connectivity: {Cloud VPN|Interconnect|none}
- On-premises CIDR: {CIDR if applicable}

Provide:
1. VPC design (single vs multiple VPCs)
2. IP address plan (non-overlapping CIDRs)
3. Subnet design per region
4. Secondary ranges for GKE
5. Firewall strategy
6. NAT configuration
7. Terraform configuration
```

### Configure Private Service Connect

```
Configure Private Service Connect for:

VPC: {VPC_NAME}
Region: {REGION}
Services: {Google APIs|Published services|Both}

For Google APIs:
- Endpoints needed: {all-apis|specific services}

For published services:
- Service attachment: {ATTACHMENT_URL}

Provide:
1. IP address reservation
2. PSC endpoint configuration
3. DNS configuration
4. Firewall rules
5. Verification commands
6. Terraform configuration
```

### Troubleshoot Connectivity

```
Troubleshoot network connectivity issue:

Source:
- Type: {GKE pod|Cloud Run|Compute Engine|Cloud Functions}
- Location: {VPC, region, zone}

Destination:
- Type: {Google API|External service|Internal service}
- Address: {URL or IP}

Error message: {Error details}

Current configuration:
- VPC: {VPC details}
- Firewall rules: {Relevant rules}
- Routes: {Relevant routes}
- NAT: {NAT configuration if applicable}

Provide:
1. Diagnostic commands to run
2. Common causes for this issue
3. Step-by-step troubleshooting guide
4. Resolution commands
```

---

## Cost Optimization Prompts

### Project Cost Analysis

```
Analyze GCP project costs:

Project: {PROJECT_ID}
Time period: {Last 30 days|Last 90 days|Custom}

Billing data:
{Paste billing export summary or cost breakdown}

Provide:
1. Top cost drivers breakdown
2. Anomaly detection (unusual spikes)
3. Idle resource identification
4. Right-sizing opportunities
5. Committed Use Discount recommendations
6. Storage optimization opportunities
7. Network cost reduction strategies
8. Estimated monthly savings potential
```

### Implement Cost Controls

```
Implement cost controls for:

Project: {PROJECT_ID}
Budget: {MONTHLY_BUDGET}
Alert thresholds: {50%, 80%, 100%, 120%}

Requirements:
- Email alerts to: {EMAILS}
- Slack notifications: {yes|no, WEBHOOK if yes}
- Automatic actions: {none|stop dev resources|other}

Provide:
1. Budget creation commands
2. Alert policy configuration
3. Notification channel setup
4. Automation for cost control (Cloud Functions)
5. Billing export setup for analysis
6. Dashboard creation (Looker Studio or custom)
```

---

## Security Prompts

### Security Audit

```
Perform security audit for:

Project: {PROJECT_ID}
Scope: {IAM|Networking|Compute|Storage|All}

Provide:
1. Security Command Center findings analysis
2. IAM best practices assessment
3. Network security evaluation
4. Encryption status review
5. Logging and monitoring gaps
6. Compliance checklist (SOC2/HIPAA if applicable)
7. Remediation priority list
8. Implementation commands
```

### Implement Security Best Practices

```
Implement security best practices for:

Project: {PROJECT_ID}
Compliance requirements: {SOC2|HIPAA|PCI-DSS|General}

Current state:
{Describe current security configuration}

Implement:
1. Organization policies
2. VPC Service Controls (if needed)
3. Cloud Armor configuration
4. Audit logging
5. Data encryption (CMEK if required)
6. Secret management
7. Binary Authorization (if using containers)

Provide Terraform configurations and gcloud commands.
```

---

## Migration Prompts

### Migrate to GCP

```
Create migration plan:

Source: {AWS|Azure|On-premises|Other cloud}
Target: GCP

Workloads to migrate:
{Describe applications, databases, storage}

Requirements:
- Downtime tolerance: {Zero|Minimal|Acceptable}
- Timeline: {Phases and deadlines}
- Budget: {Migration budget}

Provide:
1. GCP service mapping from source
2. Network connectivity plan
3. Data migration strategy
4. Application migration approach
5. Testing and validation plan
6. Cutover procedure
7. Rollback plan
```

### Modernize to Serverless

```
Modernize application to serverless:

Current architecture:
{Describe current VM-based or container architecture}

Traffic patterns:
{Describe traffic patterns, peak times, etc.}

Evaluate migration to:
- Cloud Run
- Cloud Functions
- App Engine

Provide:
1. Architecture comparison (current vs serverless)
2. Cost comparison
3. Code changes required
4. Migration steps
5. CI/CD pipeline updates
6. Monitoring and alerting changes
```

---

## Disaster Recovery Prompts

### Design DR Strategy

```
Design disaster recovery strategy:

Application: {APPLICATION_NAME}
RTO: {Recovery Time Objective}
RPO: {Recovery Point Objective}

Current architecture:
{Describe current architecture}

Primary region: {REGION}
DR region: {DR_REGION}

Provide:
1. DR architecture design
2. Data replication strategy
3. Failover procedure
4. Failback procedure
5. Testing plan
6. Automation scripts
7. Cost estimate for DR infrastructure
```

### Test DR Procedure

```
Create DR test plan:

Application: {APPLICATION_NAME}
DR configuration:
{Describe current DR setup}

Test scope: {Full failover|Partial|Data recovery only}

Provide:
1. Pre-test checklist
2. Step-by-step test procedure
3. Validation criteria
4. Rollback steps
5. Post-test documentation template
6. Improvement recommendations based on common issues
```

---

## Monitoring Prompts

### Setup Monitoring Stack

```
Configure monitoring for:

Project: {PROJECT_ID}
Services: {GKE|Cloud Run|Compute Engine|Cloud SQL|etc.}

Requirements:
- Metrics to track: {List key metrics}
- Alert channels: {Email|Slack|PagerDuty}
- Dashboard requirements: {Describe}

Provide:
1. Cloud Monitoring configuration
2. Alert policies
3. Notification channels
4. Custom dashboards
5. Log-based metrics
6. SLO configuration (if applicable)
7. Terraform configurations
```

### Create SLO/SLI

```
Define SLOs for:

Service: {SERVICE_NAME}
Type: {API|Web application|Background job}

User expectations:
- Availability: {e.g., 99.9%}
- Latency: {e.g., p95 < 200ms}
- Error rate: {e.g., < 0.1%}

Provide:
1. SLI definitions
2. SLO targets
3. Error budget calculation
4. Cloud Monitoring SLO configuration
5. Alert policies for error budget burn
6. Dashboard for SLO tracking
```

---

*GCP LLM Prompts v2.0 | Updated: 2026-01*
