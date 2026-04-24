# AWS Lambda Examples

Production-ready code examples for common Lambda patterns.

## Function Management (CLI)

### Create Function

```bash
# Create function with Python runtime
aws lambda create-function \
    --function-name my-function \
    --runtime python3.12 \
    --role arn:aws:iam::123456789012:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30 \
    --memory-size 256 \
    --architectures arm64

# Create function with environment variables
aws lambda create-function \
    --function-name my-function \
    --runtime nodejs20.x \
    --role arn:aws:iam::123456789012:role/lambda-role \
    --handler index.handler \
    --zip-file fileb://function.zip \
    --environment "Variables={DB_HOST=mydb.cluster.rds.amazonaws.com,LOG_LEVEL=INFO}"
```

### Update Function

```bash
# Update code
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip

# Update configuration
aws lambda update-function-configuration \
    --function-name my-function \
    --timeout 60 \
    --memory-size 512 \
    --environment "Variables={KEY1=value1,KEY2=value2}"

# Enable SnapStart
aws lambda update-function-configuration \
    --function-name my-function \
    --snap-start ApplyOn=PublishedVersions
```

### Invocation

```bash
# Synchronous invocation
aws lambda invoke \
    --function-name my-function \
    --payload '{"key": "value"}' \
    --cli-binary-format raw-in-base64-out \
    response.json

# Asynchronous invocation
aws lambda invoke \
    --function-name my-function \
    --invocation-type Event \
    --payload '{"key": "value"}' \
    --cli-binary-format raw-in-base64-out \
    response.json

# View logs with invocation
aws lambda invoke \
    --function-name my-function \
    --log-type Tail \
    --payload '{}' \
    --cli-binary-format raw-in-base64-out \
    response.json \
    --query 'LogResult' --output text | base64 -d
```

## Handler Patterns

### Python - Basic Handler

```python
import json
import logging
import boto3
from typing import Any

# Initialize outside handler for reuse
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def handler(event: dict, context: Any) -> dict:
    """
    Process incoming order.

    Args:
        event: API Gateway event or direct invocation payload
        context: Lambda context object

    Returns:
        API Gateway response format
    """
    request_id = context.aws_request_id

    try:
        # Parse input
        body = json.loads(event.get('body', '{}'))
        order_id = body.get('order_id')

        if not order_id:
            return response(400, {'error': 'order_id required'})

        # Process
        result = process_order(order_id, body)

        logger.info(json.dumps({
            'event': 'order_processed',
            'order_id': order_id,
            'request_id': request_id
        }))

        return response(200, result)

    except Exception as e:
        logger.error(json.dumps({
            'event': 'order_error',
            'error': str(e),
            'request_id': request_id
        }))
        return response(500, {'error': 'Internal server error'})

def process_order(order_id: str, data: dict) -> dict:
    """Process order business logic."""
    table.put_item(Item={'order_id': order_id, **data})
    return {'order_id': order_id, 'status': 'processed'}

def response(status_code: int, body: dict) -> dict:
    """Format API Gateway response."""
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }
```

### Python - Idempotent Handler

```python
import json
import hashlib
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
idempotency_table = dynamodb.Table('idempotency')
orders_table = dynamodb.Table('orders')

def handler(event, context):
    """Idempotent order processing."""
    body = json.loads(event.get('body', '{}'))

    # Generate idempotency key
    idempotency_key = generate_idempotency_key(body)

    # Check for existing result
    existing = get_cached_result(idempotency_key)
    if existing:
        return existing['response']

    # Process and cache
    try:
        result = process_order(body)
        response = {'statusCode': 200, 'body': json.dumps(result)}
        cache_result(idempotency_key, response)
        return response
    except Exception as e:
        # Don't cache errors - allow retry
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def generate_idempotency_key(body: dict) -> str:
    """Generate deterministic key from request."""
    canonical = json.dumps(body, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()

def get_cached_result(key: str) -> dict | None:
    """Retrieve cached result if exists and not expired."""
    try:
        response = idempotency_table.get_item(Key={'idempotency_key': key})
        item = response.get('Item')
        if item and datetime.fromisoformat(item['expires_at']) > datetime.utcnow():
            return item
    except Exception:
        pass
    return None

def cache_result(key: str, response: dict) -> None:
    """Cache result with TTL."""
    expires_at = datetime.utcnow() + timedelta(hours=24)
    idempotency_table.put_item(Item={
        'idempotency_key': key,
        'response': response,
        'expires_at': expires_at.isoformat(),
        'ttl': int(expires_at.timestamp())
    })

def process_order(body: dict) -> dict:
    """Actual order processing logic."""
    order_id = body['order_id']
    orders_table.put_item(Item={'order_id': order_id, **body})
    return {'order_id': order_id, 'status': 'processed'}
```

