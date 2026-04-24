# Serverless Templates

Copy-paste templates for AWS SAM, Serverless Framework, SST, and AWS CDK.

## AWS SAM Templates

### Basic REST API

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Basic REST API with Lambda and DynamoDB

Globals:
  Function:
    Runtime: python3.11
    Architectures:
      - arm64
    Timeout: 30
    MemorySize: 256
    Tracing: Active
    Environment:
      Variables:
        TABLE_NAME: !Ref DataTable
        LOG_LEVEL: INFO

Resources:
  # API Gateway
  HttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: prod
      CorsConfiguration:
        AllowOrigins:
          - "https://example.com"
        AllowMethods:
          - GET
          - POST
          - PUT
          - DELETE
        AllowHeaders:
          - Content-Type
          - Authorization

  # Lambda Functions
  GetItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/items.get_item
      Description: Get item by ID
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref DataTable
      Events:
        GetItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items/{id}
            Method: GET

  CreateItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/items.create_item
      Description: Create new item
      Policies:
        - DynamoDBWritePolicy:
            TableName: !Ref DataTable
      Events:
        CreateItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items
            Method: POST

  ListItemsFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/items.list_items
      Description: List all items
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref DataTable
      Events:
        ListItems:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items
            Method: GET

  # DynamoDB Table
  DataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub ${AWS::StackName}-items
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: PK
          AttributeType: S
        - AttributeName: SK
          AttributeType: S
      KeySchema:
        - AttributeName: PK
          KeyType: HASH
        - AttributeName: SK
          KeyType: RANGE
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true

Outputs:
  ApiUrl:
    Description: API Gateway URL
    Value: !Sub "https://${HttpApi}.execute-api.${AWS::Region}.amazonaws.com/prod"
  TableName:
    Description: DynamoDB Table Name
    Value: !Ref DataTable
```

### Event-Driven Processing with SQS

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Event-driven processing with SQS and DLQ

Globals:
  Function:
    Runtime: nodejs20.x
    Architectures:
      - arm64
    Timeout: 30
    MemorySize: 512

Resources:
  # Main Queue
  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub ${AWS::StackName}-processing
      VisibilityTimeout: 180  # 6x Lambda timeout
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3

  # Dead Letter Queue
  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub ${AWS::StackName}-dlq
      MessageRetentionPeriod: 1209600  # 14 days

  # Processor Lambda
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/processor.handler
      Description: Process messages from SQS
      ReservedConcurrentExecutions: 10
      Policies:
        - SQSPollerPolicy:
            QueueName: !GetAtt ProcessingQueue.QueueName
        - S3WritePolicy:
            BucketName: !Ref ResultsBucket
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt ProcessingQueue.Arn
            BatchSize: 10
            MaximumBatchingWindowInSeconds: 5
            FunctionResponseTypes:
              - ReportBatchItemFailures

  # DLQ Processor
  DLQProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/dlq-processor.handler
      Description: Handle failed messages
      Policies:
        - SQSPollerPolicy:
            QueueName: !GetAtt DeadLetterQueue.QueueName
      Events:
        DLQEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt DeadLetterQueue.Arn
            BatchSize: 1

  # Results Bucket
  ResultsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${AWS::StackName}-results
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256

Outputs:
  QueueUrl:
    Value: !Ref ProcessingQueue
  DLQUrl:
    Value: !Ref DeadLetterQueue
```

### Step Functions Workflow

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Step Functions workflow with Lambda

Resources:
  # Step 1: Validate
  ValidateFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/steps/validate.handler
      Runtime: python3.11
      Timeout: 30

  # Step 2: Process
  ProcessFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/steps/process.handler
      Runtime: python3.11
      Timeout: 300

  # Step 3: Notify
  NotifyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/steps/notify.handler
      Runtime: python3.11
      Timeout: 30
      Policies:
        - SNSPublishMessagePolicy:
            TopicName: !GetAtt NotificationTopic.TopicName

  # State Machine
  ProcessingStateMachine:
    Type: AWS::Serverless::StateMachine
    Properties:
      DefinitionUri: statemachine/processing.asl.json
      DefinitionSubstitutions:
        ValidateFunctionArn: !GetAtt ValidateFunction.Arn
        ProcessFunctionArn: !GetAtt ProcessFunction.Arn
        NotifyFunctionArn: !GetAtt NotifyFunction.Arn
      Policies:
        - LambdaInvokePolicy:
            FunctionName: !Ref ValidateFunction
        - LambdaInvokePolicy:
            FunctionName: !Ref ProcessFunction
        - LambdaInvokePolicy:
            FunctionName: !Ref NotifyFunction

  # Notification Topic
  NotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub ${AWS::StackName}-notifications

