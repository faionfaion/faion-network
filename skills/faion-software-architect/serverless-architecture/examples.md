# Serverless Architecture Examples

Real-world serverless architectures for common use cases.

## Example 1: E-Commerce API

### Requirements

- REST API for product catalog, cart, orders
- 10K-100K daily active users
- Peak traffic during sales events (10x normal)
- Sub-second response times
- Payment processing integration

### Architecture

```
                                 ┌─────────────────┐
                                 │   CloudFront    │
                                 │   (CDN/Cache)   │
                                 └────────┬────────┘
                                          │
                                 ┌────────▼────────┐
                                 │   API Gateway   │
                                 │  (REST API)     │
                                 └────────┬────────┘
                                          │
          ┌───────────────────────────────┼───────────────────────────────┐
          │                               │                               │
   ┌──────▼──────┐                ┌───────▼───────┐              ┌───────▼───────┐
   │   Lambda    │                │    Lambda     │              │    Lambda     │
   │  Products   │                │     Cart      │              │    Orders     │
   └──────┬──────┘                └───────┬───────┘              └───────┬───────┘
          │                               │                               │
   ┌──────▼──────┐                ┌───────▼───────┐              ┌───────▼───────┐
   │  DynamoDB   │                │  DynamoDB     │              │  DynamoDB     │
   │  Products   │                │   Sessions    │              │    Orders     │
   └─────────────┘                └───────────────┘              └───────┬───────┘
                                                                         │
                                                                ┌────────▼────────┐
                                                                │   EventBridge   │
                                                                └────────┬────────┘
                                                    ┌────────────────────┼────────────────────┐
                                                    │                    │                    │
                                             ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
                                             │   Lambda    │      │   Lambda    │      │   Lambda    │
                                             │  Inventory  │      │  Payments   │      │   Email     │
                                             └─────────────┘      └──────┬──────┘      └─────────────┘
                                                                         │
                                                                  ┌──────▼──────┐
                                                                  │   Stripe    │
                                                                  │   (ext)     │
                                                                  └─────────────┘
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Database | DynamoDB | Auto-scaling, pay-per-request, single-digit ms latency |
| Event Bus | EventBridge | Decouple order processing from API response |
| Payments | Async via SQS | Don't block API response, retry on failure |
| Caching | CloudFront + DAX | Reduce DynamoDB reads for product catalog |
| Auth | Cognito | Managed auth, JWT tokens |

### DynamoDB Single-Table Design

```
PK                    SK                      Type        Data
-----------------------------------------------------------------
PRODUCT#123          METADATA                Product     {name, price, stock}
PRODUCT#123          CATEGORY#electronics    Category    {category_name}
USER#456             PROFILE                 User        {email, name}
USER#456             CART                    Cart        {items: [...]}
ORDER#789            METADATA                Order       {status, total}
ORDER#789            ITEM#1                  OrderItem   {product_id, qty}
```

### Cost Estimate (Monthly)

| Component | Usage | Cost |
|-----------|-------|------|
| Lambda | 5M invocations, 200ms avg | ~$10 |
| API Gateway | 5M requests | ~$17 |
| DynamoDB | 100M read, 10M write | ~$40 |
| CloudFront | 100GB transfer | ~$9 |
| **Total** | | **~$76** |

---

## Example 2: Real-Time Data Pipeline

### Requirements

- Ingest 10K events/second from IoT devices
- Real-time aggregations (1-minute windows)
- Store raw data for analytics
- Alert on anomalies
- Dashboard for monitoring

### Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐
│ IoT Devices │───▶│  Kinesis    │───▶│      Lambda         │
│   (10K/s)   │    │  Data       │    │  (Transform/Filter) │
└─────────────┘    │  Streams    │    └──────────┬──────────┘
                   └─────────────┘               │
                                                 │
                   ┌─────────────────────────────┼─────────────────────────────┐
                   │                             │                             │
            ┌──────▼──────┐               ┌──────▼──────┐               ┌──────▼──────┐
            │   Kinesis   │               │   Lambda    │               │  Kinesis    │
            │  Firehose   │               │ Aggregator  │               │  Analytics  │
            └──────┬──────┘               └──────┬──────┘               └──────┬──────┘
                   │                             │                             │
            ┌──────▼──────┐               ┌──────▼──────┐               ┌──────▼──────┐
            │     S3      │               │  Timestream │               │  Dashboard  │
            │  (Raw Data) │               │  (Metrics)  │               │  (Grafana)  │
            └─────────────┘               └──────┬──────┘               └─────────────┘
                                                 │
                                          ┌──────▼──────┐
                                          │ EventBridge │
                                          └──────┬──────┘
                                                 │
                                          ┌──────▼──────┐
                                          │   Lambda    │
                                          │  (Alerting) │
                                          └──────┬──────┘
                                                 │
                                          ┌──────▼──────┐
                                          │    SNS      │
                                          │ (PagerDuty) │
                                          └─────────────┘
```

