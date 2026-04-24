# AWS LLM Prompts

Optimized prompts for AWS infrastructure tasks using LLMs.

---

## Infrastructure Design Prompts

### VPC Architecture

```
Design a VPC architecture for a [production/staging/development] environment with the following requirements:

Requirements:
- [Number] availability zones
- Public and private subnets
- NAT Gateway for private subnet internet access
- [Specific compliance requirements if any]

Application profile:
- [Web application / API service / Data processing]
- Expected traffic: [High/Medium/Low]
- Data sensitivity: [High/Medium/Low]

Output:
1. CIDR block allocation plan
2. Subnet layout with AZ distribution
3. Route table configuration
4. Security group rules
5. Network ACL recommendations
6. Estimated monthly cost

Format: Terraform code with comments explaining each decision.
```

### ECS/EKS Architecture

```
Design a container orchestration architecture for:

Application:
- [Microservices count and names]
- [Container image sizes and resource requirements]
- [Inter-service communication patterns]

Requirements:
- High availability across [number] AZs
- Auto-scaling based on [CPU/Memory/Custom metrics]
- Blue-green deployment capability
- [Fargate/EC2/Mixed] compute type

Constraints:
- Budget: $[amount]/month
- Compliance: [HIPAA/PCI-DSS/SOC2/None]

Output:
1. Cluster architecture diagram (describe)
2. Task/Pod definitions
3. Service mesh configuration (if needed)
4. Deployment strategy
5. Monitoring and alerting setup
6. Cost breakdown
```

### Serverless Architecture

```
Design a serverless architecture for:

Use case: [API backend / Event processing / Scheduled jobs]

Workload characteristics:
- Requests per second: [Peak] / [Average]
- Execution duration: [Short < 1s / Medium 1-15s / Long > 15s]
- Memory requirements: [MB]
- Cold start tolerance: [High/Medium/Low]

Integrations:
- [List of AWS services to integrate]
- [External APIs/services]

Output:
1. Lambda function design
2. API Gateway configuration
3. Event source mappings
4. Step Functions workflow (if applicable)
5. Error handling and retry strategy
6. Cost estimation based on usage pattern
```

---

## Security Prompts

### IAM Policy Design

```
Create an IAM policy for:

Role: [Developer / DevOps / Application / Service]

Required permissions:
- [List specific actions needed]
- [Resources to access]

Constraints:
- Follow least-privilege principle
- Include conditions for:
  - MFA requirement: [Yes/No]
  - IP restriction: [CIDR ranges]
  - Time-based access: [Yes/No]

Output:
1. IAM policy JSON
2. Explanation of each statement
3. Trust policy (if role)
4. Permission boundaries recommendation
5. Service Control Policy considerations
```

### Security Audit

```
Perform a security audit for the following AWS environment:

Current setup:
- [List of services in use]
- [VPC architecture summary]
- [IAM structure summary]

Focus areas:
- [ ] IAM best practices
- [ ] Network security
- [ ] Data encryption
- [ ] Logging and monitoring
- [ ] Incident response readiness

Compliance requirements: [HIPAA/PCI-DSS/SOC2/GDPR/None]

Output:
1. Security findings with severity (Critical/High/Medium/Low)
2. Remediation recommendations
3. AWS CLI commands to fix issues
4. CloudFormation/Terraform for automation
5. Compliance gap analysis
```

### Secrets Management

```
Design a secrets management strategy for:

Application type: [Web app / Microservices / Batch processing]

Secrets to manage:
- [Database credentials]
- [API keys]
- [Certificates]
- [Other sensitive config]

Requirements:
- Rotation frequency: [Days]
- Access pattern: [On-demand / Cached / Startup only]
- Cross-account access: [Yes/No]

Output:
1. Secrets Manager vs Parameter Store recommendation
2. Secret structure and naming convention
3. Rotation Lambda function design
4. Application integration code (Python/Node.js)
5. IAM policies for secret access
6. Monitoring and alerting for secret access
```