Outputs:
  StateMachineArn:
    Value: !Ref ProcessingStateMachine
```

```json
// statemachine/processing.asl.json
{
  "Comment": "Processing Workflow",
  "StartAt": "Validate",
  "States": {
    "Validate": {
      "Type": "Task",
      "Resource": "${ValidateFunctionArn}",
      "Next": "Process",
      "Catch": [
        {
          "ErrorEquals": ["ValidationError"],
          "Next": "ValidationFailed"
        }
      ]
    },
    "Process": {
      "Type": "Task",
      "Resource": "${ProcessFunctionArn}",
      "Next": "Notify",
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 5,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "ProcessingFailed"
        }
      ]
    },
    "Notify": {
      "Type": "Task",
      "Resource": "${NotifyFunctionArn}",
      "End": true
    },
    "ValidationFailed": {
      "Type": "Fail",
      "Error": "ValidationError",
      "Cause": "Input validation failed"
    },
    "ProcessingFailed": {
      "Type": "Fail",
      "Error": "ProcessingError",
      "Cause": "Processing step failed"
    }
  }
}
```

### Scheduled Job with EventBridge

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Scheduled job with EventBridge

Resources:
  ScheduledFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/scheduled.handler
      Runtime: python3.11
      Timeout: 900  # 15 minutes
      MemorySize: 512
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DataTable
      Events:
        HourlySchedule:
          Type: ScheduleV2
          Properties:
            ScheduleExpression: rate(1 hour)
            ScheduleExpressionTimezone: UTC
            RetryPolicy:
              MaximumRetryAttempts: 2
              MaximumEventAgeInSeconds: 3600

  DataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
```

---

## Serverless Framework Templates

### Basic API with TypeScript

```yaml
# serverless.yml
service: my-api
frameworkVersion: '3'

provider:
  name: aws
  runtime: nodejs20.x
  architecture: arm64
  region: ${opt:region, 'eu-central-1'}
  stage: ${opt:stage, 'dev'}
  memorySize: 256
  timeout: 30
  tracing:
    lambda: true
    apiGateway: true
  environment:
    TABLE_NAME: ${self:custom.tableName}
    STAGE: ${self:provider.stage}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:UpdateItem
            - dynamodb:DeleteItem
            - dynamodb:Query
          Resource:
            - !GetAtt DataTable.Arn
            - !Sub "${DataTable.Arn}/index/*"

custom:
  tableName: ${self:service}-${self:provider.stage}-data
  esbuild:
    bundle: true
    minify: true
    sourcemap: true
    exclude:
      - aws-sdk
    target: node20

plugins:
  - serverless-esbuild
  - serverless-offline

functions:
  getItem:
    handler: src/handlers/items.getItem
    events:
      - httpApi:
          path: /items/{id}
          method: get

  createItem:
    handler: src/handlers/items.createItem
    events:
      - httpApi:
          path: /items
          method: post

  listItems:
    handler: src/handlers/items.listItems
    events:
      - httpApi:
          path: /items
          method: get

resources:
  Resources:
    DataTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:custom.tableName}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: PK
            AttributeType: S
          - AttributeName: SK
            AttributeType: S
        KeySchema:
          - AttributeName: PK
            KeyType: HASH
          - AttributeName: SK
            KeyType: RANGE
        PointInTimeRecoverySpecification:
          PointInTimeRecoveryEnabled: true

  Outputs:
    ApiUrl:
      Value: !Sub "https://${HttpApi}.execute-api.${AWS::Region}.amazonaws.com"
```

### Multi-Service Architecture

