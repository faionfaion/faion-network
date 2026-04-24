# AWS Lambda LLM Prompts

Prompts for AI-assisted Lambda development and optimization.

## Function Design

### Create Lambda Handler

```
Create a production-ready AWS Lambda handler for [LANGUAGE: Python/Node.js/Java] that:

Purpose: [DESCRIBE FUNCTION PURPOSE]

Requirements:
- Initialize SDK clients outside handler for reuse
- Implement structured JSON logging
- Include proper error handling with appropriate status codes
- Add type hints/TypeScript types
- Make function idempotent using [idempotency key strategy]

Event source: [API Gateway / SQS / DynamoDB Streams / Kinesis / S3 / EventBridge]

Include:
1. Handler code with best practices
2. Example event payload
3. Required IAM permissions
```

### Review Lambda Function

```
Review this Lambda function for best practices:

```[CODE]```

Check for:
1. Cold start optimization (SDK/connection initialization)
2. Error handling completeness
3. Idempotency implementation
4. Logging quality (structured, appropriate level)
5. Security (no hardcoded secrets, least privilege)
6. Performance (async operations, connection reuse)
7. Resource cleanup

Provide specific recommendations with code examples.
```

### Optimize Cold Start

```
Analyze this Lambda function for cold start optimization:

Runtime: [RUNTIME]
Current cold start: [DURATION]
Memory: [SIZE]
VPC: [YES/NO]

Function code:
```[CODE]```

Recommend optimizations for:
1. Code-level changes (initialization, lazy loading)
2. Configuration changes (memory, architecture)
3. SnapStart applicability
4. Provisioned Concurrency cost-benefit
5. Layer optimization

Provide before/after examples.
```

## Event Source Configuration

### SQS Integration

```
Design SQS event source configuration for Lambda:

Use case: [DESCRIBE WORKLOAD]
Message rate: [MESSAGES/SECOND]
Processing time per message: [DURATION]
Latency requirement: [REAL-TIME / NEAR-REAL-TIME / BATCH]
Error tolerance: [DESCRIBE]

Provide:
1. Batch size recommendation
2. Batching window setting
3. Visibility timeout calculation
4. DLQ configuration
5. Event filtering pattern (if applicable)
6. Lambda handler with ReportBatchItemFailures
7. CloudFormation/SAM template
```

### DynamoDB Streams Integration

```
Design DynamoDB Streams processing with Lambda:

Table operations: [INSERT/MODIFY/REMOVE - which to process]
Expected throughput: [WRITES/SECOND]
Processing requirements: [DESCRIBE]
Ordering requirements: [STRICT / RELAXED]

Provide:
1. Stream configuration (view type)
2. Event source mapping settings
3. Parallelization factor recommendation
4. Error handling strategy (bisect, retry, DLQ)
5. Lambda handler code with batch item failures
6. Terraform/SAM template
```

### Kinesis Integration

```
Design Kinesis stream processing with Lambda:

Stream: [SHARD COUNT]
Records per second: [RATE]
Record size: [AVERAGE SIZE]
Processing latency requirement: [SLA]
Ordering: [REQUIRED / NOT REQUIRED]

Provide:
1. Batch size optimization
2. Parallelization factor setting
3. Starting position strategy
4. Error handling configuration
5. Tumbling window (if aggregation needed)
6. Lambda handler with checkpointing logic
```

## Layer Management

### Create Layer

```
Create an AWS Lambda layer for:

Runtime: [PYTHON/NODEJS]
Dependencies: [LIST PACKAGES WITH VERSIONS]
Architecture: [x86_64 / arm64 / both]

Provide:
1. Directory structure
2. Build script (bash)
3. Requirements file / package.json
4. Size optimization tips
5. Publish command
6. Version management strategy
```

### Optimize Layer Size

```
Analyze and optimize this Lambda layer:

Current size: [SIZE]
Contents: [DESCRIBE OR LIST]
Runtime: [RUNTIME]

Provide:
1. Size analysis by component
2. Unnecessary file identification
3. Alternative lighter packages
4. Build optimization commands
5. Target size recommendation
```

## Deployment

### Blue-Green Deployment

```
Create a blue-green deployment strategy for Lambda:

Function: [NAME]
Current traffic: [REQUESTS/SECOND]
Rollback requirement: [INSTANT / WITHIN X MINUTES]
Monitoring: [CLOUDWATCH / CUSTOM]

Provide:
1. Version publishing workflow
2. Alias configuration
3. Traffic shifting strategy (percentage, duration)
4. Rollback triggers and automation
5. Monitoring queries for canary metrics
6. Shell script or GitHub Actions workflow
```

### CI/CD Pipeline

```
Create CI/CD pipeline for Lambda deployment:

Source: [GITHUB / GITLAB / CODECOMMIT]
Language: [RUNTIME]
Environments: [LIST: dev, staging, prod]
Testing requirements: [UNIT / INTEGRATION / E2E]
Approval: [MANUAL FOR PROD / AUTOMATIC]

Provide:
1. Pipeline definition (GitHub Actions / GitLab CI)
2. Build stage (install, test, package)
3. Deploy stage per environment
4. Deployment verification
5. Rollback procedure
6. SAM/Serverless Framework configuration
```