---

## Cost Optimization Prompts

### Cost Analysis

```
Analyze costs for the following AWS workload:

Current infrastructure:
- EC2: [Instance types and count]
- RDS: [Instance types and storage]
- S3: [Storage volume and access patterns]
- Data transfer: [Inbound/Outbound volumes]
- Other services: [List]

Usage patterns:
- Peak hours: [Time range]
- Low usage periods: [Time range]
- Seasonal variations: [Description]

Budget target: $[amount]/month
Current spend: $[amount]/month

Output:
1. Cost breakdown by service
2. Savings opportunities with percentages
3. Reserved Instances/Savings Plans recommendations
4. Spot Instance opportunities
5. Right-sizing recommendations
6. Architecture changes for cost reduction
7. Implementation priority and estimated savings
```

### Right-Sizing

```
Right-size the following EC2 instances:

Current instances:
| Instance ID | Type | vCPU | Memory | Current CPU% | Current Mem% |
|-------------|------|------|--------|--------------|--------------|
| [ID] | [Type] | [#] | [GB] | [%] | [%] |

Workload characteristics:
- [CPU-bound / Memory-bound / Balanced]
- Performance requirements: [Latency sensitive / Throughput focused]
- Burstable acceptable: [Yes/No]

Constraints:
- Graviton compatible: [Yes/No]
- Spot acceptable: [Yes/No]
- Minimum availability: [%]

Output:
1. Recommended instance types with justification
2. Cost savings per instance
3. Performance impact analysis
4. Migration strategy
5. AWS CLI commands for modification
```

### Reserved Instance Strategy

```
Design a Reserved Instance/Savings Plans strategy:

Current usage:
- [Instance types and hours per month]
- [Lambda invocations and duration]
- [Fargate vCPU and memory hours]

Commitment tolerance:
- Maximum upfront payment: $[amount]
- Commitment term: [1-year / 3-year / Flexible]
- Payment preference: [All Upfront / Partial / No Upfront]

Output:
1. Savings Plans vs Reserved Instances comparison
2. Recommended coverage percentage
3. Specific RI/SP purchases
4. Flexibility considerations
5. Break-even analysis
6. Implementation timeline
```

---

## Reliability Prompts

### Disaster Recovery Design

```
Design a disaster recovery strategy for:

Application: [Description]
Tier: [1-Critical / 2-Important / 3-Standard]

Requirements:
- RTO: [Time]
- RPO: [Time]
- Data volume: [Size]
- Geographic requirements: [Regions]

Current architecture:
- Primary region: [Region]
- Data stores: [RDS/DynamoDB/S3/etc.]
- Compute: [EC2/ECS/Lambda/etc.]

Output:
1. DR strategy (Pilot Light / Warm Standby / Multi-Site)
2. Replication architecture
3. Failover procedure (runbook)
4. Failback procedure
5. Testing strategy
6. Cost comparison of DR options
7. CloudFormation/Terraform for DR infrastructure
```

### High Availability Design

```
Design high availability for:

Application type: [Web / API / Database / Queue processor]

Requirements:
- Uptime SLA: [99.9% / 99.95% / 99.99%]
- Max acceptable downtime per month: [Minutes]
- Geographic distribution: [Single region / Multi-region]

Current single points of failure:
- [List known SPOFs]

Constraints:
- Budget increase limit: [%]
- Complexity tolerance: [Low / Medium / High]

Output:
1. HA architecture design
2. Multi-AZ deployment strategy
3. Load balancing configuration
4. Auto-scaling policies
5. Health check design
6. Failure scenarios and mitigations
7. Cost impact analysis
```

### Auto-Scaling Strategy

