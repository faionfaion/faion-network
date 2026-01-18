# M-DO-008: AWS Lambda Serverless

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #aws, #lambda, #serverless, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Managing servers is time-consuming and expensive for event-driven workloads. Paying for idle compute capacity wastes money on unpredictable traffic patterns.

## Promise

After this methodology, you will build serverless applications with AWS Lambda. You'll pay only for actual compute time with automatic scaling.

## Overview

AWS Lambda runs code without provisioning servers. Functions execute in response to events (HTTP, S3, SQS, schedule) and scale automatically.

---

## Framework

### Step 1: Lambda Basics

```
Lambda Function Components:
├── Handler - Entry point function
├── Runtime - Node.js, Python, Go, etc.
├── Memory - 128 MB to 10 GB
├── Timeout - Up to 15 minutes
├── Environment - Variables
├── Layers - Shared libraries
└── Triggers - Event sources
```

### Step 2: Node.js Lambda

```javascript
// handler.js
export const handler = async (event, context) => {
  console.log('Event:', JSON.stringify(event, null, 2));

  // API Gateway event
  const body = JSON.parse(event.body || '{}');

  try {
    const result = await processRequest(body);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        message: 'Success',
        data: result,
      }),
    };
  } catch (error) {
    console.error('Error:', error);

    return {
      statusCode: 500,
      body: JSON.stringify({
        message: 'Internal Server Error',
      }),
    };
  }
};

async function processRequest(data) {
  // Business logic here
  return { processed: true, data };
}
```

### Step 3: Python Lambda

```python
# handler.py
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")

    # Environment variables
    table_name = os.environ.get('TABLE_NAME')

    try:
        body = json.loads(event.get('body', '{}'))
        result = process_request(body)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'message': 'Success',
                'data': result,
            }),
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error'}),
        }


def process_request(data):
    return {'processed': True, 'data': data}
```

### Step 4: Deploy with AWS CLI

```bash
# Create deployment package
zip -r function.zip handler.js node_modules/

# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime nodejs20.x \
  --handler handler.handler \
  --role arn:aws:iam::123456789:role/lambda-role \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment "Variables={TABLE_NAME=my-table}"

# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip

# Invoke function
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  output.json
```

### Step 5: API Gateway Integration

```bash
# Create REST API
aws apigateway create-rest-api \
  --name my-api \
  --endpoint-configuration types=REGIONAL

# Create resource and method
aws apigateway create-resource \
  --rest-api-id xxx \
  --parent-id yyy \
  --path-part users

aws apigateway put-method \
  --rest-api-id xxx \
  --resource-id zzz \
  --http-method POST \
  --authorization-type NONE

# Integrate with Lambda
aws apigateway put-integration \
  --rest-api-id xxx \
  --resource-id zzz \
  --http-method POST \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:123456789:function:my-function/invocations
```

### Step 6: SAM (Serverless Application Model)

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: My Serverless API

Globals:
  Function:
    Runtime: nodejs20.x
    Timeout: 30
    MemorySize: 256
    Environment:
      Variables:
        TABLE_NAME: !Ref UsersTable

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handler.handler
      Events:
        GetUsers:
          Type: Api
          Properties:
            Path: /users
            Method: get
        CreateUser:
          Type: Api
          Properties:
            Path: /users
            Method: post
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable

  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: users
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH

Outputs:
  ApiUrl:
    Description: API Gateway endpoint URL
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
```

```bash
# Build and deploy
sam build
sam deploy --guided

# Local testing
sam local start-api
sam local invoke ApiFunction --event event.json
```

---

## Templates

### Serverless Framework

```yaml
# serverless.yml
service: my-service

provider:
  name: aws
  runtime: nodejs20.x
  region: us-east-1
  stage: ${opt:stage, 'dev'}
  memorySize: 256
  timeout: 30
  environment:
    TABLE_NAME: ${self:service}-${self:provider.stage}-users

  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:Query
            - dynamodb:Scan
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:UpdateItem
            - dynamodb:DeleteItem
          Resource:
            - !GetAtt UsersTable.Arn

functions:
  getUsers:
    handler: src/handlers/users.getAll
    events:
      - http:
          path: users
          method: get
          cors: true

  createUser:
    handler: src/handlers/users.create
    events:
      - http:
          path: users
          method: post
          cors: true

  processQueue:
    handler: src/handlers/queue.process
    events:
      - sqs:
          arn: !GetAtt ProcessingQueue.Arn
          batchSize: 10

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:provider.environment.TABLE_NAME}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
        KeySchema:
          - AttributeName: id
            KeyType: HASH

    ProcessingQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: ${self:service}-${self:provider.stage}-queue

plugins:
  - serverless-offline
  - serverless-plugin-typescript

custom:
  serverless-offline:
    httpPort: 3000
```

### Lambda with Terraform

```hcl
# main.tf
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "api" {
  function_name    = "${var.project}-${var.environment}-api"
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  handler          = "handler.handler"
  runtime          = "nodejs20.x"
  role             = aws_iam_role.lambda.arn
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.users.name
      NODE_ENV   = var.environment
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda]
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project}-${var.environment}-api"
  retention_in_days = 14
}

resource "aws_iam_role" "lambda" {
  name = "${var.project}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# API Gateway
resource "aws_apigatewayv2_api" "api" {
  name          = "${var.project}-${var.environment}"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["*"]
  }
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id             = aws_apigatewayv2_api.api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.api.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_lambda_permission" "api" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*"
}
```

---

## Examples

### S3 Trigger

```javascript
// Process uploaded files
export const handler = async (event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key);

    console.log(`Processing: s3://${bucket}/${key}`);

    // Process file
    const { S3Client, GetObjectCommand } = require('@aws-sdk/client-s3');
    const s3 = new S3Client({});

    const response = await s3.send(new GetObjectCommand({
      Bucket: bucket,
      Key: key,
    }));

    const content = await response.Body.transformToString();
    // Process content...
  }
};
```

### Scheduled Task

```yaml
# serverless.yml
functions:
  dailyCleanup:
    handler: src/handlers/cleanup.handler
    events:
      - schedule:
          rate: cron(0 2 * * ? *)  # Daily at 2 AM UTC
          enabled: true
```

---

## Common Mistakes

1. **Cold starts ignored** - Use provisioned concurrency for latency-sensitive
2. **No error handling** - Always catch and log errors
3. **Large packages** - Use layers for dependencies
4. **Synchronous operations** - Use async/await properly
5. **No monitoring** - Enable X-Ray and CloudWatch

---

## Checklist

- [ ] Proper IAM role (least privilege)
- [ ] Environment variables for config
- [ ] Error handling and logging
- [ ] CloudWatch alarms
- [ ] API Gateway CORS configured
- [ ] Cold start optimization
- [ ] Deployment automation (SAM/Serverless)
- [ ] Local testing setup

---

## Next Steps

- M-DO-007: AWS EC2
- M-DO-009: Terraform Basics
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-008 v1.0*