```yaml
# serverless.yml
service: orders-service
frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.11
  stage: ${opt:stage, 'dev'}
  environment:
    ORDERS_TABLE: ${self:custom.ordersTable}
    EVENT_BUS: ${self:custom.eventBus}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:*
          Resource:
            - !GetAtt OrdersTable.Arn
        - Effect: Allow
          Action:
            - events:PutEvents
          Resource:
            - !Sub "arn:aws:events:${AWS::Region}:${AWS::AccountId}:event-bus/${self:custom.eventBus}"

custom:
  ordersTable: ${self:service}-${self:provider.stage}-orders
  eventBus: ${self:service}-${self:provider.stage}-bus

functions:
  createOrder:
    handler: src/handlers/orders.create
    events:
      - httpApi:
          path: /orders
          method: post

  getOrder:
    handler: src/handlers/orders.get
    events:
      - httpApi:
          path: /orders/{id}
          method: get

  # Event handler from other services
  handlePaymentCompleted:
    handler: src/handlers/events.payment_completed
    events:
      - eventBridge:
          eventBus: ${self:custom.eventBus}
          pattern:
            source:
              - payments-service
            detail-type:
              - PaymentCompleted

resources:
  Resources:
    OrdersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:custom.ordersTable}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: PK
            AttributeType: S
          - AttributeName: SK
            AttributeType: S
          - AttributeName: GSI1PK
            AttributeType: S
          - AttributeName: GSI1SK
            AttributeType: S
        KeySchema:
          - AttributeName: PK
            KeyType: HASH
          - AttributeName: SK
            KeyType: RANGE
        GlobalSecondaryIndexes:
          - IndexName: GSI1
            KeySchema:
              - AttributeName: GSI1PK
                KeyType: HASH
              - AttributeName: GSI1SK
                KeyType: RANGE
            Projection:
              ProjectionType: ALL

    EventBus:
      Type: AWS::Events::EventBus
      Properties:
        Name: ${self:custom.eventBus}
```

---

## SST Templates

### Full-Stack Application

```typescript
// sst.config.ts
import { SSTConfig } from "sst";
import { API } from "./stacks/API";
import { Database } from "./stacks/Database";
import { Web } from "./stacks/Web";

export default {
  config(_input) {
    return {
      name: "my-app",
      region: "eu-central-1",
    };
  },
  stacks(app) {
    app
      .stack(Database)
      .stack(API)
      .stack(Web);
  },
} satisfies SSTConfig;
```

```typescript
// stacks/Database.ts
import { StackContext, Table } from "sst/constructs";

export function Database({ stack }: StackContext) {
  const table = new Table(stack, "Data", {
    fields: {
      PK: "string",
      SK: "string",
      GSI1PK: "string",
      GSI1SK: "string",
    },
    primaryIndex: { partitionKey: "PK", sortKey: "SK" },
    globalIndexes: {
      GSI1: { partitionKey: "GSI1PK", sortKey: "GSI1SK" },
    },
  });

  return { table };
}
```

```typescript
// stacks/API.ts
import { StackContext, Api, use } from "sst/constructs";
import { Database } from "./Database";

export function API({ stack }: StackContext) {
  const { table } = use(Database);

  const api = new Api(stack, "Api", {
    defaults: {
      function: {
        bind: [table],
        runtime: "nodejs20.x",
        architecture: "arm_64",
      },
    },
    routes: {
      "GET /items": "packages/functions/src/items/list.handler",
      "GET /items/{id}": "packages/functions/src/items/get.handler",
      "POST /items": "packages/functions/src/items/create.handler",
      "PUT /items/{id}": "packages/functions/src/items/update.handler",
      "DELETE /items/{id}": "packages/functions/src/items/delete.handler",
    },
  });

  stack.addOutputs({
    ApiEndpoint: api.url,
  });

  return { api };
}
```

```typescript
// stacks/Web.ts
import { StackContext, StaticSite, use } from "sst/constructs";
import { API } from "./API";

export function Web({ stack }: StackContext) {
  const { api } = use(API);

  const site = new StaticSite(stack, "Site", {
    path: "packages/web",
    buildOutput: "dist",
    buildCommand: "npm run build",
    environment: {
      VITE_API_URL: api.url,
    },
  });

  stack.addOutputs({
    SiteUrl: site.url,
  });

  return { site };
}
```