```
Design auto-scaling for:

Service: [ECS / EKS / EC2 / Lambda]

Traffic patterns:
- Baseline: [Requests/sec or concurrent users]
- Peak: [Requests/sec or concurrent users]
- Peak timing: [Predictable schedule / Unpredictable]
- Ramp-up time: [Seconds]

Performance targets:
- Response time p95: [ms]
- Error rate: [%]
- Throughput: [Requests/sec]

Constraints:
- Minimum capacity: [Units]
- Maximum capacity: [Units]
- Scale-out speed priority: [Cost / Speed]

Output:
1. Scaling metrics selection with thresholds
2. Target tracking vs step scaling recommendation
3. Scaling policy configuration
4. Scheduled scaling (if applicable)
5. Warm-up and cooldown periods
6. Capacity planning for peak events
```

---

## Migration Prompts

### Workload Migration

```
Plan migration of:

Source environment:
- [On-premises / Other cloud / Different AWS account]
- Servers: [Count and specs]
- Databases: [Types and sizes]
- Storage: [Volumes and types]
- Network: [Current connectivity]

Application dependencies:
- [List dependencies and integrations]

Migration constraints:
- Downtime tolerance: [Hours/Minutes/Zero]
- Timeline: [Weeks]
- Team expertise: [AWS experience level]

Output:
1. Migration strategy (Rehost/Replatform/Refactor)
2. Phased migration plan
3. AWS Migration tools to use
4. Network connectivity setup
5. Data migration approach
6. Testing and validation plan
7. Rollback strategy
8. Timeline with milestones
```

### Database Migration

```
Plan database migration:

Source:
- Database: [MySQL/PostgreSQL/Oracle/SQL Server/MongoDB]
- Version: [Version]
- Size: [GB]
- Connections: [Count]

Target: [RDS/Aurora/DynamoDB/DocumentDB]

Requirements:
- Downtime tolerance: [Hours/Minutes]
- Data validation needs: [High/Medium/Low]
- Performance comparison: [Required/Optional]

Output:
1. DMS vs native migration tool recommendation
2. Schema conversion requirements
3. Migration task configuration
4. Change Data Capture setup for minimal downtime
5. Validation queries
6. Performance tuning for target
7. Cutover procedure
8. Rollback plan
```

---

## Monitoring and Observability Prompts

### Monitoring Strategy

```
Design monitoring and observability for:

Application: [Description]
Architecture: [Monolith / Microservices / Serverless]

Components to monitor:
- [List services and infrastructure]

Requirements:
- Alerting response time: [Minutes]
- Log retention: [Days]
- Metric granularity: [Seconds]
- Distributed tracing: [Yes/No]

Output:
1. CloudWatch metrics and dashboards
2. Log aggregation strategy
3. X-Ray tracing configuration
4. Alert thresholds and escalation
5. Runbooks for common alerts
6. Cost-effective log retention
7. Third-party tools integration (if applicable)
```

### Alerting Design

```
Design alerting strategy for:

Environment: [Production / Staging / Development]
On-call team: [Size and timezone coverage]

Services to alert on:
| Service | Criticality | Current SLA |
|---------|-------------|-------------|
| [Name] | [High/Med/Low] | [%] |

Alert channels:
- [PagerDuty/OpsGenie/SNS/Slack]

Output:
1. Alert hierarchy (P1-P4)
2. Metric thresholds per service
3. Composite alarms for complex conditions
4. Escalation policies
5. Alert routing rules
6. Suppression and maintenance windows
7. Alert fatigue mitigation
```

---

## Prompt Engineering Tips

### Context Setting

Always include:
- Environment type (production/staging/dev)
- Scale and traffic patterns
- Compliance requirements
- Budget constraints
- Team expertise level

### Output Formatting

Request specific formats:
- "Provide as Terraform code"
- "Include AWS CLI commands"
- "Format as runbook"
- "Create as CloudFormation template"

### Iteration

Follow-up prompts:
- "Make this more cost-effective"
- "Add [specific feature] to this design"
- "Convert to multi-region"
- "Add compliance controls for [standard]"

---

## Sources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/welcome.html)
- [AWS Cost Optimization](https://aws.amazon.com/aws-cost-management/cost-optimization/)
