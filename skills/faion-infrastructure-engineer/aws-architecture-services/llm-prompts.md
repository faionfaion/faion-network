# AWS Architecture Services - LLM Prompts

Prompts for AWS architecture decisions and service selection.

## Service Selection Prompts

### Serverless vs Containers Decision

```
Analyze my workload requirements and recommend whether to use AWS Lambda (serverless) or containers (EKS/ECS/Fargate):

WORKLOAD CHARACTERISTICS:
- Traffic pattern: [steady/variable/spiky/unpredictable]
- Average requests per second: [number]
- Peak requests per second: [number]
- Request duration: [average ms/seconds]
- Cold start tolerance: [critical/acceptable/not important]
- Memory requirements: [MB]
- CPU requirements: [intensive/moderate/light]
- GPU required: [yes/no]
- Custom runtime needed: [yes/no]
- Existing Kubernetes expertise: [high/medium/low/none]

Please provide:
1. Recommended compute service with reasoning
2. Cost comparison estimate
3. Operational complexity assessment
4. Migration path if starting with one and scaling to another
5. Hybrid approach considerations
```

### EKS vs ECS vs Fargate Decision

```
Compare EKS, ECS, and Fargate for my containerized application:

APPLICATION PROFILE:
- Number of microservices: [number]
- Team size: [number]
- Kubernetes expertise: [high/medium/low/none]
- Multi-cloud requirements: [yes/no]
- Existing EKS/ECS clusters: [describe]
- Compliance requirements: [list]
- Estimated monthly compute hours: [number]

Please provide:
1. Recommended service with justification
2. Pros and cons for each option
3. Cost estimation comparison
4. Operational overhead comparison
5. Learning curve assessment
```

### Database Selection

```
Recommend the optimal AWS database service for my application:

DATA REQUIREMENTS:
- Data model: [relational/document/key-value/graph/time-series]
- Expected data size: [GB/TB]
- Read/write ratio: [reads:writes]
- Transactions required: [ACID/eventual consistency]
- Query patterns: [describe typical queries]
- Latency requirements: [ms]
- Availability requirements: [99.9%/99.99%/99.999%]
- Global distribution needed: [yes/no]
- Existing database expertise: [PostgreSQL/MySQL/MongoDB/DynamoDB/etc.]

Please recommend:
1. Primary database service (Aurora/RDS/DynamoDB/DocumentDB/etc.)
2. Instance sizing and configuration
3. High availability setup
4. Backup and recovery strategy
5. Cost optimization tips
```

## Architecture Review Prompts

### Well-Architected Review

```
Review my AWS architecture against the Well-Architected Framework:

CURRENT ARCHITECTURE:
[Describe your architecture or paste Terraform code]

FOCUS AREAS:
- [ ] Operational Excellence
- [ ] Security
- [ ] Reliability
- [ ] Performance Efficiency
- [ ] Cost Optimization
- [ ] Sustainability

Please provide:
1. Assessment for each pillar (1-5 rating)
2. Top 3 issues per pillar
3. Prioritized remediation recommendations
4. Quick wins vs long-term improvements
5. Estimated effort for each recommendation
```

### Security Review

```
Perform a security review of my AWS infrastructure:

INFRASTRUCTURE COMPONENTS:
[List services: EKS, RDS, S3, Lambda, etc.]

SECURITY CONCERNS:
- IAM policies: [paste or describe]
- Network configuration: [VPC, security groups, NACLs]
- Encryption status: [at rest, in transit]
- Secrets management: [current approach]
- Logging and monitoring: [current setup]

Please identify:
1. Critical security gaps
2. IAM over-permissions
3. Network exposure risks
4. Encryption gaps
5. Compliance considerations (SOC2, HIPAA, etc.)
6. Remediation steps with priority
```

### Cost Optimization Review

```
Analyze my AWS infrastructure for cost optimization:

CURRENT SETUP:
[Describe services, instance types, usage patterns]

MONTHLY SPEND:
- EC2/EKS: $[amount]
- RDS: $[amount]
- Lambda: $[amount]
- S3: $[amount]
- Data Transfer: $[amount]
- Other: $[amount]

Please provide:
1. Right-sizing recommendations
2. Reserved Instances / Savings Plans opportunities
3. Spot Instance candidates
4. Unused resources to terminate
5. Architecture changes for cost reduction
6. Estimated savings per recommendation
```

## Event-Driven Architecture Prompts

### EventBridge Design

```
Design an event-driven architecture using Amazon EventBridge:

USE CASE:
[Describe the business process]

EVENT SOURCES:
[List: AWS services, custom applications, SaaS integrations]

EVENT CONSUMERS:
[List: Lambda, Step Functions, SQS, SNS, etc.]

REQUIREMENTS:
- Event volume: [events/second]
- Latency requirements: [ms]
- Ordering requirements: [strict/best-effort/none]
- Error handling: [retry strategy]
- Cross-account: [yes/no]

Please design:
1. Event bus structure (default vs custom)
2. Event schema definitions
3. Event rules and patterns
4. Target configurations
5. Dead-letter queue strategy
6. Monitoring and observability setup
```