### Lambda Configuration

```yaml
# Kinesis trigger with batching
Resources:
  ProcessStreamFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: handler.process
      Runtime: python3.11
      MemorySize: 1024
      Timeout: 60
      Events:
        KinesisEvent:
          Type: Kinesis
          Properties:
            Stream: !GetAtt DataStream.Arn
            StartingPosition: LATEST
            BatchSize: 1000
            MaximumBatchingWindowInSeconds: 5
            ParallelizationFactor: 10
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Ingestion | Kinesis Data Streams | High throughput, ordered processing |
| Raw Storage | S3 via Firehose | Cost-effective, query with Athena |
| Time-series | Timestream | Purpose-built, auto-scaling |
| Alerting | EventBridge + Lambda | Flexible rules, easy to extend |
| Analytics | Kinesis Analytics | Real-time SQL queries |

### Cost Estimate (Monthly)

| Component | Usage | Cost |
|-----------|-------|------|
| Kinesis Streams | 2 shards | ~$30 |
| Lambda | 26M invocations | ~$100 |
| Kinesis Firehose | 25TB ingested | ~$200 |
| S3 | 25TB storage | ~$575 |
| Timestream | 1TB writes, 5TB storage | ~$400 |
| **Total** | | **~$1,305** |

---

## Example 3: SaaS Multi-Tenant Application

### Requirements

- B2B SaaS with 1000+ tenants
- Tenant isolation (data and compute)
- Per-tenant billing
- Admin dashboard
- API rate limiting per tenant

### Architecture

```
                              ┌─────────────────┐
                              │    Route 53     │
                              │   (DNS + Health)│
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │    CloudFront   │
                              └────────┬────────┘
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
           ┌────────▼────────┐  ┌──────▼──────┐  ┌───────▼───────┐
           │   S3 (Static)   │  │ API Gateway │  │  AppSync      │
           │   React SPA     │  │  REST API   │  │  GraphQL      │
           └─────────────────┘  └──────┬──────┘  └───────┬───────┘
                                       │                  │
                              ┌────────▼────────┐         │
                              │ Lambda Authorizer│         │
                              │ (JWT + Tenant)  │         │
                              └────────┬────────┘         │
                                       │                  │
                    ┌──────────────────┼──────────────────┤
                    │                  │                  │
           ┌────────▼────────┐  ┌──────▼──────┐  ┌───────▼───────┐
           │     Lambda      │  │   Lambda    │  │    Lambda     │
           │   Core API      │  │  Webhooks   │  │   Real-time   │
           └────────┬────────┘  └──────┬──────┘  └───────┬───────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                              ┌────────▼────────┐
                              │    DynamoDB     │
                              │ (Single-Table)  │
                              │ PK: TENANT#xxx  │
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │   EventBridge   │
                              └────────┬────────┘
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
           ┌────────▼────────┐  ┌──────▼──────┐  ┌───────▼───────┐
           │     Lambda      │  │   Lambda    │  │    Lambda     │
           │    Billing      │  │  Analytics  │  │   Audit Log   │
           └────────┬────────┘  └─────────────┘  └───────┬───────┘
                    │                                     │
           ┌────────▼────────┐                   ┌───────▼───────┐
           │     Stripe      │                   │  CloudWatch   │
           │                 │                   │     Logs      │
           └─────────────────┘                   └───────────────┘