### Node.js - Basic Handler

```javascript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';

// Initialize outside handler
const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);
const TABLE_NAME = process.env.TABLE_NAME || 'orders';

export const handler = async (event, context) => {
  const requestId = context.awsRequestId;

  try {
    const body = JSON.parse(event.body || '{}');
    const { orderId } = body;

    if (!orderId) {
      return response(400, { error: 'orderId required' });
    }

    // Process order
    await docClient.send(new PutCommand({
      TableName: TABLE_NAME,
      Item: { orderId, ...body, createdAt: new Date().toISOString() }
    }));

    console.log(JSON.stringify({
      event: 'order_processed',
      orderId,
      requestId
    }));

    return response(200, { orderId, status: 'processed' });

  } catch (error) {
    console.error(JSON.stringify({
      event: 'order_error',
      error: error.message,
      requestId
    }));
    return response(500, { error: 'Internal server error' });
  }
};

const response = (statusCode, body) => ({
  statusCode,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body)
});
```

## Event Source Patterns

### SQS Batch Processing with Partial Failures

```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Process SQS batch with partial failure reporting.

    Returns failed message IDs so they can be retried.
    """
    batch_item_failures = []

    for record in event['Records']:
        try:
            message_id = record['messageId']
            body = json.loads(record['body'])

            process_message(body)

            logger.info(json.dumps({
                'event': 'message_processed',
                'message_id': message_id
            }))

        except Exception as e:
            logger.error(json.dumps({
                'event': 'message_failed',
                'message_id': record['messageId'],
                'error': str(e)
            }))
            batch_item_failures.append({
                'itemIdentifier': record['messageId']
            })

    return {
        'batchItemFailures': batch_item_failures
    }

def process_message(body: dict) -> None:
    """Process individual message."""
    # Business logic here
    pass
```

### DynamoDB Streams Processing

```python
import json
import logging
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event: dict, context: Any) -> dict:
    """Process DynamoDB Stream events."""
    batch_item_failures = []

    for record in event['Records']:
        try:
            event_name = record['eventName']  # INSERT, MODIFY, REMOVE

            if event_name == 'INSERT':
                new_image = record['dynamodb']['NewImage']
                handle_insert(new_image)
            elif event_name == 'MODIFY':
                old_image = record['dynamodb']['OldImage']
                new_image = record['dynamodb']['NewImage']
                handle_modify(old_image, new_image)
            elif event_name == 'REMOVE':
                old_image = record['dynamodb']['OldImage']
                handle_remove(old_image)

        except Exception as e:
            logger.error(json.dumps({
                'event': 'stream_processing_error',
                'event_id': record['eventID'],
                'error': str(e)
            }))
            batch_item_failures.append({
                'itemIdentifier': record['eventID']
            })

    return {'batchItemFailures': batch_item_failures}

def handle_insert(new_image: dict) -> None:
    """Handle new record."""
    pass

def handle_modify(old_image: dict, new_image: dict) -> None:
    """Handle record update."""
    pass

def handle_remove(old_image: dict) -> None:
    """Handle record deletion."""
    pass
```

### Kinesis Processing