### Choreography vs Orchestration

```
Recommend choreography vs orchestration for my workflow:

WORKFLOW DESCRIPTION:
[Describe the business process step by step]

CHARACTERISTICS:
- Number of steps: [number]
- Sequential dependencies: [describe]
- Parallel execution: [yes/no]
- Error handling complexity: [simple/complex]
- Compensation actions needed: [yes/no]
- Long-running steps: [yes/no, duration]
- Human approval steps: [yes/no]

Please recommend:
1. Choreography (EventBridge) or Orchestration (Step Functions)
2. Hybrid approach if applicable
3. Architecture diagram description
4. Error handling strategy
5. Monitoring approach
```

## Migration Prompts

### Container Migration

```
Plan migration of my application to AWS containers:

CURRENT STATE:
- Application type: [monolith/microservices]
- Current hosting: [on-prem/other cloud/EC2]
- Languages/frameworks: [list]
- Database: [current setup]
- Dependencies: [external services]

TARGET STATE:
- Container orchestration: [EKS/ECS/Fargate]
- Environment: [dev/staging/prod]
- Timeline: [desired timeline]

Please provide:
1. Migration strategy (lift-and-shift vs refactor)
2. Containerization approach
3. CI/CD pipeline design
4. Networking and security setup
5. Data migration plan
6. Rollback strategy
7. Risk assessment
```

### Serverless Migration

```
Plan migration to AWS serverless:

CURRENT APPLICATION:
- Architecture: [monolith/microservices/API]
- Current hosting: [EC2/ECS/on-prem]
- Request patterns: [describe]
- Database: [current DB]
- State management: [how state is handled]

Please provide:
1. Serverless architecture design
2. Lambda function decomposition
3. API Gateway configuration
4. Database migration (to DynamoDB or Aurora Serverless)
5. State management with Step Functions
6. Cold start mitigation strategies
7. Cost comparison before/after
```

## Terraform Code Generation Prompts

### Generate EKS Cluster

```
Generate production-ready Terraform code for an EKS cluster:

REQUIREMENTS:
- Cluster version: 1.31
- Node groups: general (on-demand) + spot
- Instance types: Graviton (arm64)
- VPC: existing or new
- Add-ons: CoreDNS, kube-proxy, VPC CNI, EBS CSI
- IRSA: enabled
- Secrets encryption: KMS
- Logging: CloudWatch

Include:
1. EKS cluster module configuration
2. Node group definitions
3. IAM roles and policies
4. Security groups
5. Add-on configurations
6. Output values
```

### Generate RDS Aurora

```
Generate production-ready Terraform code for Aurora PostgreSQL:

REQUIREMENTS:
- Engine version: 16.x
- Instance class: db.r7g.large (Graviton)
- Instances: 1 writer + 1 reader
- Multi-AZ: yes
- Encryption: KMS
- Performance Insights: enabled
- Backup retention: 30 days (prod) / 7 days (non-prod)
- Deletion protection: prod only

Include:
1. Aurora module configuration
2. KMS key for encryption
3. Security group
4. Parameter group customizations
5. CloudWatch alarms
6. Output values
```

### Generate S3 + CloudFront

```
Generate Terraform code for S3 bucket with CloudFront distribution:

REQUIREMENTS:
- S3: private, versioned, encrypted
- CloudFront: OAC, HTTPS only, compression
- Domain: static.example.com
- Cache policy: CachingOptimized
- Lifecycle: transition to IA at 90 days, Glacier at 180 days

Include:
1. S3 bucket module
2. CloudFront distribution module
3. Origin Access Control
4. ACM certificate (us-east-1)
5. Route53 records
6. S3 bucket policy for CloudFront
```

## Troubleshooting Prompts

### Debug EKS Issues

```
Help me troubleshoot EKS cluster issues:

SYMPTOMS:
[Describe the problem: pods not starting, networking issues, etc.]

CLUSTER INFO:
- EKS version: [version]
- Node groups: [describe]
- VPC configuration: [describe]
- Add-ons: [list]

ERROR MESSAGES:
[Paste relevant error messages from kubectl, CloudWatch, etc.]

Please help:
1. Diagnose the root cause
2. Provide step-by-step debugging commands
3. Recommend fixes
4. Suggest preventive measures
```

### Debug Lambda Issues

```
Help me troubleshoot Lambda function issues:

SYMPTOMS:
[Describe: cold starts, timeouts, errors, etc.]

FUNCTION CONFIGURATION:
- Runtime: [runtime]
- Memory: [MB]
- Timeout: [seconds]
- VPC: [yes/no]
- Concurrency: [number]

ERROR LOGS:
[Paste CloudWatch logs]

Please help:
1. Identify the issue
2. Provide resolution steps
3. Recommend configuration optimizations
4. Suggest monitoring improvements
```

---

*AWS Architecture Services LLM Prompts | faion-infrastructure-engineer*