```typescript
// packages/functions/src/items/list.ts
import { Table } from "sst/node/table";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, QueryCommand } from "@aws-sdk/lib-dynamodb";

const client = DynamoDBDocumentClient.from(new DynamoDBClient({}));

export async function handler() {
  const result = await client.send(
    new QueryCommand({
      TableName: Table.Data.tableName,
      KeyConditionExpression: "PK = :pk",
      ExpressionAttributeValues: {
        ":pk": "ITEMS",
      },
    })
  );

  return {
    statusCode: 200,
    body: JSON.stringify(result.Items),
  };
}
```

### Event-Driven with SST

```typescript
// stacks/Events.ts
import { StackContext, EventBus, Queue, Function } from "sst/constructs";

export function Events({ stack }: StackContext) {
  // Dead Letter Queue
  const dlq = new Queue(stack, "DLQ", {
    consumer: "packages/functions/src/dlq.handler",
  });

  // Processing Queue
  const queue = new Queue(stack, "ProcessingQueue", {
    consumer: {
      function: "packages/functions/src/processor.handler",
      cdk: {
        eventSource: {
          batchSize: 10,
          maxBatchingWindow: Duration.seconds(5),
          reportBatchItemFailures: true,
        },
      },
    },
    cdk: {
      queue: {
        deadLetterQueue: {
          queue: dlq.cdk.queue,
          maxReceiveCount: 3,
        },
      },
    },
  });

  // Event Bus
  const bus = new EventBus(stack, "Bus", {
    rules: {
      orderCreated: {
        pattern: {
          source: ["orders"],
          detailType: ["OrderCreated"],
        },
        targets: {
          queue: queue,
          notify: "packages/functions/src/notify.handler",
        },
      },
    },
  });

  return { bus, queue };
}
```

---

## AWS CDK Templates

### API with Lambda and DynamoDB

```typescript
// lib/api-stack.ts
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigw from 'aws-cdk-lib/aws-apigatewayv2';
import * as apigwIntegrations from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as nodejs from 'aws-cdk-lib/aws-lambda-nodejs';

export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB Table
    const table = new dynamodb.Table(this, 'DataTable', {
      partitionKey: { name: 'PK', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'SK', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      pointInTimeRecovery: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    // Shared Lambda configuration
    const lambdaConfig: nodejs.NodejsFunctionProps = {
      runtime: lambda.Runtime.NODEJS_20_X,
      architecture: lambda.Architecture.ARM_64,
      timeout: cdk.Duration.seconds(30),
      memorySize: 256,
      tracing: lambda.Tracing.ACTIVE,
      environment: {
        TABLE_NAME: table.tableName,
        NODE_OPTIONS: '--enable-source-maps',
      },
      bundling: {
        minify: true,
        sourceMap: true,
        externalModules: ['@aws-sdk/*'],
      },
    };

    // Lambda Functions
    const getItemFn = new nodejs.NodejsFunction(this, 'GetItemFunction', {
      ...lambdaConfig,
      entry: 'src/handlers/items/get.ts',
    });

    const listItemsFn = new nodejs.NodejsFunction(this, 'ListItemsFunction', {
      ...lambdaConfig,
      entry: 'src/handlers/items/list.ts',
    });

    const createItemFn = new nodejs.NodejsFunction(this, 'CreateItemFunction', {
      ...lambdaConfig,
      entry: 'src/handlers/items/create.ts',
    });

    // Grant permissions
    table.grantReadData(getItemFn);
    table.grantReadData(listItemsFn);
    table.grantWriteData(createItemFn);

    // HTTP API
    const api = new apigw.HttpApi(this, 'HttpApi', {
      corsPreflight: {
        allowOrigins: ['https://example.com'],
        allowMethods: [apigw.CorsHttpMethod.GET, apigw.CorsHttpMethod.POST],
        allowHeaders: ['Content-Type', 'Authorization'],
      },
    });

    // Routes
    api.addRoutes({
      path: '/items/{id}',
      methods: [apigw.HttpMethod.GET],
      integration: new apigwIntegrations.HttpLambdaIntegration('GetItem', getItemFn),
    });

    api.addRoutes({
      path: '/items',
      methods: [apigw.HttpMethod.GET],
      integration: new apigwIntegrations.HttpLambdaIntegration('ListItems', listItemsFn),
    });

    api.addRoutes({
      path: '/items',
      methods: [apigw.HttpMethod.POST],
      integration: new apigwIntegrations.HttpLambdaIntegration('CreateItem', createItemFn),
    });

    // Outputs
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url!,
      description: 'API Gateway URL',
    });

    new cdk.CfnOutput(this, 'TableName', {
      value: table.tableName,
      description: 'DynamoDB Table Name',
    });
  }
}
```