```python
import json
import base64
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """Process Kinesis stream records."""
    batch_item_failures = []

    for record in event['Records']:
        try:
            # Decode Kinesis data
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data = json.loads(payload)

            sequence_number = record['kinesis']['sequenceNumber']
            partition_key = record['kinesis']['partitionKey']

            process_kinesis_record(data, partition_key)

            logger.info(json.dumps({
                'event': 'kinesis_record_processed',
                'sequence_number': sequence_number
            }))

        except Exception as e:
            logger.error(json.dumps({
                'event': 'kinesis_record_error',
                'sequence_number': record['kinesis']['sequenceNumber'],
                'error': str(e)
            }))
            batch_item_failures.append({
                'itemIdentifier': record['kinesis']['sequenceNumber']
            })

    return {'batchItemFailures': batch_item_failures}

def process_kinesis_record(data: dict, partition_key: str) -> None:
    """Process individual Kinesis record."""
    pass
```

## Layers Management

### Create Python Layer

```bash
# Create layer directory structure
mkdir -p python-layer/python

# Install dependencies
pip install \
    requests==2.31.0 \
    boto3==1.34.0 \
    -t python-layer/python \
    --platform manylinux2014_aarch64 \
    --only-binary=:all:

# Remove unnecessary files
find python-layer -type d -name "__pycache__" -exec rm -rf {} +
find python-layer -type f -name "*.pyc" -delete
find python-layer -type d -name "*.dist-info" -exec rm -rf {} +

# Package
cd python-layer && zip -r ../layer.zip python

# Publish
aws lambda publish-layer-version \
    --layer-name my-dependencies \
    --description "Python dependencies v1.0.0" \
    --zip-file fileb://layer.zip \
    --compatible-runtimes python3.11 python3.12 \
    --compatible-architectures arm64
```

### Create Node.js Layer

```bash
# Create layer directory structure
mkdir -p nodejs-layer/nodejs

# Install dependencies
cd nodejs-layer/nodejs
npm init -y
npm install lodash axios --save

# Remove dev dependencies and clean
rm -rf node_modules/.package-lock.json

# Package
cd .. && zip -r ../layer.zip nodejs

# Publish
aws lambda publish-layer-version \
    --layer-name node-dependencies \
    --description "Node.js dependencies v1.0.0" \
    --zip-file fileb://layer.zip \
    --compatible-runtimes nodejs18.x nodejs20.x
```

## Aliases and Versions

### Blue-Green Deployment

```bash
# 1. Update code
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://new-version.zip

# 2. Wait for update to complete
aws lambda wait function-updated --function-name my-function

# 3. Publish version
VERSION=$(aws lambda publish-version \
    --function-name my-function \
    --description "v2.0.0 - new feature" \
    --query 'Version' --output text)

echo "Published version: $VERSION"

# 4. Shift 10% traffic to new version
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --routing-config "{\"AdditionalVersionWeights\": {\"$VERSION\": 0.1}}"

# 5. Monitor for errors, then complete shift
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --function-version "$VERSION" \
    --routing-config '{}'
```

### Canary Deployment Script

