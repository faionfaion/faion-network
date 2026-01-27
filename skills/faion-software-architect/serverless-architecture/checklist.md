# Serverless Architecture Design Checklist

Step-by-step checklist for designing, implementing, and operating serverless applications.

## Phase 1: Requirements Analysis

### 1.1 Workload Characteristics

- [ ] **Traffic pattern analysis**
  - [ ] Identify peak load (requests/second)
  - [ ] Document traffic variability (spiky vs steady)
  - [ ] Map time-of-day/seasonal patterns
  - [ ] Estimate growth trajectory

- [ ] **Latency requirements**
  - [ ] Define acceptable p50/p95/p99 latency
  - [ ] Identify latency-critical paths
  - [ ] Document cold start tolerance
  - [ ] Consider geographic distribution needs

- [ ] **Execution characteristics**
  - [ ] Maximum expected execution time
  - [ ] Memory requirements per function
  - [ ] CPU-intensive vs I/O-bound workloads
  - [ ] Concurrent execution needs

### 1.2 Business Constraints

- [ ] **Cost model**
  - [ ] Define budget constraints
  - [ ] Calculate cost at expected scale
  - [ ] Model cost at 10x scale
  - [ ] Compare with container/VM alternatives

- [ ] **Compliance requirements**
  - [ ] Data residency requirements (regions)
  - [ ] Encryption requirements (at rest, in transit)
  - [ ] Audit logging requirements
  - [ ] Multi-tenancy isolation needs

- [ ] **Operational requirements**
  - [ ] SLA targets (availability %)
  - [ ] RTO/RPO for disaster recovery
  - [ ] On-call and incident response needs
  - [ ] Team serverless experience level

### 1.3 Serverless Fit Assessment

| Question | Yes = Serverless Fit | No = Consider Alternatives |
|----------|---------------------|---------------------------|
| Variable/unpredictable traffic? | Serverless ideal | Containers may be cheaper |
| Execution time < 15 minutes? | Lambda viable | Use Fargate/ECS |
| Latency spikes acceptable? | Standard Lambda | Provisioned concurrency or containers |
| Event-driven processing? | Serverless ideal | Consider always-on services |
| Rapid iteration needed? | Fast deployments | Works for any approach |

## Phase 2: Architecture Design

### 2.1 Function Design

- [ ] **Decomposition strategy**
  - [ ] Define bounded contexts
  - [ ] Map functions to business capabilities
  - [ ] Avoid nano-functions (too granular)
  - [ ] Avoid lambdaliths (too monolithic)
  - [ ] Target: 1 function = 1 responsibility

- [ ] **Function sizing**
  - [ ] Right-size memory allocation
  - [ ] Configure appropriate timeout
  - [ ] Plan for reserved concurrency (if needed)
  - [ ] Consider provisioned concurrency for critical paths

- [ ] **Handler design**
  - [ ] Separate business logic from handler
  - [ ] Initialize connections outside handler
  - [ ] Implement proper error handling
  - [ ] Return appropriate status codes

### 2.2 Event Architecture

- [ ] **Event source selection**
  | Source Type | Service | Use When |
  |-------------|---------|----------|
  | HTTP | API Gateway | REST/GraphQL APIs |
  | Queue | SQS | Buffering, retry needed |
  | Pub/Sub | SNS | Fan-out, multiple consumers |
  | Event Bus | EventBridge | Routing, filtering, SaaS integration |
  | Stream | Kinesis/DynamoDB Streams | Ordered processing, replay |
  | Storage | S3 | File uploads, batch processing |
  | Schedule | EventBridge Scheduler | Cron jobs |

- [ ] **Event patterns**
  - [ ] Define event schemas (CloudEvents or custom)
  - [ ] Plan for event versioning
  - [ ] Design for idempotency
  - [ ] Configure dead-letter queues (DLQ)

### 2.3 State Management

- [ ] **Statelessness verification**
  - [ ] No in-memory state between invocations
  - [ ] External storage for all persistent data
  - [ ] Session handling strategy defined