### Step Functions with CDK

```typescript
// lib/workflow-stack.ts
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as nodejs from 'aws-cdk-lib/aws-lambda-nodejs';

export class WorkflowStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambda Functions
    const validateFn = new nodejs.NodejsFunction(this, 'ValidateFunction', {
      entry: 'src/steps/validate.ts',
      runtime: lambda.Runtime.NODEJS_20_X,
    });

    const processFn = new nodejs.NodejsFunction(this, 'ProcessFunction', {
      entry: 'src/steps/process.ts',
      runtime: lambda.Runtime.NODEJS_20_X,
      timeout: cdk.Duration.minutes(5),
    });

    const notifyFn = new nodejs.NodejsFunction(this, 'NotifyFunction', {
      entry: 'src/steps/notify.ts',
      runtime: lambda.Runtime.NODEJS_20_X,
    });

    // Step Functions Tasks
    const validateTask = new tasks.LambdaInvoke(this, 'Validate', {
      lambdaFunction: validateFn,
      outputPath: '$.Payload',
    });

    const processTask = new tasks.LambdaInvoke(this, 'Process', {
      lambdaFunction: processFn,
      outputPath: '$.Payload',
    }).addRetry({
      maxAttempts: 3,
      interval: cdk.Duration.seconds(5),
      backoffRate: 2,
    });

    const notifyTask = new tasks.LambdaInvoke(this, 'Notify', {
      lambdaFunction: notifyFn,
      outputPath: '$.Payload',
    });

    // Error handling
    const failState = new sfn.Fail(this, 'Failed', {
      cause: 'Processing failed',
      error: 'ProcessingError',
    });

    // State Machine Definition
    const definition = validateTask
      .addCatch(failState, { errors: ['ValidationError'] })
      .next(processTask)
      .addCatch(failState, { errors: ['States.ALL'] })
      .next(notifyTask);

    // State Machine
    const stateMachine = new sfn.StateMachine(this, 'ProcessingWorkflow', {
      definition,
      timeout: cdk.Duration.minutes(30),
      tracingEnabled: true,
    });

    new cdk.CfnOutput(this, 'StateMachineArn', {
      value: stateMachine.stateMachineArn,
    });
  }
}
```

---

## Lambda Handler Templates

### Python Handler with Powertools

```python
# src/handlers/items.py
import json
import os
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.idempotency import (
    idempotent,
    DynamoDBPersistenceLayer,
    IdempotencyConfig,
)
import boto3

# Initialize Powertools
logger = Logger()
tracer = Tracer()
metrics = Metrics()
app = APIGatewayHttpResolver()

# Initialize outside handler
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

# Idempotency
persistence_layer = DynamoDBPersistenceLayer(table_name=os.environ.get('IDEMPOTENCY_TABLE', 'IdempotencyTable'))
idempotency_config = IdempotencyConfig(expires_after_seconds=3600)


@app.get("/items/<item_id>")
@tracer.capture_method
def get_item(item_id: str):
    """Get item by ID"""
    logger.info("Getting item", item_id=item_id)

    response = table.get_item(Key={'PK': 'ITEM', 'SK': item_id})

    if 'Item' not in response:
        return {"error": "Item not found"}, 404

    metrics.add_metric(name="ItemsRetrieved", unit="Count", value=1)
    return response['Item']


@app.get("/items")
@tracer.capture_method
def list_items():
    """List all items"""
    response = table.query(
        KeyConditionExpression='PK = :pk',
        ExpressionAttributeValues={':pk': 'ITEM'}
    )
    return {"items": response.get('Items', [])}


@app.post("/items")
@tracer.capture_method
@idempotent(config=idempotency_config, persistence_store=persistence_layer)
def create_item():
    """Create new item"""
    body = app.current_event.json_body

    item = {
        'PK': 'ITEM',
        'SK': body['id'],
        'name': body['name'],
        'data': body.get('data', {})
    }

    table.put_item(Item=item)
    logger.info("Item created", item_id=body['id'])
    metrics.add_metric(name="ItemsCreated", unit="Count", value=1)

    return {"message": "Created", "item": item}, 201


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
```

