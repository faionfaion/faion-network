# Serverless Architecture

Event-driven, auto-scaling compute without server management. Build applications that scale to zero and handle millions of requests.

## What is Serverless?

Serverless computing abstracts infrastructure management, allowing developers to focus on code. Key characteristics:

| Characteristic | Description |
|----------------|-------------|
| No server provisioning | Cloud provider manages all infrastructure |
| Pay per execution | Billed only for actual compute time (ms granularity) |
| Auto-scaling | Scales from zero to thousands of instances automatically |
| Event-driven | Functions triggered by events (HTTP, queue, schedule, etc.) |
| Stateless | Each invocation is independent; state stored externally |

```
Event --> Function --> Response
         (scales automatically, 0 to 1000+ instances)
```

## When to Use Serverless

### Ideal Use Cases

| Use Case | Why Serverless Fits |
|----------|---------------------|
| REST/GraphQL APIs | Auto-scaling, pay-per-request, easy deployment |
| Event processing | Native integration with queues, streams, storage |
| Webhooks | Handle spiky, unpredictable traffic |
| Scheduled jobs (cron) | No idle costs between executions |
| Image/video processing | Scale horizontally for parallel processing |
| Data transformations | ETL pipelines, real-time processing |
| MVPs and prototypes | Fast iteration, minimal ops overhead |
| Chatbots and AI | Burst traffic patterns, API integrations |
| IoT backends | Handle millions of device events |

### When NOT to Use Serverless

| Scenario | Why | Alternative |
|----------|-----|-------------|
| Long-running tasks (>15 min) | Lambda timeout limit | ECS/Fargate, Step Functions |
| Consistent high load | Cost inefficient at scale | Containers, EC2 |
| Low latency requirements (<50ms) | Cold starts add latency | Containers, keep-warm strategies |
| Complex stateful applications | Requires external state management | Kubernetes, traditional servers |
| GPU/specialized hardware | Limited instance types | EC2 with GPU, SageMaker |
| WebSockets (persistent) | Connection limits | API Gateway WebSocket, AppSync |
| Heavy compute (video encoding) | Memory/CPU limits, cost | EC2 Spot, dedicated instances |
| Compliance requiring control | Multi-tenancy concerns | Dedicated infrastructure |

## Serverless Providers and Services

### FaaS (Functions as a Service)

| Provider | Service | Max Timeout | Max Memory | Languages |
|----------|---------|-------------|------------|-----------|
| AWS | Lambda | 15 min | 10 GB | Node, Python, Go, Java, .NET, Ruby, Rust |
| Azure | Functions | Unlimited* | 14 GB | Node, Python, Java, .NET, PowerShell |
| GCP | Cloud Functions | 60 min (2nd gen) | 32 GB | Node, Python, Go, Java, .NET, Ruby, PHP |
| Cloudflare | Workers | 30s (CPU) | 128 MB | JS/TS, Rust, WASM |
| Vercel | Functions | 300s (Pro) | 3 GB | Node, Python, Go, Ruby |
| Netlify | Functions | 26s (sync) | 1 GB | Node, Go |

*Azure Durable Functions can run indefinitely

### Serverless Databases

| Database | Type | Best For | Pricing Model |
|----------|------|----------|---------------|
| DynamoDB | NoSQL (key-value) | High-scale APIs, AWS-native | Pay-per-request or provisioned |
| PlanetScale | MySQL (Vitess) | Web apps, schema branching | Rows read/written |
| Neon | PostgreSQL | Full SQL, branching | Compute time |
| Supabase | PostgreSQL | Full-stack, real-time | Compute + storage |
| Upstash | Redis | Caching, rate limiting | Requests |
| Fauna | Document | Multi-region, GraphQL | Reads/writes/compute |
| MongoDB Atlas | Document | Flexible schema | Instance-based |
| CockroachDB Serverless | Distributed SQL | Global distribution | Request units |
| Turso | SQLite (libSQL) | Edge, embedded | Rows read |

### Supporting Services

| Category | AWS | Azure | GCP |
|----------|-----|-------|-----|
| API Gateway | API Gateway, AppSync | API Management | Cloud Endpoints, Apigee |
| Event Bus | EventBridge | Event Grid | Eventarc |
| Message Queue | SQS | Service Bus | Cloud Tasks |
| Pub/Sub | SNS | Service Bus Topics | Pub/Sub |
| Workflow | Step Functions | Durable Functions | Workflows |
| Storage | S3 | Blob Storage | Cloud Storage |
| Auth | Cognito | Azure AD B2C | Firebase Auth |
| Secrets | Secrets Manager | Key Vault | Secret Manager |

## Development Frameworks Comparison