- [ ] **State storage selection**
  | State Type | Recommended Service | Notes |
  |------------|---------------------|-------|
  | User session | DynamoDB, Redis | TTL-based expiration |
  | Cache | ElastiCache, Momento | Consider Lambda extension |
  | Workflow state | Step Functions | Built-in state management |
  | Long-term data | DynamoDB, RDS | Match data model to DB type |
  | Files | S3 | Use pre-signed URLs |

### 2.4 Integration Patterns

- [ ] **Synchronous patterns**
  - [ ] API Gateway --> Lambda for request/response
  - [ ] Set appropriate timeouts
  - [ ] Implement circuit breakers for external calls
  - [ ] Use connection pooling (RDS Proxy)

- [ ] **Asynchronous patterns**
  - [ ] SQS for task queuing
  - [ ] SNS for fan-out
  - [ ] EventBridge for event routing
  - [ ] Step Functions for orchestration

- [ ] **Long-running processes**
  - [ ] Use Step Functions for workflows > 15 min
  - [ ] Consider Lambda Durable Functions (2025+)
  - [ ] Implement callback patterns for human approval
  - [ ] Design compensation logic for failures

### 2.5 API Design

- [ ] **API Gateway configuration**
  - [ ] Choose REST API vs HTTP API
  - [ ] Configure throttling limits
  - [ ] Enable caching where appropriate
  - [ ] Set up custom domain
  - [ ] Configure CORS

- [ ] **Authentication/Authorization**
  - [ ] Choose auth method (Cognito, Lambda authorizer, IAM)
  - [ ] Implement JWT validation
  - [ ] Define resource-based policies
  - [ ] Configure API keys for rate limiting

## Phase 3: Development Setup

### 3.1 Framework Selection

- [ ] **Choose IaC framework**
  | Criteria | AWS SAM | Serverless Framework | SST | CDK |
  |----------|---------|---------------------|-----|-----|
  | Simplicity | High | Medium | Medium | Low |
  | AWS-native | Yes | Plugin | Yes | Yes |
  | Multi-cloud | No | Yes | No | No |
  | Type safety | No | No | Yes | Yes |
  | Local dev | Good | Good | Excellent | Manual |
  | Ecosystem | AWS | Large | Growing | AWS |

- [ ] **Project structure**
  ```
  project/
  ├── src/
  │   ├── functions/
  │   │   ├── api/
  │   │   ├── events/
  │   │   └── scheduled/
  │   ├── lib/           # Shared code
  │   └── layers/        # Lambda layers
  ├── tests/
  │   ├── unit/
  │   └── integration/
  ├── template.yaml      # SAM
  ├── serverless.yml     # Serverless Framework
  └── sst.config.ts      # SST
  ```

### 3.2 Development Environment

- [ ] **Local development**
  - [ ] Set up SAM CLI or equivalent
  - [ ] Configure local DynamoDB
  - [ ] Set up LocalStack (optional)
  - [ ] Configure IDE/editor plugins

- [ ] **Dependencies**
  - [ ] Use Lambda layers for shared deps
  - [ ] Minimize package size (tree shaking)
  - [ ] Pin dependency versions
  - [ ] Exclude test/dev dependencies from deployment

### 3.3 Code Quality

- [ ] **Standards**
  - [ ] Linting configuration (ESLint, Ruff, etc.)
  - [ ] Type checking (TypeScript, mypy)
  - [ ] Code formatting (Prettier, Black)
  - [ ] Pre-commit hooks

- [ ] **Testing strategy**
  - [ ] Unit tests for business logic
  - [ ] Integration tests with local emulators
  - [ ] Contract tests for APIs
  - [ ] End-to-end tests in staging

## Phase 4: Security

### 4.1 IAM and Permissions

- [ ] **Least privilege**
  - [ ] Specific resource ARNs (not *)
  - [ ] Minimal action sets
  - [ ] Per-function IAM roles
  - [ ] Review with IAM Access Analyzer

- [ ] **IAM policy checklist**
  ```yaml
  # BAD: Overly permissive
  - Effect: Allow
    Action: dynamodb:*
    Resource: "*"

  # GOOD: Least privilege
  - Effect: Allow
    Action:
      - dynamodb:GetItem
      - dynamodb:PutItem
    Resource: !GetAtt MyTable.Arn
  ```

