---
name: faion-aws-lambda-reference
description: AWS Lambda serverless compute - function design, cold starts, layers, event sources
version: 2.0.0
updated: 2026-01-26
---

# AWS Lambda

Serverless function management with focus on function design, cold start optimization, layers, and event sources.

## Overview

| Aspect | Description |
|--------|-------------|
| Service | AWS Lambda |
| Type | Serverless compute |
| Billing | Pay per invocation + duration (GB-seconds) |
| Memory | 128 MB - 10,240 MB |
| Timeout | Up to 15 minutes |
| Package Size | 50 MB (compressed), 250 MB (uncompressed) |

## Core Concepts

### Execution Model

```
Request → Cold Start (if needed) → INIT phase → INVOKE phase → Response
            ↓
    Execution environment reuse (warm start)
```

### Cold Start Phases

| Phase | Description | Optimization |
|-------|-------------|--------------|
| INIT | Download code, start runtime, run initialization | SnapStart, Provisioned Concurrency |
| INVOKE | Execute handler | Code optimization, memory tuning |
| SHUTDOWN | Clean up (optional) | Graceful shutdown handlers |

### Billing Model (2025+)

```
Cost = Requests + Duration (GB-seconds) + INIT phase (since Aug 2025)

GB-seconds = Allocated Memory (GB) x Execution Time (seconds)
```

**Important:** INIT phase now billed same as invocation duration (since August 2025).

## Function Design Principles

### Single Responsibility

```
Good:
- processOrder()      → handles order processing
- sendNotification()  → handles notifications
- generateReport()    → handles reports

Bad:
- doEverything()      → monolithic function
```

### Handler Structure

```python
# Initialize outside handler (reused across invocations)
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('my-table')

def handler(event, context):
    """
    Handler executes on each invocation.
    Keep it focused on business logic.
    """
    # Validate input
    if not validate(event):
        return error_response(400, "Invalid input")

    # Process
    result = process(event)

    # Return
    return success_response(result)
```

### Idempotency

Essential for reliable serverless systems:

```python
import hashlib
from datetime import datetime, timedelta

def handler(event, context):
    # Generate idempotency key
    idempotency_key = hashlib.sha256(
        f"{event['order_id']}:{event['timestamp']}".encode()
    ).hexdigest()

    # Check if already processed
    existing = get_from_cache(idempotency_key)
    if existing:
        return existing

    # Process and cache result
    result = process_order(event)
    cache_result(idempotency_key, result, ttl=timedelta(hours=24))

    return result
```

## Cold Start Optimization

### Optimization Strategies

| Strategy | Cold Start Reduction | Cost Impact | Best For |
|----------|---------------------|-------------|----------|
| SnapStart | 58-94% | Minimal | Java, Python, .NET |
| Provisioned Concurrency | ~100% | High ($$$) | Strict latency APIs |
| Memory Increase | Variable | Medium | CPU-bound functions |
| Graviton2 (ARM) | 10-20% | -20% cost | I/O-heavy workloads |
| Code Optimization | 20-50% | None | All functions |

### SnapStart

Available for Java 11+, Python, .NET 8:

```yaml
# SAM template
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      SnapStart:
        ApplyOn: PublishedVersions
```

**Important Considerations:**
- Snapshot expires after 14 days of inactivity
- Unique content (IDs, secrets) must be generated AFTER initialization
- Use CRaC hooks for advanced priming (Java)

### Provisioned Concurrency

Use sparingly - expensive:

```bash
# Configure provisioned concurrency
aws lambda put-provisioned-concurrency-config \
    --function-name my-function \
    --qualifier prod \
    --provisioned-concurrent-executions 10
```

**Cost Example:**
- 50 functions x 5 provisioned = ~$19,000/year
- vs. regular cold starts = ~$50/month

### Code-Level Optimization

```python
# GOOD: Initialize outside handler
import boto3
from aws_xray_sdk.core import patch_all

# SDK clients initialized once
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
patch_all()  # X-Ray tracing

# Connection pooling
http = urllib3.PoolManager(maxsize=10)

def handler(event, context):
    # Only business logic here
    return process(event)
```

## Lambda Layers

### When to Use

| Use Case | Recommendation |
|----------|----------------|
| Shared dependencies across functions | Yes |
| Large libraries (pandas, numpy) | Yes |
| Custom runtimes | Yes |
| Organization-wide utilities | Yes |
| Go/Rust functions | No (use static compilation) |

### Layer Structure

```
my-layer.zip
├── python/                    # Python runtime
│   └── my_package/
│       └── __init__.py
├── nodejs/                    # Node.js runtime
│   └── node_modules/
└── lib/                       # Shared libraries
```

### Limits

| Limit | Value |
|-------|-------|
| Layers per function | 5 |
| Compressed layer size | 50 MB |
| Uncompressed total (function + layers) | 250 MB |

### Version Management

```bash
# Publish new version
aws lambda publish-layer-version \
    --layer-name my-dependencies \
    --description "v1.2.0 - updated boto3" \
    --zip-file fileb://layer.zip \
    --compatible-runtimes python3.11 python3.12

# Update function to use new layer version
aws lambda update-function-configuration \
    --function-name my-function \
    --layers arn:aws:lambda:us-east-1:123456789012:layer:my-dependencies:5
```

