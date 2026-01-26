# AWS Architecture Foundations LLM Prompts

## Multi-Account Strategy

### Design AWS Organization Structure

```
Design an AWS Organizations structure for [COMPANY_TYPE]:

Requirements:
- Company size: [STARTUP/SMB/ENTERPRISE]
- Compliance: [GDPR/HIPAA/PCI-DSS/SOC2/NONE]
- Environments: [DEV/STAGING/PROD] or [SPECIFY]
- Teams: [NUMBER] development teams
- Workloads: [WEB/API/ML/DATA/HYBRID]

Provide:
1. Recommended OU hierarchy
2. Account types and purposes
3. SCPs for each OU level
4. IAM Identity Center permission sets
5. Cross-account access patterns
6. Billing/cost allocation strategy
```

### Plan Control Tower Deployment

```
Plan AWS Control Tower deployment:

Current state:
- Existing accounts: [NUMBER] or greenfield
- Identity provider: [OKTA/AZURE_AD/GOOGLE/AWS_SSO_ONLY]
- Regions: [PRIMARY_REGION] + [SECONDARY_REGIONS]
- Compliance requirements: [LIST]

Deliverables:
1. Pre-deployment checklist
2. OU structure design
3. Guardrails selection (preventive/detective)
4. Account Factory configuration
5. Customizations via LZA (if needed)
6. Migration plan for existing accounts
```

## Well-Architected Review

### Conduct Well-Architected Assessment

```
Perform AWS Well-Architected review for [WORKLOAD_NAME]:

Workload description:
- Type: [WEB_APP/API/DATA_PIPELINE/ML/OTHER]
- Traffic: [REQUESTS_PER_SECOND]
- Data: [VOLUME] [SENSITIVITY_LEVEL]
- Criticality: [MISSION_CRITICAL/IMPORTANT/STANDARD]

Assess each pillar:
1. Operational Excellence
   - Deployment automation
   - Monitoring and observability
   - Incident response

2. Security
   - Identity and access management
   - Network security
   - Data protection

3. Reliability
   - Fault tolerance
   - Recovery procedures
   - Scaling strategy

4. Performance Efficiency
   - Compute optimization
   - Database performance
   - Caching strategy

5. Cost Optimization
   - Right-sizing
   - Reserved capacity
   - Waste elimination

6. Sustainability
   - Resource efficiency
   - Managed services usage

Output: Findings, recommendations, priority matrix
```

### Review Security Posture

```
Review AWS security posture for [ACCOUNT/ORGANIZATION]:

Scope:
- Accounts: [LIST] or organization-wide
- Focus areas: [IAM/NETWORK/DATA/COMPLIANCE/ALL]
- Compliance framework: [SPECIFY]

Check:
1. IAM
   - MFA enforcement
   - Access key rotation
   - Permission boundaries
   - Least privilege adherence

2. Network
   - VPC design
   - Security group rules
   - Public exposure
   - Flow log analysis

3. Data Protection
   - Encryption at rest
   - Encryption in transit
   - Key management
   - Data classification

4. Detection
   - GuardDuty findings
   - Security Hub score
   - Config compliance
   - CloudTrail coverage

Output: Risk matrix, remediation priorities, terraform code for fixes
```

## VPC Design

### Design VPC Architecture

```
Design VPC architecture for [WORKLOAD_TYPE]:

Requirements:
- Region: [AWS_REGION]
- High availability: [YES/NO]
- Workloads: [EKS/ECS/EC2/LAMBDA/MIXED]
- Database: [RDS/AURORA/DYNAMODB/NONE]
- Internet access: [FULL/EGRESS_ONLY/NONE]
- Connectivity: [STANDALONE/TRANSIT_GATEWAY/VPN/DIRECT_CONNECT]

Design:
1. CIDR planning (with growth)
2. Subnet layout (public/private/database)
3. NAT strategy (cost vs. availability)
4. VPC endpoints required
5. Security group rules
6. Network ACLs (if needed)
7. Flow logs configuration

Output: Terraform module with complete VPC configuration
```

### Plan Transit Gateway Network