```

### Tenant Isolation Strategy

```python
# Lambda Authorizer for tenant context
def authorize(event, context):
    token = event['authorizationToken']
    claims = verify_jwt(token)

    tenant_id = claims['tenant_id']
    user_id = claims['sub']

    # Generate policy with tenant context
    return {
        'principalId': user_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Allow',
                'Resource': event['methodArn']
            }]
        },
        'context': {
            'tenant_id': tenant_id,  # Passed to Lambda
            'tier': claims['tier']
        }
    }
```

### DynamoDB Access Pattern

```python
# All queries scoped to tenant
def get_projects(tenant_id: str):
    return table.query(
        KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
        ExpressionAttributeValues={
            ':pk': f'TENANT#{tenant_id}',
            ':sk': 'PROJECT#'
        }
    )
```

### Rate Limiting by Tier

```yaml
# API Gateway Usage Plans
Resources:
  FreeTierUsagePlan:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      Throttle:
        RateLimit: 10
        BurstLimit: 20
      Quota:
        Limit: 1000
        Period: DAY

  ProTierUsagePlan:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      Throttle:
        RateLimit: 100
        BurstLimit: 200
      Quota:
        Limit: 100000
        Period: DAY
```

---

## Example 4: AI/ML Inference API

### Requirements

- Serve ML model predictions via API
- Handle variable load (10-10K requests/min)
- Low latency (<500ms p95)
- A/B testing for model versions
- Cost-efficient at low utilization

### Architecture

```
                              ┌─────────────────┐
                              │   API Gateway   │
                              │   (HTTP API)    │
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │     Lambda      │
                              │   (Routing)     │
                              └────────┬────────┘
                    ┌──────────────────┼──────────────────┐
                    │ 90%              │ 10%              │
           ┌────────▼────────┐  ┌──────▼──────────────────▼───────┐
           │     Lambda      │  │          Lambda                 │
           │   Model v1      │  │        Model v2 (test)          │
           │  (Provisioned)  │  │                                 │
           └────────┬────────┘  └──────────────────┬──────────────┘
                    │                              │
                    └──────────────────┬───────────┘
                                       │
                              ┌────────▼────────┐
                              │       S3        │
                              │  (Model Files)  │
                              └─────────────────┘

    ┌───────────────────────────────────────────────────────────────────┐
    │                    Async Training Pipeline                         │
    │                                                                   │
    │  S3 (Data) --> Step Functions --> SageMaker --> S3 (Model) --> Lambda Deploy
    └───────────────────────────────────────────────────────────────────┘
```

### Lambda with ML Model

```python
# Load model outside handler (cached)
import onnxruntime as ort
import boto3
import os

# Download and cache model on cold start
model_path = '/tmp/model.onnx'
if not os.path.exists(model_path):
    s3 = boto3.client('s3')
    s3.download_file('ml-models-bucket', 'model-v1.onnx', model_path)

session = ort.InferenceSession(model_path)

def handler(event, context):
    input_data = preprocess(event['body'])

    result = session.run(
        ['output'],
        {'input': input_data}
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': result[0].tolist()})
    }
```

### Configuration for Low Latency

```yaml
Resources:
  InferenceFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: inference.handler
      Runtime: python3.11
      MemorySize: 3008  # More memory = more CPU
      Timeout: 30
      Architectures:
        - arm64  # 20% cheaper, often faster for ML
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: 5  # Keep warm
      Layers:
        - !Ref ONNXRuntimeLayer
      Environment:
        Variables:
          MODEL_VERSION: v1
```

### A/B Testing with Weighted Routing

```yaml
# API Gateway with Lambda aliases
Resources:
  ApiStage:
    Type: AWS::ApiGateway::Stage
    Properties:
      StageName: prod
      CanarySettings:
        PercentTraffic: 10
        StageVariableOverrides:
          MODEL_ALIAS: canary
        UseStageCache: false