| Framework | Language | Provider | Best For | Learning Curve |
|-----------|----------|----------|----------|----------------|
| **AWS SAM** | YAML/JSON | AWS | AWS-native, simple projects | Low |
| **Serverless Framework** | YAML | Multi-cloud | Multi-provider, plugins | Medium |
| **SST** | TypeScript | AWS | Full-stack, DX focus | Medium |
| **AWS CDK** | TS/Python/Java | AWS | Complex infra, type safety | Medium-High |
| **Pulumi** | TS/Python/Go | Multi-cloud | Multi-provider, code-first | Medium |
| **Terraform** | HCL | Multi-cloud | Multi-provider, mature | Medium |
| **Architect** | YAML | AWS | Simplicity, conventions | Low |
| **Claudia.js** | JS | AWS | Node.js focused | Low |

### Framework Selection Guide

```
Need multi-cloud? --> Serverless Framework or Pulumi
AWS-only, simple? --> AWS SAM
AWS-only, complex? --> AWS CDK or SST
Full-stack TypeScript? --> SST
Need plugins/ecosystem? --> Serverless Framework
Infrastructure team? --> Terraform or CDK
```

## Core Architecture Patterns

### 1. API Backend Pattern

```
Client --> API Gateway --> Lambda --> DynamoDB
                |                        |
                +--> Lambda (Auth) <-----+
```

- API Gateway handles routing, throttling, caching
- Lambda functions per route or single "lambdalith"
- DynamoDB for data persistence

### 2. Event Processing Pattern

```
S3 Upload --> EventBridge --> Lambda --> Process --> Store Result
    |                            |
    +---- SNS (notify) <---------+
```

- Asynchronous processing triggered by events
- Fan-out to multiple processors via SNS/SQS

### 3. Saga/Orchestration Pattern (Step Functions)

```
API --> Step Functions --> Lambda A --> Lambda B --> Lambda C
              |                                         |
              +------- Compensating Transactions <------+
                       (on failure)
```

- Coordinates multi-step workflows
- Built-in retry, error handling, state management
- Human approval steps supported

### 4. Fan-Out/Fan-In Pattern

```
                    +--> SQS --> Lambda (worker 1) --+
Event --> SNS ------+--> SQS --> Lambda (worker 2) --+--> Aggregator
                    +--> SQS --> Lambda (worker 3) --+
```

- Parallel processing of tasks
- SQS provides buffering and retry

### 5. CQRS with Event Sourcing

```
Command --> Lambda --> EventBridge --> Event Store
                            |
                            +--> Lambda (projector) --> Read DB
                            +--> Lambda (projector) --> Search Index
```

- Separate read/write paths
- Event-driven projections

### 6. Edge Computing Pattern

```
User --> CloudFront --> Lambda@Edge --> Origin
              |
              +--> Cache
```

- Low-latency global distribution
- A/B testing, personalization at edge

## Cold Start Optimization

Cold starts occur when a new function instance is created. Impact varies by runtime:

| Runtime | Typical Cold Start | Optimization Priority |
|---------|-------------------|----------------------|
| Python | 200-500ms | Medium |
| Node.js | 100-300ms | Low |
| Go | 50-150ms | Low |
| Java | 1-5s | Critical |
| .NET | 500ms-2s | High |
| Rust | 50-150ms | Low |

### Optimization Techniques

| Technique | Effectiveness | Cost | Notes |
|-----------|---------------|------|-------|
| **Provisioned Concurrency** | Eliminates cold starts | $$$$ | Pay for always-on instances |
| **SnapStart (Java/.NET)** | ~90% reduction | Free | AWS Lambda only, Java 11+, .NET 8+ |
| **Keep-Warm Pings** | Moderate | $ | CloudWatch rule every 5 min |
| **Smaller packages** | 10-30% reduction | Free | Remove unused dependencies |
| **Init code outside handler** | 20-40% reduction | Free | Reuse connections |
| **Native compilation** | 50-80% reduction | Free | GraalVM, Native AOT |
| **Right-size memory** | Varies | $/savings | More memory = more CPU |
| **ARM/Graviton** | 10-20% faster | 20% cheaper | No code changes usually |

### Code-Level Best Practices

```python
# GOOD: Initialize outside handler (runs once per container)
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def handler(event, context):
    # Reuses existing connection
    return table.get_item(Key={'id': event['id']})
```

```python
# BAD: Initialize inside handler (runs every invocation)
def handler(event, context):
    import boto3  # Slow!
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('orders')
    return table.get_item(Key={'id': event['id']})
```

## Cost Optimization

### AWS Lambda Pricing Model (2025)

```
Cost = Requests + (Duration x Memory) + Data Transfer

- $0.20 per 1M requests
- $0.0000166667 per GB-second (x86)
- $0.0000133334 per GB-second (ARM) - 20% cheaper
```

### Cost Optimization Strategies

| Strategy | Potential Savings | Implementation |
|----------|-------------------|----------------|
| ARM/Graviton processors | 20% | Change architecture setting |
| Right-size memory | 10-50% | Use AWS Compute Optimizer |
| Reduce duration | Direct savings | Optimize code, connections |
| Batch processing | 30-70% | Process multiple items per invocation |
| Savings Plans | Up to 17% | Commit to consistent usage |
| Lambda Managed Instances | Up to 72% | For steady-state workloads (2025) |