### 4.2 Secrets Management

- [ ] **Never hardcode secrets**
  - [ ] Use AWS Secrets Manager or Parameter Store
  - [ ] Rotate secrets automatically
  - [ ] Cache secrets in Lambda memory
  - [ ] Use environment variables for non-sensitive config

- [ ] **Environment variables**
  - [ ] Encrypt at rest (KMS)
  - [ ] Don't log sensitive values
  - [ ] Validate required vars at startup

### 4.3 Data Protection

- [ ] **Encryption**
  - [ ] Enable encryption at rest for all data stores
  - [ ] Use HTTPS for all API endpoints
  - [ ] Encrypt sensitive fields in DynamoDB
  - [ ] Use KMS customer-managed keys for compliance

- [ ] **Input validation**
  - [ ] Validate all input parameters
  - [ ] Sanitize data to prevent injection
  - [ ] Use API Gateway request validation
  - [ ] Implement rate limiting

### 4.4 Network Security

- [ ] **VPC considerations**
  - [ ] Only use VPC when required (adds cold start)
  - [ ] Use VPC endpoints for AWS services
  - [ ] Configure security groups
  - [ ] Enable VPC Flow Logs

## Phase 5: Observability

### 5.1 Logging

- [ ] **Structured logging**
  ```python
  # Use Powertools for AWS Lambda
  from aws_lambda_powertools import Logger
  logger = Logger()

  @logger.inject_lambda_context
  def handler(event, context):
      logger.info("Processing order", order_id=event['id'])
  ```

- [ ] **Log configuration**
  - [ ] Set appropriate log level per environment
  - [ ] Enable CloudWatch Log Insights
  - [ ] Configure log retention
  - [ ] Don't log sensitive data (PII, secrets)

### 5.2 Metrics

- [ ] **Essential metrics**
  | Metric | Source | Alert Threshold |
  |--------|--------|-----------------|
  | Invocations | CloudWatch | Baseline deviation |
  | Errors | CloudWatch | > 1% error rate |
  | Duration | CloudWatch | p95 > timeout/2 |
  | Throttles | CloudWatch | > 0 |
  | ConcurrentExecutions | CloudWatch | > 80% limit |
  | Cold starts | Custom/Insights | > 10% |
  | Cost | Cost Explorer | > budget |

- [ ] **Custom metrics**
  - [ ] Use CloudWatch EMF for custom metrics
  - [ ] Track business metrics (orders, signups)
  - [ ] Measure external API latencies
  - [ ] Monitor cache hit rates

### 5.3 Tracing

- [ ] **Distributed tracing setup**
  - [ ] Enable AWS X-Ray or ADOT
  - [ ] Instrument all Lambda functions
  - [ ] Add custom segments for business operations
  - [ ] Trace across service boundaries

- [ ] **OpenTelemetry (recommended)**
  - [ ] Add ADOT Lambda layer
  - [ ] Configure trace sampling
  - [ ] Export to preferred backend
  - [ ] Add custom attributes to spans

### 5.4 Alerting

- [ ] **Alert configuration**
  - [ ] Error rate alerts
  - [ ] Latency threshold alerts
  - [ ] Throttling alerts
  - [ ] Cost anomaly alerts
  - [ ] Business metric alerts

- [ ] **Runbook creation**
  - [ ] Document common failure modes
  - [ ] Create escalation procedures
  - [ ] Define on-call responsibilities

## Phase 6: Deployment

### 6.1 CI/CD Pipeline

- [ ] **Pipeline stages**
  ```
  Code --> Build --> Test --> Deploy Staging --> Integration Tests --> Deploy Prod
  ```

- [ ] **Deployment checklist**
  - [ ] Run unit tests
  - [ ] Run security scanning (SAST)
  - [ ] Run dependency vulnerability scan
  - [ ] Deploy to staging
  - [ ] Run integration tests
  - [ ] Deploy to production (canary/blue-green)
  - [ ] Run smoke tests
  - [ ] Monitor error rates

