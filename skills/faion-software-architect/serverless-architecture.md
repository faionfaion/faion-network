# Serverless Architecture

Event-driven, auto-scaling compute without server management.

## What is Serverless?

- No server provisioning
- Pay per execution
- Auto-scaling to zero
- Event-driven execution

```
Event ──▶ Function ──▶ Response
          (scales automatically)
```

## Serverless Services

### Compute (FaaS)
| Provider | Service |
|----------|---------|
| AWS | Lambda |
| GCP | Cloud Functions |
| Azure | Azure Functions |
| Cloudflare | Workers |
| Vercel | Edge Functions |

### Backend Services
| Type | Examples |
|------|----------|
| Database | DynamoDB, Firestore, PlanetScale |
| Storage | S3, Cloud Storage |
| Auth | Auth0, Cognito, Clerk |
| Queue | SQS, Pub/Sub |
| API Gateway | API Gateway, Cloud Endpoints |

## When to Choose Serverless

| Good For | Not Good For |
|----------|--------------|
| Variable traffic | Consistent high load |
| Event processing | Long-running tasks |
| APIs, webhooks | WebSockets (limited) |
| Scheduled jobs | Low latency requirements |
| MVPs, prototypes | Complex stateful apps |

## Architecture Patterns

### API Backend
```
Client ──▶ API Gateway ──▶ Lambda ──▶ DynamoDB
```

### Event Processing
```
S3 Upload ──▶ Lambda ──▶ Process ──▶ Store Result
```

### Scheduled Jobs
```
CloudWatch Events (cron) ──▶ Lambda ──▶ Task
```

### Fan-out
```
                    ┌──▶ Lambda A
SNS Topic ──▶ SQS ──┼──▶ Lambda B
                    └──▶ Lambda C
```

## Function Design

### Best Practices

```python
# ✅ GOOD: Small, focused functions
def process_order(event, context):
    order = parse_order(event)
    validate_order(order)
    save_order(order)
    return success_response(order.id)

# ❌ BAD: Monolithic function
def handle_everything(event, context):
    # 500 lines of code handling all cases
    pass
```

### Cold Start Optimization

```python
# Initialize outside handler (runs once per container)
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def handler(event, context):
    # Reuses existing connection
    return table.get_item(Key={'id': event['id']})
```

### Keep Functions Warm
```yaml
# serverless.yml
functions:
  api:
    handler: handler.main
    events:
      - schedule: rate(5 minutes)  # Keep warm
```

## State Management

Serverless functions are stateless. Use external services:

| State Type | Solution |
|------------|----------|
| Session | Redis, DynamoDB |
| Cache | ElastiCache, Momento |
| Files | S3, Cloud Storage |
| Database | RDS Proxy, PlanetScale |

## Limitations

| Limitation | Workaround |
|------------|------------|
| Timeout (15min Lambda) | Step Functions for long tasks |
| Cold starts | Keep warm, provisioned concurrency |
| No local state | External cache/DB |
| Vendor lock-in | Use abstraction layers |
| Debugging harder | Good logging, tracing |

## Cost Model

```
Cost = Requests × Duration × Memory

AWS Lambda Example:
- $0.20 per 1M requests
- $0.0000166667 per GB-second

1M requests × 200ms × 128MB = ~$0.50/month
```

## Serverless Framework Example

```yaml
# serverless.yml
service: my-api

provider:
  name: aws
  runtime: python3.11
  region: eu-central-1

functions:
  getUser:
    handler: handlers/users.get
    events:
      - http:
          path: users/{id}
          method: get

  createOrder:
    handler: handlers/orders.create
    events:
      - http:
          path: orders
          method: post

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: users
        BillingMode: PAY_PER_REQUEST
```

## Monitoring

Essential for serverless:
- CloudWatch Logs / Metrics
- X-Ray for tracing
- Custom dashboards
- Alerts on errors, duration

## Related

- [event-driven-architecture.md](event-driven-architecture.md) - Event patterns
- [cloud-architecture.md](cloud-architecture.md) - Cloud context