## Performance Tuning

### Memory Optimization

```
Recommend optimal memory for this Lambda function:

Current configuration:
- Memory: [SIZE]
- Average duration: [MS]
- P99 duration: [MS]
- CPU-bound: [YES/NO]
- I/O-bound: [YES/NO]

Workload characteristics:
- [DESCRIBE PROCESSING]

Provide:
1. Power Tuning execution plan
2. Expected cost/performance tradeoffs
3. Recommended memory setting with justification
4. Architecture recommendation (x86 vs ARM)
```

### Concurrency Planning

```
Plan Lambda concurrency for:

Expected traffic pattern: [STEADY / SPIKY / SCHEDULED]
Peak requests per second: [NUMBER]
Function duration: [AVERAGE MS]
Cold start tolerance: [ACCEPTABLE / MINIMIZE]
Budget constraint: [AMOUNT / NONE]

Calculate and provide:
1. Required concurrency limit
2. Reserved concurrency recommendation
3. Provisioned concurrency cost analysis
4. Burst handling strategy
5. Throttling mitigation plan
```

## Monitoring & Observability

### CloudWatch Dashboard

```
Create CloudWatch dashboard for Lambda monitoring:

Functions to monitor: [LIST]
Critical metrics: [LIST: duration, errors, throttles, etc.]
Business metrics: [LIST]
Alert thresholds: [DESCRIBE]

Provide:
1. Dashboard JSON definition
2. Key metric widgets
3. Alarm configurations
4. Log Insights queries for:
   - Error investigation
   - Cold start analysis
   - Performance trends
5. Anomaly detection setup
```

### Troubleshooting Guide

```
Create troubleshooting runbook for Lambda issues:

Function: [NAME/DESCRIPTION]
Common issues: [LIST KNOWN ISSUES]
SLO: [LATENCY AND ERROR RATE TARGETS]

Include diagnostic steps for:
1. High error rate
2. Increased latency
3. Throttling
4. Memory issues
5. Timeout issues
6. Cold start spikes

With specific CloudWatch queries and resolution steps.
```

## Security

### IAM Policy

```
Create least-privilege IAM policy for Lambda:

Function purpose: [DESCRIBE]
AWS services accessed:
- [SERVICE 1]: [OPERATIONS]
- [SERVICE 2]: [OPERATIONS]

Resources:
- [SPECIFIC ARNs OR PATTERNS]

Provide:
1. IAM policy JSON
2. Trust policy for execution role
3. Resource-based policy (if needed)
4. Explanation of each permission
5. Security review checklist
```

### Security Audit

```
Perform security audit on Lambda configuration:

Function ARN: [ARN]
VPC: [YES/NO]
Environment variables: [LIST]
Triggers: [LIST]
Downstream services: [LIST]

Audit for:
1. IAM permissions (over-privileged?)
2. Environment variable encryption
3. VPC security group rules
4. Function URL security
5. Secrets management
6. Input validation
7. Dependency vulnerabilities

Provide findings and remediation steps.
```

## Cost Optimization

### Cost Analysis

```
Analyze Lambda cost for:

Monthly invocations: [NUMBER]
Average duration: [MS]
Memory: [SIZE]
Architecture: [x86_64 / arm64]
Provisioned concurrency: [YES/NO, AMOUNT]

Calculate:
1. Current monthly cost breakdown
2. Cost optimization opportunities
3. Memory optimization savings
4. ARM migration savings
5. Provisioned concurrency ROI
6. Reserved capacity recommendations
```

### Cost Reduction Plan

```
Create cost reduction plan for Lambda workload:

Current monthly spend: [AMOUNT]
Functions: [COUNT]
Top cost contributors: [LIST]

Analyze and recommend:
1. Right-sizing opportunities
2. Architecture changes (x86 to ARM)
3. Code optimization impact
4. Provisioned concurrency review
5. Event filtering opportunities
6. Tiered storage for logs
7. Implementation priority (ROI-based)
```

## Migration

### Container to Lambda

```
Migrate containerized application to Lambda:

Current setup:
- Image size: [SIZE]
- Memory: [CONTAINER MEMORY]
- Startup time: [DURATION]
- Request handling: [SYNC/ASYNC]

Application details:
- Language: [RUNTIME]
- Dependencies: [LIST]
- External services: [LIST]

Provide:
1. Migration feasibility assessment
2. Architecture changes needed
3. Handler adaptation strategy
4. Layer packaging for dependencies
5. Testing approach
6. Rollback plan
```

### Monolith to Lambda

```
Decompose monolithic function into multiple Lambdas:

Current function:
- Lines of code: [COUNT]
- Responsibilities: [LIST]
- Execution paths: [DESCRIBE]
- Average duration: [MS]

Provide:
1. Function decomposition strategy
2. Communication patterns (sync/async)
3. Shared code/layer strategy
4. State management approach
5. Migration steps (incremental)
6. Testing strategy
```

---

*AWS Lambda LLM Prompts | Use with [README.md](README.md)*