## Event Sources

### Event Source Types

| Source | Invocation | Batching | Ordering |
|--------|------------|----------|----------|
| API Gateway | Sync | No | N/A |
| SQS | Async (polling) | Yes | FIFO only |
| Kinesis | Async (polling) | Yes | Per shard |
| DynamoDB Streams | Async (polling) | Yes | Per shard |
| SNS | Async | No | No |
| EventBridge | Async | No | No |
| S3 | Async | No | No |

### Batch Configuration

| Source | Default Batch | Max Batch | Batching Window |
|--------|---------------|-----------|-----------------|
| SQS (Standard) | 10 | 10,000 | 0-300s |
| SQS (FIFO) | 10 | 10 | 0-300s |
| Kinesis | 100 | 10,000 | 0-300s |
| DynamoDB Streams | 100 | 10,000 | 0-300s |

### Error Handling

```yaml
# CloudFormation/SAM
EventSourceMapping:
  Type: AWS::Lambda::EventSourceMapping
  Properties:
    FunctionName: !Ref MyFunction
    EventSourceArn: !GetAtt MyQueue.Arn
    BatchSize: 10
    MaximumBatchingWindowInSeconds: 5
    FunctionResponseTypes:
      - ReportBatchItemFailures
    DestinationConfig:
      OnFailure:
        Destination: !GetAtt DLQ.Arn
```

### Event Filtering

Reduce invocations by filtering at source:

```json
{
  "FilterCriteria": {
    "Filters": [
      {
        "Pattern": "{\"body\": {\"status\": [\"PENDING\", \"PROCESSING\"]}}"
      }
    ]
  }
}
```

## Performance Tuning

### Memory vs CPU

Memory allocation also scales CPU proportionally:

| Memory | vCPU | Use Case |
|--------|------|----------|
| 128 MB | 0.083 | Simple transformations |
| 512 MB | 0.33 | Light processing |
| 1,769 MB | 1 | Balanced workloads |
| 3,008 MB | 2 | CPU-intensive |
| 10,240 MB | 6 | Heavy computation |

### Power Tuning Tool

Use AWS Lambda Power Tuning to find optimal memory:

```bash
# Deploy power tuning state machine
sam deploy --guided --template-file aws-lambda-power-tuning.yaml

# Run tuning
aws stepfunctions start-execution \
    --state-machine-arn arn:aws:states:...:powerTuningStateMachine \
    --input '{"lambdaARN": "arn:aws:lambda:...:my-function", "powerValues": [128, 256, 512, 1024, 2048], "num": 50}'
```

## Deployment Patterns

### Blue-Green with Aliases

```bash
# 1. Deploy new version
aws lambda update-function-code --function-name my-func --zip-file fileb://new.zip
aws lambda publish-version --function-name my-func

# 2. Gradual traffic shift (10% to new)
aws lambda update-alias \
    --function-name my-func \
    --name prod \
    --routing-config '{"AdditionalVersionWeights": {"2": 0.1}}'

# 3. Monitor metrics, then complete shift
aws lambda update-alias \
    --function-name my-func \
    --name prod \
    --function-version 2
```

### Canary Deployment (CodeDeploy)

```yaml
# SAM template
DeploymentPreference:
  Type: Canary10Percent5Minutes
  Alarms:
    - !Ref ErrorAlarm
  Hooks:
    PreTraffic: !Ref PreTrafficHook
    PostTraffic: !Ref PostTrafficHook
```

## Monitoring

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Invocations | Total invocations | Anomaly detection |
| Duration | Execution time | > 80% of timeout |
| Errors | Failed invocations | > 1% error rate |
| Throttles | Rate-limited invocations | > 0 |
| ConcurrentExecutions | Parallel executions | > 80% of limit |
| IteratorAge | Stream processing lag | > 1 minute |

### Structured Logging (JSON)

```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(json.dumps({
        "event": "order_processed",
        "order_id": event["order_id"],
        "duration_ms": 150,
        "request_id": context.aws_request_id
    }))
```

## Security

### IAM Best Practices

- Least privilege: only permissions function needs
- Resource-based policies for cross-account
- No wildcards in production

### Environment Variables

```bash
# Encrypt sensitive values
aws lambda update-function-configuration \
    --function-name my-function \
    --kms-key-arn arn:aws:kms:...:key/... \
    --environment "Variables={DB_PASSWORD=encrypted_value}"
```

### VPC Considerations

- Use VPC only when necessary (adds cold start latency)
- Use VPC endpoints for AWS services
- Ensure sufficient ENI capacity

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | IaC templates |
| [llm-prompts.md](llm-prompts.md) | AI prompts for Lambda tasks |

## Sources

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)
- [Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
- [Event Source Mapping](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html)
- [AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)
- [Sedai Lambda Optimization](https://sedai.io/blog/best-tools-optimizing-aws-lambda)
- [Lambda Cold Start Optimization 2025](https://zircon.tech/blog/aws-lambda-cold-start-optimization-in-2025-what-actually-works/)
- [AWS Lambda Layers Best Practices](https://www.ranthebuilder.cloud/post/aws-lambda-layers-best-practices)

---

*AWS Lambda Reference v2.0.0 | Updated: 2026-01-26*
