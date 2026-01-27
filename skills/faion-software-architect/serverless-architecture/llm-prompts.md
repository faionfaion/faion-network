# LLM Prompts for Serverless Architecture

Effective prompts for LLM-assisted serverless design, implementation, and optimization.

## Architecture Design Prompts

### Initial Architecture Assessment

```
I need to design a serverless architecture for [APPLICATION TYPE].

Requirements:
- Expected traffic: [X requests/day, peak patterns]
- Latency requirements: [p95 < Xms]
- Data model: [describe main entities]
- Integrations: [external APIs, services]
- Compliance: [GDPR, HIPAA, etc.]
- Budget constraints: [if any]

Current tech stack: [existing technologies]
Cloud provider preference: [AWS/Azure/GCP/multi-cloud]

Please recommend:
1. Overall architecture pattern (event-driven, API-centric, etc.)
2. Specific services to use
3. Data storage strategy
4. Key design decisions with tradeoffs
5. Cost estimate at expected scale
```

### Serverless Fit Assessment

```
Evaluate whether serverless is appropriate for this use case:

Application: [description]
Workload characteristics:
- Request rate: [X/second average, X/second peak]
- Request duration: [X ms average]
- Traffic pattern: [spiky/steady/predictable]
- State requirements: [stateless/stateful/sessions]

Current infrastructure: [if migrating]
Team experience: [serverless experience level]

Please analyze:
1. Serverless suitability score (1-10) with reasoning
2. Key risks and mitigations
3. Alternative approaches if serverless is not ideal
4. Migration path if applicable
5. Cost comparison (serverless vs containers vs VMs)
```

### Event-Driven Design

```
Design an event-driven serverless architecture for:

Use case: [description]
Event sources: [S3 uploads, API calls, IoT devices, etc.]
Processing requirements:
- Order guarantee needed: [yes/no]
- Exactly-once processing: [yes/no]
- Processing latency: [real-time/near-real-time/batch]
- Throughput: [events/second]

Please provide:
1. Event flow diagram
2. Choice of messaging service (SQS vs SNS vs EventBridge vs Kinesis)
3. Event schema design
4. Error handling and retry strategy
5. Dead-letter queue configuration
6. Idempotency approach
```

### Multi-Tenant SaaS Design

```
Design a multi-tenant serverless SaaS architecture:

Product: [description]
Tenant model:
- Expected tenants: [X]
- Isolation level needed: [shared DB/siloed DB/compute isolation]
- Tenant tiers: [free/pro/enterprise features]

Requirements:
- Per-tenant rate limiting
- Tenant-specific configuration
- Usage metering for billing
- Audit logging

Please design:
1. Tenant isolation strategy
2. Data model with tenant partitioning
3. Authentication/authorization flow
4. Rate limiting implementation
5. Metering and billing integration
6. Cost allocation approach
```

---

## Implementation Prompts

### Lambda Function Design

```
Create a Lambda function for:

Purpose: [description]
Trigger: [API Gateway/SQS/S3/EventBridge/etc.]
Runtime: [Python/Node.js/Go/etc.]
Input: [expected event structure]
Output: [expected response]

Requirements:
- Idempotency: [yes/no]
- Retry behavior: [describe]
- External dependencies: [APIs, databases]
- Performance target: [X ms p95]

Please provide:
1. Complete handler code with best practices
2. Error handling strategy
3. Logging and tracing setup (Powertools)
4. Unit test examples
5. IAM policy (least privilege)
6. SAM/CDK template snippet
```

### DynamoDB Single-Table Design

```
Design a DynamoDB single-table schema for:

Entities:
- [Entity 1]: [attributes]
- [Entity 2]: [attributes]
- [Entity 3]: [attributes]

Access patterns:
1. [Get entity by ID]
2. [List entities by category]
3. [Query entities by date range]
4. [Get related entities]

Please provide:
1. Table schema (PK, SK, GSIs)
2. Access pattern implementation for each query
3. Example items
4. Python/TypeScript code examples
5. Cost estimation approach
```

