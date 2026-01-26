# GCP Architecture Patterns LLM Prompts

## Architecture Design Prompts

### GKE Cluster Design

```
Design a production GKE cluster for [APPLICATION_TYPE] with the following requirements:
- Expected workload: [WORKLOAD_DESCRIPTION]
- Traffic pattern: [STEADY/BURSTY/BATCH]
- Compliance requirements: [SOC2/HIPAA/PCI-DSS/NONE]
- Budget constraints: [HIGH/MEDIUM/LOW]

Include:
1. Cluster configuration (regional, release channel, networking mode)
2. Node pool strategy (general, spot, GPU if needed)
3. Security configuration (Workload Identity, Binary Authorization)
4. Monitoring and logging setup
5. Cost optimization recommendations

Output as Terraform HCL with comments explaining each decision.
```

### Cloud SQL Design

```
Design a Cloud SQL PostgreSQL setup for:
- Application type: [WEB_APP/ANALYTICS/MULTI_TENANT]
- Expected connections: [NUMBER]
- Data size: [SIZE_GB]
- Read/write ratio: [RATIO]
- RTO/RPO requirements: [RTO_MINUTES]/[RPO_MINUTES]

Include:
1. Instance sizing and tier selection
2. High availability configuration
3. Backup and PITR setup
4. Read replica strategy
5. Connection pooling recommendations
6. Monitoring flags and insights

Output as Terraform HCL with justifications.
```

### Microservices Architecture

```
Design a microservices architecture on GCP for:
- Number of services: [COUNT]
- Communication pattern: [SYNC/ASYNC/HYBRID]
- Traffic: [REQUESTS_PER_SECOND]
- Latency requirements: P99 < [MS]ms

Include:
1. Compute platform selection (GKE vs Cloud Run)
2. Service-to-service communication (gRPC, REST, Pub/Sub)
3. API Gateway configuration
4. Service mesh requirements (if applicable)
5. Observability stack (tracing, logging, metrics)
6. Database per service or shared database strategy

Provide architecture diagram description and Terraform code.
```

### Data Pipeline Design

```
Design a data pipeline on GCP for:
- Data sources: [SOURCE_TYPES]
- Volume: [GB_PER_DAY]
- Latency requirement: [REAL_TIME/NEAR_REAL_TIME/BATCH]
- Transformations: [TRANSFORMATION_TYPES]
- Consumers: [BI/ML/API]

Include:
1. Ingestion layer (Pub/Sub, Datastream, Transfer Service)
2. Processing layer (Dataflow, Dataproc, Cloud Functions)
3. Storage layer (BigQuery, Cloud Storage, BigLake)
4. Orchestration (Workflows, Composer, Cloud Scheduler)
5. Data quality and monitoring
6. Cost estimation

Output as architecture diagram description and Terraform/Beam code.
```

---

## Code Generation Prompts

### Terraform Module Generation

```
Generate a Terraform module for [RESOURCE_TYPE] with:
- Input variables with validation
- Sensible defaults for [ENVIRONMENT]
- Outputs for common integration points
- Conditional logic for dev/staging/prod environments
- Security best practices enabled by default

Resource requirements:
[SPECIFIC_REQUIREMENTS]

Follow Google Cloud best practices and include comments.
```

### Helm Chart Generation

```
Generate a Helm chart for deploying [APPLICATION] to GKE with:
- Deployment with [REPLICAS] replicas
- HPA with min [MIN] max [MAX] based on [METRIC]
- Service Account with Workload Identity annotation
- ConfigMap and Secret references
- Health checks (startup, liveness, readiness)
- Resource requests/limits
- NetworkPolicy for [INGRESS/EGRESS] rules
- PodDisruptionBudget

Include values.yaml with environment-specific overrides.
```

### Dataflow Pipeline

```
Generate a Dataflow pipeline in [PYTHON/JAVA] for:
- Source: [SOURCE_TYPE] ([SOURCE_DETAILS])
- Transformations:
  1. [TRANSFORM_1]
  2. [TRANSFORM_2]
  3. [TRANSFORM_3]
- Sink: [SINK_TYPE] ([SINK_DETAILS])
- Error handling: Dead letter queue for failed records
- Monitoring: Custom metrics for [METRIC_TYPES]

Use Apache Beam with GCP-specific I/O connectors.
```

---

## Troubleshooting Prompts

### GKE Troubleshooting

```
Troubleshoot the following GKE issue:
- Symptom: [SYMPTOM_DESCRIPTION]
- Error message: [ERROR_MESSAGE]
- Cluster version: [VERSION]
- Node pool type: [STANDARD/SPOT/AUTOPILOT]

Provide:
1. Diagnostic commands to run
2. Common causes for this issue
3. Resolution steps
4. Prevention measures
```

### Cloud SQL Troubleshooting