```

---

## Example 5: Document Processing Pipeline

### Requirements

- Process uploaded documents (PDF, images)
- Extract text (OCR), classify, summarize
- Handle 1K-10K documents/day
- Long processing times (2-5 min per doc)
- Notify users when complete

### Architecture

```
┌─────────────┐       ┌─────────────┐       ┌─────────────────────────┐
│   Client    │──────▶│ API Gateway │──────▶│        Lambda           │
│             │       │             │       │   (Upload Handler)      │
└─────────────┘       └─────────────┘       └───────────┬─────────────┘
                                                        │
                                            ┌───────────▼───────────┐
                                            │          S3           │
                                            │   (Document Upload)   │
                                            └───────────┬───────────┘
                                                        │ (S3 Event)
                                            ┌───────────▼───────────┐
                                            │     Step Functions    │
                                            │  (Document Pipeline)  │
                                            └───────────┬───────────┘
                                                        │
                    ┌───────────────────────────────────┼───────────────────────────────────┐
                    │                                   │                                   │
         ┌──────────▼──────────┐             ┌─────────▼─────────┐             ┌──────────▼──────────┐
         │       Lambda        │             │      Lambda       │             │       Lambda        │
         │    Text Extract     │             │    Classify       │             │     Summarize       │
         │   (Textract/OCR)    │             │   (Comprehend)    │             │    (Bedrock)        │
         └──────────┬──────────┘             └─────────┬─────────┘             └──────────┬──────────┘
                    │                                   │                                   │
                    └───────────────────────────────────┼───────────────────────────────────┘
                                                        │
                                            ┌───────────▼───────────┐
                                            │       Lambda          │
                                            │   Store Results       │
                                            └───────────┬───────────┘
                                                        │
                    ┌───────────────────────────────────┼───────────────────────────────────┐
                    │                                   │                                   │
         ┌──────────▼──────────┐             ┌─────────▼─────────┐             ┌──────────▼──────────┐
         │      DynamoDB       │             │    OpenSearch     │             │         S3          │
         │     (Metadata)      │             │   (Full-text)     │             │    (Processed)      │
         └─────────────────────┘             └───────────────────┘             └─────────────────────┘
                                                        │
                                            ┌───────────▼───────────┐
                                            │      EventBridge      │
                                            └───────────┬───────────┘
                                                        │
                                            ┌───────────▼───────────┐
                                            │        Lambda         │
                                            │   Send Notification   │
                                            └───────────┬───────────┘
                                            ┌───────────┼───────────┐
                                            │           │           │
                                     ┌──────▼───┐ ┌─────▼────┐ ┌────▼─────┐
                                     │   SES    │ │   SNS    │ │ WebSocket│
                                     │ (Email)  │ │  (Push)  │ │ (App)    │
                                     └──────────┘ └──────────┘ └──────────┘
```

### Step Functions Definition

```json
{
  "Comment": "Document Processing Pipeline",
  "StartAt": "ExtractText",
  "States": {
    "ExtractText": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789:function:ExtractText",
      "Next": "ParallelProcessing",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "HandleError"
      }]
    },
    "ParallelProcessing": {
      "Type": "Parallel",
      "Next": "StoreResults",
      "Branches": [
        {
          "StartAt": "Classify",
          "States": {
            "Classify": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:123456789:function:Classify",
              "End": true
            }
          }
        },
        {
          "StartAt": "Summarize",
          "States": {
            "Summarize": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:123456789:function:Summarize",
              "End": true
            }
          }
        }
      ]
    },
    "StoreResults": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789:function:StoreResults",
      "Next": "NotifyUser"
    },
    "NotifyUser": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789:function:NotifyUser",
      "End": true
    },
    "HandleError": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789:function:HandleError",
      "End": true
    }
  }
}
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Orchestration | Step Functions | Built-in retry, state management, visualization |
| OCR | Textract | Managed, handles complex layouts |
| Classification | Comprehend | Custom classifier training |
| Summarization | Bedrock | State-of-the-art LLM summaries |
| Search | OpenSearch Serverless | Full-text search, auto-scaling |

---

## Example 6: Scheduled Data Sync

### Requirements

- Sync data from external API every hour
- Handle pagination (1000s of records)
- Retry on failure
- Track sync status
- Alert on failures