### Step Functions Workflow

```
Design a Step Functions workflow for:

Process: [description]
Steps:
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

Requirements:
- Error handling: [retry strategy]
- Timeout: [max duration]
- Human approval: [yes/no, at which step]
- Parallel processing: [which steps]

Please provide:
1. State machine definition (ASL JSON)
2. Lambda functions for each task
3. Error handling and retry configuration
4. IAM policies
5. SAM/CDK template
```

### API Gateway Configuration

```
Configure API Gateway for:

Endpoints:
- [METHOD /path - description]
- [METHOD /path - description]

Requirements:
- Authentication: [Cognito/Lambda authorizer/API key]
- Rate limiting: [requests/second per client]
- Caching: [yes/no, TTL]
- CORS: [allowed origins]
- Request validation: [yes/no]

Please provide:
1. API Gateway configuration (OpenAPI or SAM)
2. Lambda authorizer code (if needed)
3. Request/response mapping
4. Throttling and quota settings
5. Custom domain setup
```

---

## Cold Start Optimization Prompts

### Cold Start Analysis

```
Analyze and optimize cold starts for this Lambda function:

Runtime: [Python/Node.js/Java/etc.]
Current cold start: [X ms]
Target cold start: [X ms]
Package size: [X MB]
Memory: [X MB]
VPC: [yes/no]

Dependencies:
[List main dependencies]

Please analyze:
1. Main contributors to cold start time
2. Quick wins (no code changes)
3. Code-level optimizations
4. Dependency optimization
5. Provisioned concurrency recommendation
6. SnapStart eligibility (if Java/.NET)
```

### Package Size Optimization

```
Optimize Lambda deployment package:

Current size: [X MB]
Runtime: [Python/Node.js/etc.]

Dependencies (from requirements.txt/package.json):
[list dependencies]

Please recommend:
1. Dependencies to remove or replace
2. Tree-shaking configuration
3. Layer strategy
4. Native dependency handling
5. Expected size reduction
```

---

## Cost Optimization Prompts

### Cost Analysis

```
Analyze serverless costs for:

Current monthly metrics:
- Invocations: [X]
- Average duration: [X ms]
- Memory: [X MB]
- Data transfer: [X GB]
- API Gateway requests: [X]
- DynamoDB reads/writes: [X/X]

Current monthly cost: [if known]

Please analyze:
1. Cost breakdown by service
2. Optimization opportunities
3. Right-sizing recommendations
4. Reserved capacity analysis
5. Architecture changes for cost reduction
6. Expected savings
```

### Cost Projection

```
Project serverless costs at scale:

Current state:
- Daily active users: [X]
- Requests per user: [X]
- Average function duration: [X ms]
- Memory per function: [X MB]

Growth projection:
- 3 months: [X users]
- 6 months: [X users]
- 12 months: [X users]

Please provide:
1. Cost projection chart
2. Cost per user analysis
3. Scaling inflection points
4. Cost optimization triggers
5. Budget planning recommendations
```

---

## Monitoring and Debugging Prompts

### Observability Setup

```
Set up observability for serverless application:

Services:
- [List Lambda functions]
- [DynamoDB tables]
- [API Gateway]
- [Step Functions]
- [Other services]

Requirements:
- Log retention: [X days]
- Metrics granularity: [1 min/5 min]
- Tracing: [sampling rate]
- Alert channels: [Slack/email/PagerDuty]

Please provide:
1. CloudWatch dashboard JSON
2. Essential alarms configuration
3. X-Ray/OpenTelemetry setup
4. Log Insights queries
5. Cost monitoring alerts
```

### Debugging Guide

```
Help debug this serverless issue:

Symptoms:
[Describe the problem - errors, latency, failures]

Relevant logs/traces:
[Paste relevant log snippets]

Architecture:
[Describe affected components]

Please help:
1. Identify likely root causes
2. Diagnostic steps to take
3. Log Insights queries to run
4. X-Ray analysis approach
5. Common fixes for this pattern
```

