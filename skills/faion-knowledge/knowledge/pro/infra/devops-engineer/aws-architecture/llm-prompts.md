# LLM Prompts for AWS Architecture

## Architecture Design

### Initial Architecture Assessment

```
You are an AWS Solutions Architect. Analyze the following requirements and propose an AWS architecture:

**Project:** {project_name}
**Requirements:**
{requirements}

**Constraints:**
- Budget: {budget_range}
- Compliance: {compliance_requirements}
- Team expertise: {team_expertise}

Please provide:
1. High-level architecture diagram (describe in text)
2. AWS services selection with justification
3. Cost estimation breakdown
4. Well-Architected Framework alignment (6 pillars)
5. Potential risks and mitigations
```

### Architecture Review

```
Review the following AWS architecture against the Well-Architected Framework:

**Current Architecture:**
{architecture_description}

**Services Used:**
{service_list}

Evaluate each pillar:
1. Operational Excellence
2. Security
3. Reliability
4. Performance Efficiency
5. Cost Optimization
6. Sustainability

For each pillar, provide:
- Current state assessment (1-5 rating)
- Gaps identified
- Specific recommendations
- Priority (High/Medium/Low)
```

---

## Terraform Generation

### VPC and Networking

```
Generate Terraform code for AWS VPC with these requirements:

**Requirements:**
- Region: {region}
- Environment: {environment}
- CIDR: {vpc_cidr}
- Availability Zones: {num_azs}
- Subnet tiers: public, private, database

**Features needed:**
- NAT Gateway (single for dev, per-AZ for prod)
- VPC Flow Logs
- DNS hostnames enabled
- Tags for Kubernetes (if applicable)

Use terraform-aws-modules/vpc/aws module version ~> 5.0.
Include proper naming conventions: {project}-{environment}.
```

### EKS Cluster

```
Generate Terraform code for EKS cluster:

**Requirements:**
- Cluster name: {cluster_name}
- Kubernetes version: {k8s_version}
- Node groups:
  - General: {instance_types}, min/max nodes
  - Spot: {spot_instance_types}, for non-critical workloads

**Add-ons:**
- CoreDNS, kube-proxy, VPC-CNI
- EBS CSI driver with IRSA
- Pod Identity agent

**Security:**
- Secrets encryption with KMS
- Private endpoint access
- IRSA enabled

Use terraform-aws-modules/eks/aws module version ~> 20.0.
Prefer Graviton (ARM64) instances for cost optimization.
```

### Serverless API

```
Generate Terraform for serverless API:

**Components:**
- API Gateway (HTTP API)
- Lambda function (Python/Node.js)
- DynamoDB table

**Requirements:**
- Custom domain: api.{domain}
- CORS for {frontend_domain}
- ARM64 architecture for Lambda
- X-Ray tracing enabled
- Least privilege IAM

**DynamoDB:**
- Single-table design with pk/sk
- On-demand billing
- Point-in-time recovery
- Encryption with KMS

Use terraform-aws-modules for each component.
```

---

## Security

### IAM Policy Generation

```
Generate a least-privilege IAM policy for:

**Service/Role:** {service_name}
**Needs access to:**
{resource_list}

**Operations required:**
{operations_list}

Requirements:
- Use specific ARNs, not wildcards
- Separate statements by resource type
- Include condition keys where appropriate
- Add Sid for each statement for clarity

Output as Terraform aws_iam_policy resource.
```

### Security Group Rules

```
Design security groups for three-tier architecture:

**Tiers:**
1. ALB (public-facing)
2. Application (ECS/EKS pods)
3. Database (RDS/Aurora)

**Requirements:**
- Principle of least privilege
- Only allow necessary ports
- Reference other security groups (not CIDRs) where possible
- No egress restrictions for app tier
- No egress for database tier

Use terraform-aws-modules/security-group/aws.
```

---

## Cost Optimization

### Cost Analysis

```
Analyze the following AWS architecture for cost optimization:

**Current monthly cost:** ${current_cost}
**Services:**
{service_list_with_specs}

**Usage patterns:**
{usage_patterns}

Provide recommendations for:
1. Right-sizing opportunities
2. Reserved capacity/Savings Plans analysis
3. Spot instance candidates
4. Storage optimization (tiering, lifecycle)
5. Serverless migration candidates
6. Quick wins (immediate savings)
7. Medium-term optimizations

Calculate estimated savings for each recommendation.
```

### Reserved Capacity Planning

```
Recommend Reserved Instances or Savings Plans:

**Current on-demand usage:**
{instance_usage}

**Usage characteristics:**
- Baseline load: {baseline}
- Peak load: {peak}
- Usage hours: {hours_per_day}
- Workload stability: {stable/variable}

Recommend:
1. Compute Savings Plans vs EC2 Reserved Instances
2. 1-year vs 3-year commitment
3. All Upfront vs No Upfront
4. Coverage percentage recommendation
```