### Architecture

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   EventBridge   │──────▶│ Step Functions  │──────▶│     Lambda      │
│  Scheduler      │       │ (Sync Workflow) │       │  Fetch Page     │
│  (hourly)       │       └────────┬────────┘       └────────┬────────┘
└─────────────────┘                │                         │
                                   │                         ▼
                                   │                ┌─────────────────┐
                                   │                │  External API   │
                                   │                └─────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
             ┌──────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
             │   Lambda    │ │  Lambda  │ │   Lambda    │
             │  Transform  │ │  Store   │ │  Complete   │
             └─────────────┘ └────┬─────┘ └──────┬──────┘
                                  │              │
                           ┌──────▼──────┐ ┌─────▼──────┐
                           │  DynamoDB   │ │ CloudWatch │
                           │             │ │  Metrics   │
                           └─────────────┘ └────────────┘
```

### Step Functions for Pagination

```json
{
  "Comment": "Paginated Data Sync",
  "StartAt": "InitializeSync",
  "States": {
    "InitializeSync": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:InitSync",
      "Next": "FetchPage"
    },
    "FetchPage": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:FetchPage",
      "Next": "ProcessRecords",
      "Retry": [{
        "ErrorEquals": ["RetryableError"],
        "IntervalSeconds": 5,
        "MaxAttempts": 3,
        "BackoffRate": 2
      }]
    },
    "ProcessRecords": {
      "Type": "Map",
      "ItemsPath": "$.records",
      "MaxConcurrency": 10,
      "Iterator": {
        "StartAt": "Transform",
        "States": {
          "Transform": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:...:Transform",
            "Next": "Store"
          },
          "Store": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:...:Store",
            "End": true
          }
        }
      },
      "Next": "CheckMorePages"
    },
    "CheckMorePages": {
      "Type": "Choice",
      "Choices": [{
        "Variable": "$.nextPageToken",
        "IsPresent": true,
        "Next": "FetchPage"
      }],
      "Default": "CompleteSync"
    },
    "CompleteSync": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:Complete",
      "End": true
    }
  }
}
```

---

## Anti-Pattern Examples

### Anti-Pattern 1: Synchronous Chain (Bad)

```
# DON'T DO THIS
Lambda A --sync--> Lambda B --sync--> Lambda C --sync--> Lambda D

Problems:
- Latency compounds: 100ms + 100ms + 100ms + 100ms = 400ms+
- Timeout risk: If Lambda A timeout is 30s, chain can timeout
- Error handling: Failures cascade unpredictably
- Cost: Paying for Lambda A to wait for B, C, D
```

**Fix**: Use Step Functions or async patterns.

### Anti-Pattern 2: The Lambdalith (Bad)

```python
# DON'T DO THIS - One Lambda handling everything
def handler(event, context):
    path = event['path']
    method = event['httpMethod']

    if path == '/users' and method == 'GET':
        return get_users()
    elif path == '/users' and method == 'POST':
        return create_user(event['body'])
    elif path == '/orders' and method == 'GET':
        return get_orders()
    elif path == '/orders' and method == 'POST':
        return create_order(event['body'])
    # ... 50 more routes
```

Problems:
- Can't scale routes independently
- All routes need same permissions
- One bug affects everything
- Slow deployments

**Fix**: Split by domain (users, orders) or use API Gateway routing.

### Anti-Pattern 3: No Idempotency (Bad)

```python
# DON'T DO THIS
def handler(event, context):
    order = event['order']
    charge_payment(order['amount'])  # May be called twice!
    send_confirmation(order['email'])
    save_order(order)
```

**Fix**: Use idempotency keys.

```python
from aws_lambda_powertools.utilities.idempotency import idempotent

@idempotent(persistence_store=DynamoDBPersistenceLayer(table_name='IdempotencyTable'))
def handler(event, context):
    # Now safe from duplicate executions
    ...
```

---

## Summary: Pattern Selection Guide

| Scenario | Recommended Pattern |
|----------|---------------------|
| REST/GraphQL API | API Gateway + Lambda (per domain) |
| File processing | S3 trigger + Lambda |
| Long workflows | Step Functions |
| High-volume events | Kinesis/SQS + Lambda |
| Real-time updates | WebSocket API + Lambda |
| Scheduled jobs | EventBridge Scheduler + Lambda |
| Multi-step with retries | Step Functions |
| Fan-out processing | SNS + SQS + Lambda |
| Multi-tenant SaaS | Tenant-scoped DynamoDB + authorizers |

---

*These examples represent common patterns. Adapt based on specific requirements.*