---

## Migration Prompts

### Monolith to Serverless

```
Plan migration from monolith to serverless:

Current application:
- Framework: [Django/Rails/Express/etc.]
- Database: [PostgreSQL/MySQL/etc.]
- Features: [list main features]
- Traffic: [requests/day]
- Team size: [X developers]

Constraints:
- Timeline: [X months]
- Budget: [if relevant]
- Downtime tolerance: [zero/minimal/scheduled]

Please provide:
1. Strangler fig pattern application
2. Phased migration plan
3. Database migration strategy
4. Feature prioritization for migration
5. Parallel running approach
6. Rollback strategy
```

### Container to Serverless

```
Evaluate migrating from containers to serverless:

Current setup:
- Container platform: [ECS/EKS/Fargate]
- Services: [list services]
- Requests/second: [X]
- Current monthly cost: [X]

Please analyze:
1. Migration feasibility per service
2. Services to keep as containers
3. Services suitable for Lambda
4. Estimated cost comparison
5. Migration approach
6. Hybrid architecture design
```

---

## Security Prompts

### Security Review

```
Review serverless security for:

Architecture:
[Describe components]

Current security measures:
- IAM: [describe]
- Encryption: [describe]
- Network: [VPC usage]
- Secrets: [management approach]

Please review:
1. IAM policy issues (over-permissive)
2. Data protection gaps
3. Input validation requirements
4. Dependency vulnerabilities approach
5. Secrets management improvements
6. Compliance gaps (if requirements specified)
```

### Least Privilege IAM

```
Create least-privilege IAM policy for:

Lambda function: [name/purpose]

AWS services accessed:
- DynamoDB: [table name, operations: get/put/query/etc.]
- S3: [bucket name, operations: get/put/delete]
- SQS: [queue name, operations]
- Secrets Manager: [secret ARN]
- [Other services]

Please provide:
1. Complete IAM policy JSON
2. Explanation of each permission
3. Condition keys for extra security
4. Resource-level restrictions
```

---

## Prompt Engineering Tips

### For Better Results

1. **Be specific about constraints**
   - Include limits (timeout, memory, cost)
   - Specify compliance requirements
   - Mention existing infrastructure

2. **Provide context**
   - Current architecture (if migrating)
   - Team experience level
   - Business criticality

3. **Ask for tradeoffs**
   - "What are the pros/cons of each approach?"
   - "What's the cost vs complexity tradeoff?"

4. **Request artifacts**
   - Ask for code, not just descriptions
   - Request IaC templates
   - Ask for test examples

5. **Iterate on responses**
   - "How would this change if traffic is 10x?"
   - "What if we need to support multiple regions?"

### Common Follow-up Questions

```
- How would this handle [failure scenario]?
- What's the cost at [X] scale?
- How do we monitor [specific aspect]?
- What's the rollback strategy?
- How do we test this locally?
- What security considerations am I missing?
```

### Verify LLM Outputs

Always verify:
- AWS service limits (may be outdated)
- Pricing (changes frequently)
- Service availability in your region
- IAM policy security implications
- Code correctness with actual testing

---

## Quick Reference Prompts

### Generate SAM Template

```
Generate AWS SAM template for:
- [X] Lambda functions with [runtime]
- API Gateway with [routes]
- DynamoDB table for [entities]
- Include proper IAM, logging, and tracing
```

### Generate Lambda Handler

```
Generate [Python/Node.js/Go] Lambda handler:
- Trigger: [type]
- Input: [schema]
- Logic: [description]
- Output: [schema]
- Include Powertools for logging/tracing
```

### Generate Step Functions

```
Generate Step Functions workflow:
- Steps: [1, 2, 3...]
- Error handling: [requirements]
- Include ASL definition and Lambda code
```

---

*Customize these prompts based on your specific requirements and context.*