### TypeScript Handler

```typescript
// src/handlers/items/get.ts
import { APIGatewayProxyHandlerV2 } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';
import { Logger } from '@aws-lambda-powertools/logger';
import { Tracer } from '@aws-lambda-powertools/tracer';
import { Metrics, MetricUnit } from '@aws-lambda-powertools/metrics';

// Initialize outside handler
const logger = new Logger({ serviceName: 'items-service' });
const tracer = new Tracer({ serviceName: 'items-service' });
const metrics = new Metrics({ serviceName: 'items-service' });

const client = tracer.captureAWSv3Client(
  DynamoDBDocumentClient.from(new DynamoDBClient({}))
);

const tableName = process.env.TABLE_NAME!;

export const handler: APIGatewayProxyHandlerV2 = async (event) => {
  const segment = tracer.getSegment();
  const handlerSegment = segment?.addNewSubsegment('handler');

  try {
    const itemId = event.pathParameters?.id;

    if (!itemId) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Missing item ID' }),
      };
    }

    logger.info('Getting item', { itemId });

    const result = await client.send(
      new GetCommand({
        TableName: tableName,
        Key: { PK: 'ITEM', SK: itemId },
      })
    );

    if (!result.Item) {
      metrics.addMetric('ItemNotFound', MetricUnit.Count, 1);
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Item not found' }),
      };
    }

    metrics.addMetric('ItemsRetrieved', MetricUnit.Count, 1);

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result.Item),
    };
  } catch (error) {
    logger.error('Error getting item', { error });
    throw error;
  } finally {
    handlerSegment?.close();
    metrics.publishStoredMetrics();
  }
};
```

---

## IAM Policy Templates

### Least Privilege DynamoDB

```yaml
# Specific table access
Statement:
  - Effect: Allow
    Action:
      - dynamodb:GetItem
      - dynamodb:Query
    Resource:
      - !GetAtt DataTable.Arn
      - !Sub "${DataTable.Arn}/index/*"

# Write access
  - Effect: Allow
    Action:
      - dynamodb:PutItem
      - dynamodb:UpdateItem
      - dynamodb:DeleteItem
    Resource:
      - !GetAtt DataTable.Arn
```

### S3 Access

```yaml
# Read-only specific prefix
Statement:
  - Effect: Allow
    Action:
      - s3:GetObject
    Resource:
      - !Sub "${Bucket.Arn}/uploads/*"

# Write access
  - Effect: Allow
    Action:
      - s3:PutObject
    Resource:
      - !Sub "${Bucket.Arn}/results/*"
```

### EventBridge

```yaml
# Publish events
Statement:
  - Effect: Allow
    Action:
      - events:PutEvents
    Resource:
      - !Sub "arn:aws:events:${AWS::Region}:${AWS::AccountId}:event-bus/${EventBus}"
```

### Secrets Manager

```yaml
# Read specific secret
Statement:
  - Effect: Allow
    Action:
      - secretsmanager:GetSecretValue
    Resource:
      - !Ref MySecret
```

---

## Configuration Templates

### Environment Variables Pattern

```yaml
# SAM template
Globals:
  Function:
    Environment:
      Variables:
        # Required
        TABLE_NAME: !Ref DataTable
        LOG_LEVEL: !If [IsProd, "INFO", "DEBUG"]

        # Feature flags
        FEATURE_NEW_UI: !If [IsProd, "false", "true"]

        # External services (use Secrets Manager for sensitive)
        EXTERNAL_API_URL: !Sub "https://api.${Environment}.example.com"
```

### Tagging Strategy

```yaml
# SAM template
Globals:
  Function:
    Tags:
      Environment: !Ref Environment
      Service: !Ref AWS::StackName
      Owner: platform-team
      CostCenter: engineering

Resources:
  DataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Service
          Value: !Ref AWS::StackName
```

---

*Templates are starting points. Customize based on requirements.*