---

## Reliability and DR

### Disaster Recovery Design

```
Design disaster recovery strategy for:

**Application:** {application_description}
**RTO:** {rto}
**RPO:** {rpo}
**Current region:** {primary_region}
**DR region:** {dr_region}

**Components:**
{component_list}

Provide:
1. DR strategy (backup/restore, pilot light, warm standby, active-active)
2. Data replication approach
3. DNS failover configuration
4. Recovery runbook outline
5. Testing strategy
6. Cost implications
```

### High Availability Assessment

```
Assess high availability for:

**Architecture:**
{architecture_description}

Evaluate:
1. Single points of failure
2. Multi-AZ deployment status
3. Auto-scaling configuration
4. Health check coverage
5. Failover mechanisms
6. Data durability

For each gap found, provide:
- Impact assessment
- Remediation steps
- Terraform code changes
```

---

## Monitoring and Observability

### CloudWatch Setup

```
Design CloudWatch monitoring for:

**Services:**
{service_list}

**Key metrics to track:**
{business_metrics}

Create:
1. Dashboard layout (JSON format)
2. Alarms with appropriate thresholds
3. Log groups and retention policies
4. Metric filters for application logs
5. SNS topics and subscriptions
6. Composite alarms for service health

Use Terraform resources.
```

### Alerting Strategy

```
Design alerting strategy for production AWS workload:

**Services:** {service_list}
**On-call team:** {team_size}
**Escalation path:** {escalation_description}

Define:
1. Critical alerts (immediate page)
2. Warning alerts (business hours)
3. Informational alerts (daily digest)

For each alert:
- Metric and threshold
- Evaluation period
- Actions (SNS, Lambda, etc.)
- Runbook link placeholder

Output as Terraform aws_cloudwatch_metric_alarm resources.
```

---

## Migration

### Migration Assessment

```
Assess migration of on-premises workload to AWS:

**Current state:**
{current_infrastructure}

**Workload characteristics:**
{workload_description}

**Dependencies:**
{dependencies}

Provide:
1. Migration strategy (6 Rs assessment)
2. AWS service mapping
3. Migration phases
4. Risk assessment
5. Rollback plan
6. Cost comparison (on-prem vs AWS)
```

### Containerization

```
Design containerization strategy for:

**Application:** {application_description}
**Current deployment:** {current_deployment}
**Team container experience:** {experience_level}

Recommend:
1. ECS vs EKS decision
2. Fargate vs EC2 launch type
3. Container registry (ECR)
4. CI/CD pipeline
5. Service mesh (if needed)
6. Migration approach

Include Terraform code for core components.
```

---

## Serverless Patterns

### Event-Driven Architecture

```
Design event-driven architecture for:

**Use case:** {use_case}
**Event sources:** {event_sources}
**Processing requirements:** {processing_requirements}
**Latency requirements:** {latency}

Design using:
1. EventBridge for event routing
2. SQS for buffering
3. Lambda for processing
4. Step Functions for orchestration (if needed)
5. DynamoDB for state

Include:
- Event schema
- Dead letter queue handling
- Retry strategy
- Monitoring approach

Provide Terraform code.
```

### GenAI RAG Architecture

```
Design RAG (Retrieval-Augmented Generation) architecture on AWS:

**Use case:** {use_case}
**Data sources:** {data_sources}
**Query volume:** {expected_qps}
**Latency requirements:** {latency}

Components:
1. Vector database (Kendra, OpenSearch Serverless, Aurora pgvector)
2. Embedding generation (Bedrock, SageMaker)
3. LLM inference (Bedrock)
4. API layer (API Gateway + Lambda)
5. Caching strategy

Include:
- Data ingestion pipeline
- Chunking strategy
- Prompt templates
- Cost estimation
- Terraform code for infrastructure
```

---

## Troubleshooting

### Performance Investigation

```
Investigate performance issue:

**Symptom:** {symptom_description}
**Affected service:** {service}
**Timeline:** {when_started}
**Changes made:** {recent_changes}

Provide investigation steps:
1. Metrics to check
2. Logs to analyze
3. Traces to review
4. Potential root causes
5. Quick mitigations
6. Long-term fixes

For each step, include AWS CLI commands or Console navigation.
```

### Cost Spike Analysis

```
Analyze unexpected cost increase:

**Service with spike:** {service}
**Cost increase:** ${amount} ({percentage}%)
**Time period:** {period}

Investigation steps:
1. Cost Explorer analysis dimensions
2. CloudWatch metrics to correlate
3. CloudTrail events to review
4. Potential causes
5. Remediation actions

Provide AWS CLI commands for analysis.
```