### Cost Comparison: Serverless vs Containers

| Monthly Invocations | Duration | Memory | Lambda Cost | Fargate Cost |
|--------------------|----------|--------|-------------|--------------|
| 1M | 200ms | 256MB | ~$3 | ~$30 |
| 10M | 200ms | 512MB | ~$33 | ~$30 |
| 100M | 200ms | 512MB | ~$333 | ~$60 |

**Crossover point**: At ~10-30M requests/month with consistent load, containers become more cost-effective.

## Monitoring and Observability

### OpenTelemetry (Recommended for 2025+)

AWS now recommends OpenTelemetry over X-Ray SDKs:

```yaml
# SAM template with ADOT Layer
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Layers:
        - !Sub arn:aws:lambda:${AWS::Region}:901920570463:layer:aws-otel-python-amd64-ver-1-24-0:1
      Environment:
        Variables:
          AWS_LAMBDA_EXEC_WRAPPER: /opt/otel-handler
```

### Essential Metrics

| Metric | Alert Threshold | Why |
|--------|-----------------|-----|
| Error rate | > 1% | Indicates bugs or external failures |
| Duration p95 | > 3s | Latency affecting users |
| Throttles | > 0 | Hitting concurrency limits |
| Cold start rate | > 10% | Performance degradation |
| Cost per invocation | > baseline | Cost anomaly detection |

### Observability Stack Options

| Stack | Components | Best For |
|-------|------------|----------|
| AWS Native | CloudWatch, X-Ray, Lambda Insights | Simple, integrated |
| OpenTelemetry | ADOT, Prometheus, Grafana | Vendor-neutral |
| Third-party | Datadog, Lumigo, Epsagon | Rich features, easy setup |

## Anti-Patterns to Avoid

### 1. The Lambdalith

Stuffing entire application into one Lambda:
- Long deployment cycles
- Can't scale paths independently
- One failure affects everything

**Fix**: Split by domain/bounded context, not by HTTP verb.

### 2. Nano-Functions

Over-fragmenting into tiny functions:
- Debugging nightmare
- High latency (function-to-function calls)
- Lost business logic cohesion

**Fix**: Group by domain, use Step Functions for orchestration.

### 3. Synchronous Chains

```
Lambda A --> Lambda B --> Lambda C --> Lambda D
            (sync)       (sync)       (sync)
```

Problems: Latency compounds, timeouts cascade, hard to debug.

**Fix**: Use async patterns, event-driven, or Step Functions.

### 4. Ignoring Cold Starts

Assuming instant response for user-facing APIs causes latency spikes.

**Fix**: Provisioned concurrency, keep-warm, or accept for non-critical paths.

### 5. No Idempotency

Lambda can be invoked multiple times for the same event.

**Fix**: Use idempotency keys, DynamoDB conditional writes, or idempotency libraries.

## LLM-Assisted Design Tips

When using LLMs for serverless architecture:

### Effective Prompting

1. **Specify constraints**: Include timeout limits, memory constraints, expected load
2. **Define integration points**: List AWS services, external APIs
3. **Clarify state requirements**: Session, cache, long-term storage needs
4. **Include cost sensitivity**: Budget constraints, optimization priorities
5. **Mention compliance**: Data residency, encryption requirements

### What LLMs Excel At

- Generating SAM/CDK/SST templates from requirements
- Suggesting event-driven patterns for use cases
- Writing Lambda handler boilerplate
- Creating IAM policies with least privilege
- Reviewing architecture for anti-patterns
- Generating OpenTelemetry instrumentation code

### What to Verify

- Actual AWS limits and pricing (may be outdated)
- Service availability in your region
- Security implications of generated IAM policies
- Performance characteristics (test, don't assume)

## External Resources

### Official Documentation

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Azure Functions Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Google Cloud Functions](https://cloud.google.com/functions/docs)
- [AWS Well-Architected Serverless Lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/)

### Frameworks

- [AWS SAM](https://aws.amazon.com/serverless/sam/)
- [Serverless Framework](https://www.serverless.com/)
- [SST](https://sst.dev/)
- [AWS CDK](https://aws.amazon.com/cdk/)

### Learning Resources

- [Serverless Land (AWS)](https://serverlessland.com/)
- [AWS Compute Blog](https://aws.amazon.com/blogs/compute/)
- [Jeremy Daly's Serverless Blog](https://www.jeremydaly.com/)
- [Yan Cui's Blog](https://theburningmonk.com/)

### Tools

- [AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)
- [Powertools for AWS Lambda](https://docs.powertools.aws.dev/lambda/)
- [Lumigo CLI](https://github.com/lumigo-io/lumigo-CLI)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Methodologies

- [event-driven-architecture/](../event-driven-architecture/) - Event patterns, EventBridge, messaging
- [microservices-architecture/](../microservices-architecture/) - Service decomposition
- [cloud-architecture.md](../cloud-architecture.md) - Cloud context
- [database-selection/](../database-selection/) - Choosing databases

---

*Last updated: 2025-01*