```
Troubleshoot Cloud SQL performance issue:
- Symptom: [HIGH_LATENCY/TIMEOUTS/CONNECTION_ERRORS]
- Instance tier: [TIER]
- Active connections: [COUNT]
- CPU/Memory usage: [PERCENTAGES]
- Query Insights data: [INSIGHTS_SUMMARY]

Analyze and provide:
1. Root cause analysis
2. Immediate mitigation steps
3. Long-term optimization recommendations
4. Monitoring alerts to add
```

### Networking Troubleshooting

```
Troubleshoot GCP networking issue:
- Source: [SOURCE_RESOURCE]
- Destination: [DESTINATION_RESOURCE]
- Error: [CONNECTION_REFUSED/TIMEOUT/DNS_ERROR]
- VPC configuration: [SHARED_VPC/STANDALONE]

Provide:
1. Connectivity test commands
2. Firewall rule analysis
3. Route verification
4. DNS configuration check
5. Resolution steps
```

---

## Migration Prompts

### AWS to GCP Migration

```
Create a migration plan from AWS [SERVICE] to GCP equivalent:

Source configuration:
[AWS_CONFIG]

Requirements:
- Zero downtime migration: [YES/NO]
- Data volume: [SIZE]
- Compliance requirements: [REQUIREMENTS]

Provide:
1. GCP equivalent service selection
2. Migration approach (lift-and-shift, re-platform, refactor)
3. Step-by-step migration plan
4. Rollback strategy
5. Validation checklist
6. Terraform code for target infrastructure
```

### Monolith to Microservices

```
Create a migration plan to decompose [MONOLITH_TYPE] into microservices on GCP:

Current state:
- Technology: [TECH_STACK]
- Database: [DATABASE_TYPE]
- Traffic: [REQUESTS_PER_SECOND]
- Team size: [SIZE]

Target state:
- Platform: [GKE/CLOUD_RUN/HYBRID]
- Services to extract: [SERVICE_LIST]

Provide:
1. Strangler fig pattern implementation
2. Database decomposition strategy
3. API gateway setup
4. Observability requirements
5. Phased rollout plan
6. Risk mitigation
```

---

## Cost Optimization Prompts

### Cost Analysis

```
Analyze and optimize GCP costs for:

Current monthly spend: $[AMOUNT]
Resources:
[RESOURCE_LIST_WITH_SPECS]

Provide:
1. Cost breakdown by service
2. Rightsizing recommendations
3. Committed Use Discount opportunities
4. Spot VM candidates
5. Storage class optimization
6. Network egress optimization
7. Estimated savings percentage
```

### FinOps Review

```
Perform FinOps review for GCP project [PROJECT_ID]:

Current state:
- Monthly budget: $[BUDGET]
- Critical workloads: [WORKLOAD_LIST]
- Non-critical workloads: [WORKLOAD_LIST]

Provide:
1. Tagging strategy for cost allocation
2. Budget alerts configuration
3. Recommendations export analysis
4. Reserved capacity planning
5. Showback/chargeback implementation
6. Cost optimization automation (Cloud Functions for cleanup)
```

---

## Security Prompts

### Security Review

```
Perform security review for GCP architecture:

Components:
[ARCHITECTURE_COMPONENTS]

Compliance requirements: [SOC2/HIPAA/PCI-DSS/GDPR]

Provide:
1. IAM audit (least privilege verification)
2. Network security assessment
3. Data encryption review (at rest, in transit)
4. Secret management evaluation
5. Logging and audit trail verification
6. Vulnerability assessment
7. Remediation plan with priority
```

### Zero Trust Implementation

```
Implement Zero Trust architecture on GCP for:

Access requirements:
- Internal users: [USER_GROUPS]
- External partners: [PARTNER_ACCESS]
- Service-to-service: [SERVICE_MESH_REQUIREMENTS]

Provide:
1. Identity-Aware Proxy configuration
2. VPC Service Controls setup
3. BeyondCorp Enterprise integration
4. Workload Identity implementation
5. Certificate-based authentication
6. Audit logging configuration
```

---

## Reference Prompts

### Architecture Decision Record

```
Create an ADR for: [DECISION_TITLE]

Context:
[CONTEXT_DESCRIPTION]

Options considered:
1. [OPTION_1]
2. [OPTION_2]
3. [OPTION_3]

Format:
- Title
- Status
- Context
- Decision
- Consequences
- References
```

### Runbook Generation

```
Create a runbook for: [OPERATION_TYPE]

System: [SYSTEM_DESCRIPTION]
SLO: [SLO_DEFINITION]

Include:
1. Pre-requisites and access requirements
2. Step-by-step procedures
3. Verification commands
4. Rollback procedures
5. Escalation path
6. Post-operation checklist
```

---

*GCP Architecture Patterns LLM Prompts | faion-infrastructure-engineer*