```bash
#!/bin/bash
set -e

FUNCTION_NAME=$1
ALIAS_NAME=${2:-prod}
CANARY_PERCENT=${3:-10}
WAIT_MINUTES=${4:-5}

echo "Deploying $FUNCTION_NAME with $CANARY_PERCENT% canary..."

# Update code
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://function.zip

aws lambda wait function-updated --function-name "$FUNCTION_NAME"

# Publish version
NEW_VERSION=$(aws lambda publish-version \
    --function-name "$FUNCTION_NAME" \
    --query 'Version' --output text)

echo "Published version: $NEW_VERSION"

# Get current version
CURRENT_VERSION=$(aws lambda get-alias \
    --function-name "$FUNCTION_NAME" \
    --name "$ALIAS_NAME" \
    --query 'FunctionVersion' --output text)

echo "Current version: $CURRENT_VERSION"

# Calculate weight (0.1 = 10%)
WEIGHT=$(echo "scale=2; $CANARY_PERCENT / 100" | bc)

# Shift traffic
aws lambda update-alias \
    --function-name "$FUNCTION_NAME" \
    --name "$ALIAS_NAME" \
    --routing-config "{\"AdditionalVersionWeights\": {\"$NEW_VERSION\": $WEIGHT}}"

echo "Shifted $CANARY_PERCENT% traffic to version $NEW_VERSION"
echo "Waiting $WAIT_MINUTES minutes to monitor..."

sleep $((WAIT_MINUTES * 60))

# Check for errors (simplified - use CloudWatch in production)
ERRORS=$(aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Errors \
    --dimensions Name=FunctionName,Value="$FUNCTION_NAME" \
    --start-time "$(date -u -d "$WAIT_MINUTES minutes ago" +%Y-%m-%dT%H:%M:%SZ)" \
    --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --period 300 \
    --statistics Sum \
    --query 'Datapoints[0].Sum' --output text)

if [ "$ERRORS" = "None" ] || [ "$ERRORS" = "0" ]; then
    echo "No errors detected. Completing deployment..."
    aws lambda update-alias \
        --function-name "$FUNCTION_NAME" \
        --name "$ALIAS_NAME" \
        --function-version "$NEW_VERSION" \
        --routing-config '{}'
    echo "Deployment complete!"
else
    echo "Errors detected: $ERRORS. Rolling back..."
    aws lambda update-alias \
        --function-name "$FUNCTION_NAME" \
        --name "$ALIAS_NAME" \
        --function-version "$CURRENT_VERSION" \
        --routing-config '{}'
    echo "Rollback complete."
    exit 1
fi
```

## Event Source Mappings

### Create SQS Trigger

```bash
# Create event source mapping
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:sqs:us-east-1:123456789012:my-queue \
    --batch-size 10 \
    --maximum-batching-window-in-seconds 5 \
    --function-response-types ReportBatchItemFailures

# With event filtering
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:sqs:us-east-1:123456789012:my-queue \
    --batch-size 10 \
    --filter-criteria '{
        "Filters": [
            {"Pattern": "{\"body\": {\"type\": [\"ORDER\", \"REFUND\"]}}"}
        ]
    }'
```

### Create DynamoDB Streams Trigger

```bash
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:dynamodb:us-east-1:123456789012:table/my-table/stream/2024-01-01T00:00:00.000 \
    --starting-position LATEST \
    --batch-size 100 \
    --maximum-batching-window-in-seconds 5 \
    --bisect-batch-on-function-error \
    --maximum-retry-attempts 3 \
    --maximum-record-age-in-seconds 3600 \
    --parallelization-factor 2 \
    --destination-config '{
        "OnFailure": {
            "Destination": "arn:aws:sqs:us-east-1:123456789012:dlq"
        }
    }'
```

### Create Kinesis Trigger

```bash
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:kinesis:us-east-1:123456789012:stream/my-stream \
    --starting-position LATEST \
    --batch-size 500 \
    --maximum-batching-window-in-seconds 10 \
    --parallelization-factor 5 \
    --bisect-batch-on-function-error \
    --maximum-retry-attempts 5 \
    --tumbling-window-in-seconds 30
```

## Provisioned Concurrency

```bash
# Configure provisioned concurrency on alias
aws lambda put-provisioned-concurrency-config \
    --function-name my-function \
    --qualifier prod \
    --provisioned-concurrent-executions 10

# Check status
aws lambda get-provisioned-concurrency-config \
    --function-name my-function \
    --qualifier prod

# Delete provisioned concurrency
aws lambda delete-provisioned-concurrency-config \
    --function-name my-function \
    --qualifier prod
```

## Monitoring Commands

```bash
# Get function metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Duration \
    --dimensions Name=FunctionName,Value=my-function \
    --start-time "$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --period 300 \
    --statistics Average Maximum

# Get recent logs
aws logs filter-log-events \
    --log-group-name /aws/lambda/my-function \
    --start-time $(($(date +%s) - 3600))000 \
    --filter-pattern "ERROR"

# Tail logs (requires AWS SAM CLI)
sam logs -n my-function --tail
```

---

*AWS Lambda Examples | Use with [README.md](README.md)*