```
Design Transit Gateway network topology:

Accounts and VPCs:
- [LIST_VPCS_WITH_CIDRS]

Requirements:
- Routing: [FULL_MESH/HUB_SPOKE/SEGMENTED]
- Inspection: [CENTRALIZED_FIREWALL/NONE]
- On-premises: [VPN/DIRECT_CONNECT/NONE]
- Cross-region: [YES/NO]

Provide:
1. Transit Gateway configuration
2. Route table design
3. Attachment strategy
4. Sharing via RAM
5. Security considerations
6. Cost estimate
```

## IAM Strategy

### Design IAM Strategy

```
Design IAM strategy for [USE_CASE]:

Context:
- Multi-account: [YES/NO]
- Identity source: [IAM_IDENTITY_CENTER/EXTERNAL_IDP/IAM_USERS]
- Workloads: [HUMAN/SERVICE/BOTH]
- EKS clusters: [NUMBER] (for IRSA)

Requirements:
- Role types needed: [LIST]
- Permission boundaries: [YES/NO]
- Cross-account access: [YES/NO]
- Temporary credentials only: [YES/NO]

Deliverables:
1. Permission set design (IAM Identity Center)
2. Role naming convention
3. Policy templates (S3, Secrets, DynamoDB, etc.)
4. IRSA configuration for EKS
5. Cross-account trust patterns
6. Audit and compliance controls
```

### Create Least Privilege Policy

```
Create least privilege IAM policy:

Service account: [NAME]
Purpose: [DESCRIPTION]

Required access:
- S3: [BUCKET_ARNS] [ACTIONS]
- Secrets Manager: [PREFIX_PATTERN]
- DynamoDB: [TABLE_ARNS] [ACTIONS]
- SQS: [QUEUE_ARNS] [ACTIONS]
- KMS: [KEY_ARNS]
- Other: [SPECIFY]

Constraints:
- Condition keys: [IP/VPC/MFA/TIME]
- Resource constraints: Required

Output: JSON policy with comments explaining each statement
```

## Monitoring and Observability

### Design Observability Stack

```
Design AWS observability stack for [ENVIRONMENT]:

Workloads:
- [LIST_WITH_TYPES]

Requirements:
- Metrics: [CLOUDWATCH/PROMETHEUS/BOTH]
- Logs: [CLOUDWATCH/OPENSEARCH/EXTERNAL]
- Traces: [XRAY/OTEL/EXTERNAL]
- Alerting: [CLOUDWATCH/PAGERDUTY/OPSGENIE]
- Dashboards: [CLOUDWATCH/GRAFANA]

Design:
1. Metrics collection strategy
2. Log aggregation architecture
3. Distributed tracing setup
4. Dashboard templates
5. Alert definitions (thresholds, routing)
6. Cost optimization (retention, sampling)
```

### Create Alerting Strategy

```
Create CloudWatch alerting strategy:

Services monitored:
- EKS cluster: [NAME]
- RDS/Aurora: [CLUSTER_ID]
- ALB: [NAME]
- Lambda functions: [LIST]
- Custom metrics: [NAMESPACE]

Alert tiers:
- P1 (Critical): [RESPONSE_TIME]
- P2 (High): [RESPONSE_TIME]
- P3 (Medium): [RESPONSE_TIME]
- P4 (Low): [RESPONSE_TIME]

For each service, define:
1. Key metrics to monitor
2. Thresholds (warning/critical)
3. Evaluation periods
4. Alert destinations
5. Runbook links
```

## Cost Optimization

### Analyze and Optimize Costs

```
Analyze AWS costs and recommend optimizations:

Current spend:
- Monthly: $[AMOUNT]
- Top services: [LIST]
- Growth trend: [PERCENTAGE]

Environment:
- Accounts: [NUMBER]
- Compute: [EC2/EKS/ECS/LAMBDA]
- Database: [RDS/AURORA/DYNAMODB]
- Storage: [S3_TB] [EBS_GB]

Analyze:
1. Compute utilization (right-sizing candidates)
2. Reserved Instance / Savings Plans coverage
3. Spot Instance opportunities
4. Storage tier optimization
5. Unused resources (EBS, EIP, snapshots)
6. Data transfer costs
7. NAT Gateway costs

Output: Prioritized recommendations with savings estimate
```