### 6.2 Deployment Strategies

- [ ] **Choose strategy**
  | Strategy | Risk | Rollback Speed | Use When |
  |----------|------|----------------|----------|
  | All-at-once | High | Fast | Dev/test |
  | Canary | Low | Medium | Production |
  | Linear | Low | Slow | Critical systems |
  | Blue/Green | Low | Fast | Zero downtime required |

- [ ] **Rollback plan**
  - [ ] Automated rollback on error threshold
  - [ ] Manual rollback procedure documented
  - [ ] Version aliases configured
  - [ ] Traffic shifting configured

### 6.3 Environment Management

- [ ] **Multi-environment setup**
  - [ ] Development environment
  - [ ] Staging environment (production-like)
  - [ ] Production environment
  - [ ] Consistent configuration management

- [ ] **Infrastructure as Code**
  - [ ] All resources defined in code
  - [ ] No manual console changes
  - [ ] Environment parity
  - [ ] Version controlled

## Phase 7: Operations

### 7.1 Performance Optimization

- [ ] **Cold start mitigation**
  - [ ] Analyzed cold start frequency
  - [ ] Implemented keep-warm (if needed)
  - [ ] Configured provisioned concurrency (if needed)
  - [ ] Enabled SnapStart (Java/.NET)
  - [ ] Optimized package size

- [ ] **Runtime optimization**
  - [ ] Right-sized memory
  - [ ] Used ARM architecture
  - [ ] Optimized database connections
  - [ ] Implemented caching

### 7.2 Cost Management

- [ ] **Cost monitoring**
  - [ ] Set up cost alerts
  - [ ] Track cost per function
  - [ ] Review monthly cost reports
  - [ ] Identify optimization opportunities

- [ ] **Cost optimization**
  - [ ] Switch to ARM/Graviton
  - [ ] Right-size memory allocation
  - [ ] Reduce execution duration
  - [ ] Consider Savings Plans for predictable usage
  - [ ] Evaluate Lambda Managed Instances (2025+)

### 7.3 Capacity Planning

- [ ] **Limits review**
  | Limit | Default | Action if Exceeded |
  |-------|---------|-------------------|
  | Concurrent executions | 1000 | Request increase |
  | Function timeout | 15 min | Use Step Functions |
  | /tmp storage | 10 GB | Use S3 or EFS |
  | Payload size | 6 MB sync | Use S3 for large payloads |
  | Deployment package | 250 MB | Use layers, optimize deps |

- [ ] **Scaling preparation**
  - [ ] Identified bottlenecks
  - [ ] Reserved concurrency for critical functions
  - [ ] Downstream services can handle scale
  - [ ] Database connection limits adequate

### 7.4 Disaster Recovery

- [ ] **Backup strategy**
  - [ ] DynamoDB point-in-time recovery enabled
  - [ ] S3 versioning enabled
  - [ ] Cross-region replication (if needed)
  - [ ] Infrastructure can be recreated from code

- [ ] **Multi-region (if required)**
  - [ ] Active-passive or active-active design
  - [ ] DNS failover configured
  - [ ] Data replication strategy
  - [ ] Recovery tested regularly

## Quick Reference: Decision Matrix

### Should I Use Serverless?

| Factor | Serverless | Containers | VMs |
|--------|------------|------------|-----|
| Variable traffic | Best | Good | Poor |
| Consistent high load | Poor | Best | Good |
| Cold start sensitive | Poor | Best | Good |
| Rapid development | Best | Good | Poor |
| Fine-grained control | Poor | Good | Best |
| Cost at low scale | Best | Good | Poor |
| Cost at high scale | Poor | Best | Good |

### Function Design Checklist

```
[ ] Single responsibility
[ ] Stateless execution
[ ] Idempotent operations
[ ] Proper error handling
[ ] Structured logging
[ ] Input validation
[ ] Appropriate timeout
[ ] Right-sized memory
[ ] External state storage
[ ] DLQ configured
```

---

*Use this checklist iteratively. Not all items apply to every project.*