### Plan Reserved Capacity

```
Plan Reserved Instance / Savings Plans strategy:

Current on-demand usage:
- EC2: [INSTANCE_TYPES_AND_HOURS]
- RDS: [INSTANCE_TYPES_AND_HOURS]
- ElastiCache: [NODE_TYPES_AND_HOURS]
- Fargate: [VCPU_HOURS] [MEMORY_GB_HOURS]

Considerations:
- Commitment term: [1_YEAR/3_YEAR]
- Payment: [ALL_UPFRONT/PARTIAL/NO_UPFRONT]
- Flexibility needed: [HIGH/MEDIUM/LOW]
- Growth projection: [PERCENTAGE]

Recommend:
1. RI vs Savings Plans mix
2. Coverage targets by service
3. Purchase timeline
4. Break-even analysis
5. Flexibility trade-offs
```

## Disaster Recovery

### Design DR Strategy

```
Design disaster recovery strategy:

Workload: [NAME]
Criticality: [TIER_1/TIER_2/TIER_3]

Current state:
- Primary region: [REGION]
- Data stores: [LIST]
- RPO requirement: [TIME]
- RTO requirement: [TIME]

Design options:
1. Backup and restore
2. Pilot light
3. Warm standby
4. Multi-site active-active

For selected strategy:
- Infrastructure requirements
- Data replication approach
- Failover procedure
- Failback procedure
- Testing schedule
- Cost estimate
```

## Security Incident Response

### Create Incident Response Plan

```
Create AWS security incident response plan:

Organization context:
- Accounts: [NUMBER]
- Critical workloads: [LIST]
- Compliance: [REQUIREMENTS]

Plan sections:
1. Detection
   - GuardDuty finding types
   - Security Hub alerts
   - Custom detection rules

2. Investigation
   - Log sources and access
   - Forensics procedures
   - Evidence preservation

3. Containment
   - Isolation procedures
   - IAM response actions
   - Network quarantine

4. Eradication
   - Malware removal
   - Credential rotation
   - Vulnerability patching

5. Recovery
   - Service restoration
   - Data recovery
   - Validation steps

6. Post-incident
   - Root cause analysis
   - Lessons learned
   - Prevention measures
```

## Migration Planning

### Plan Workload Migration

```
Plan migration to AWS for [WORKLOAD]:

Current state:
- Platform: [ON_PREM/OTHER_CLOUD/COLO]
- Components: [LIST]
- Dependencies: [LIST]
- Data volume: [SIZE]

Target state:
- AWS services: [PROPOSED]
- Region: [TARGET]
- Compliance: [REQUIREMENTS]

Migration approach:
- Strategy: [REHOST/REPLATFORM/REFACTOR]
- Timeline: [PHASES]
- Risk tolerance: [HIGH/MEDIUM/LOW]

Deliverables:
1. Migration waves
2. Dependency mapping
3. Data migration approach
4. Cutover procedure
5. Rollback plan
6. Validation tests
```

## Quick Reference Prompts

### VPC Quick Design

```
Create Terraform for 3-tier VPC in [REGION] for [ENVIRONMENT]:
- CIDR: 10.0.0.0/16
- 3 AZs, public/private/database subnets
- NAT: [SINGLE/PER_AZ]
- Flow logs: enabled
- VPC endpoints: S3, ECR, Secrets Manager
```

### SCP Quick Create

```
Create SCP to [OBJECTIVE]:
Examples:
- Deny root user access
- Restrict to EU regions only
- Require S3 encryption
- Deny public S3 buckets
- Require IMDSv2 for EC2
```

### IAM Role Quick Create

```
Create IAM role for [SERVICE_ACCOUNT] in EKS:
- Cluster: [NAME]
- Namespace: [NS]
- S3 access: [BUCKETS]
- Secrets access: [PREFIX]
- DynamoDB: [TABLES]
```

### Alarm Quick Create

```
Create CloudWatch alarm for [SERVICE]:
- Metric: [NAME]
- Threshold: [VALUE]
- Period: [SECONDS]
- SNS topic: [ARN]
```
