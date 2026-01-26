# AWS Lambda Templates

Infrastructure as Code templates for Lambda deployments.

## SAM Templates

### Basic Function

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Basic Lambda function

Globals:
  Function:
    Timeout: 30
    MemorySize: 256
    Runtime: python3.12
    Architectures:
      - arm64
    Tracing: Active
    Environment:
      Variables:
        LOG_LEVEL: INFO

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-my-function'
      Handler: app.handler
      CodeUri: src/
      Description: Process incoming requests
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref MyTable

  MyTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${AWS::StackName}-table'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH

Outputs:
  FunctionArn:
    Description: Lambda Function ARN
    Value: !GetAtt MyFunction.Arn
```

### API Gateway Integration

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Lambda with API Gateway

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
    Default: dev

Globals:
  Function:
    Timeout: 30
    MemorySize: 512
    Runtime: python3.12
    Architectures:
      - arm64
    Tracing: Active
    Environment:
      Variables:
        ENVIRONMENT: !Ref Environment
        LOG_LEVEL: !If [IsProd, INFO, DEBUG]

Conditions:
  IsProd: !Equals [!Ref Environment, prod]

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-api'
      Handler: app.handler
      CodeUri: src/
      Events:
        GetItems:
          Type: Api
          Properties:
            Path: /items
            Method: GET
            RestApiId: !Ref Api
        PostItem:
          Type: Api
          Properties:
            Path: /items
            Method: POST
            RestApiId: !Ref Api
        GetItem:
          Type: Api
          Properties:
            Path: /items/{id}
            Method: GET
            RestApiId: !Ref Api

  Api:
    Type: AWS::Serverless::Api
    Properties:
      Name: !Sub '${AWS::StackName}-api'
      StageName: !Ref Environment
      TracingEnabled: true
      AccessLogSetting:
        DestinationArn: !GetAtt ApiAccessLogs.Arn
        Format: '{"requestId":"$context.requestId","ip":"$context.identity.sourceIp","method":"$context.httpMethod","path":"$context.path","status":"$context.status","latency":"$context.responseLatency"}'

  ApiAccessLogs:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/apigateway/${AWS::StackName}'
      RetentionInDays: 30

Outputs:
  ApiUrl:
    Description: API Gateway URL
    Value: !Sub 'https://${Api}.execute-api.${AWS::Region}.amazonaws.com/${Environment}'
```

### SQS Event Source

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Lambda with SQS trigger

Resources:
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-processor'
      Handler: app.handler
      Runtime: python3.12
      Architectures:
        - arm64
      MemorySize: 512
      Timeout: 60
      CodeUri: src/
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt Queue.Arn
            BatchSize: 10
            MaximumBatchingWindowInSeconds: 5
            FunctionResponseTypes:
              - ReportBatchItemFailures
            FilterCriteria:
              Filters:
                - Pattern: '{"body": {"type": ["ORDER"]}}'
      Policies:
        - SQSPollerPolicy:
            QueueName: !GetAtt Queue.QueueName
        - SQSSendMessagePolicy:
            QueueName: !GetAtt DeadLetterQueue.QueueName

  Queue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub '${AWS::StackName}-queue'
      VisibilityTimeout: 300  # 5x function timeout
      MessageRetentionPeriod: 1209600  # 14 days
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub '${AWS::StackName}-dlq'
      MessageRetentionPeriod: 1209600

  DLQAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${AWS::StackName}-dlq-messages'
      AlarmDescription: Messages in DLQ
      MetricName: ApproximateNumberOfMessagesVisible
      Namespace: AWS/SQS
      Dimensions:
        - Name: QueueName
          Value: !GetAtt DeadLetterQueue.QueueName
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold

Outputs:
  QueueUrl:
    Description: SQS Queue URL
    Value: !Ref Queue
```

### DynamoDB Streams

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Lambda with DynamoDB Streams trigger

Resources:
  StreamProcessor:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-stream-processor'
      Handler: app.handler
      Runtime: python3.12
      Architectures:
        - arm64
      MemorySize: 512
      Timeout: 60
      CodeUri: src/
      Events:
        DynamoDBEvent:
          Type: DynamoDB
          Properties:
            Stream: !GetAtt Table.StreamArn
            StartingPosition: LATEST
            BatchSize: 100
            MaximumBatchingWindowInSeconds: 5
            BisectBatchOnFunctionError: true
            MaximumRetryAttempts: 3
            MaximumRecordAgeInSeconds: 3600
            ParallelizationFactor: 2
            DestinationConfig:
              OnFailure:
                Destination: !GetAtt FailureQueue.Arn
            FunctionResponseTypes:
              - ReportBatchItemFailures
      Policies:
        - DynamoDBStreamReadPolicy:
            TableName: !Ref Table
            StreamName: !Select [3, !Split ['/', !GetAtt Table.StreamArn]]
        - SQSSendMessagePolicy:
            QueueName: !GetAtt FailureQueue.QueueName

  Table:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${AWS::StackName}-table'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES

  FailureQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub '${AWS::StackName}-failures'
```

### SnapStart Configuration

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Lambda with SnapStart enabled

Resources:
  JavaFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-java-function'
      Handler: com.example.Handler::handleRequest
      Runtime: java21
      Architectures:
        - arm64
      MemorySize: 1024
      Timeout: 30
      CodeUri: target/function.jar
      SnapStart:
        ApplyOn: PublishedVersions
      AutoPublishAlias: live
      DeploymentPreference:
        Type: AllAtOnce

  PythonFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-python-function'
      Handler: app.handler
      Runtime: python3.12
      Architectures:
        - arm64
      MemorySize: 512
      Timeout: 30
      CodeUri: src/
      SnapStart:
        ApplyOn: PublishedVersions
      AutoPublishAlias: live
```

### Canary Deployment

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Lambda with CodeDeploy canary deployment

Resources:
  CanaryFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-canary'
      Handler: app.handler
      Runtime: python3.12
      Architectures:
        - arm64
      MemorySize: 512
      Timeout: 30
      CodeUri: src/
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Canary10Percent5Minutes
        Alarms:
          - !Ref ErrorAlarm
          - !Ref DurationAlarm
        Hooks:
          PreTraffic: !Ref PreTrafficHook
          PostTraffic: !Ref PostTrafficHook

  PreTrafficHook:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-pre-traffic'
      Handler: hooks.pre_traffic
      Runtime: python3.12
      MemorySize: 256
      Timeout: 60
      CodeUri: hooks/
      Policies:
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - codedeploy:PutLifecycleEventHookExecutionStatus
              Resource: '*'
            - Effect: Allow
              Action:
                - lambda:InvokeFunction
              Resource: !GetAtt CanaryFunction.Arn

  PostTrafficHook:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-post-traffic'
      Handler: hooks.post_traffic
      Runtime: python3.12
      MemorySize: 256
      Timeout: 60
      CodeUri: hooks/
      Policies:
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - codedeploy:PutLifecycleEventHookExecutionStatus
              Resource: '*'

  ErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${AWS::StackName}-errors'
      MetricName: Errors
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref CanaryFunction
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold

  DurationAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${AWS::StackName}-duration'
      MetricName: Duration
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref CanaryFunction
      Statistic: Average
      Period: 60
      EvaluationPeriods: 1
      Threshold: 5000  # 5 seconds
      ComparisonOperator: GreaterThanThreshold
```

## Terraform Templates

### Basic Function

```hcl
# variables.tf
variable "environment" {
  type    = string
  default = "dev"
}

variable "function_name" {
  type = string
}

# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/function.zip"
}

resource "aws_lambda_function" "main" {
  function_name = "${var.function_name}-${var.environment}"
  role          = aws_iam_role.lambda.arn
  handler       = "app.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  memory_size = 512
  timeout     = 30

  environment {
    variables = {
      ENVIRONMENT = var.environment
      LOG_LEVEL   = var.environment == "prod" ? "INFO" : "DEBUG"
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_iam_role" "lambda" {
  name = "${var.function_name}-${var.environment}-role"

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

resource "aws_iam_role_policy_attachment" "lambda_xray" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.main.function_name}"
  retention_in_days = 30
}

output "function_arn" {
  value = aws_lambda_function.main.arn
}

output "function_name" {
  value = aws_lambda_function.main.function_name
}
```

### With Layers

```hcl
resource "aws_lambda_layer_version" "dependencies" {
  filename            = "${path.module}/layer.zip"
  layer_name          = "${var.function_name}-dependencies"
  compatible_runtimes = ["python3.11", "python3.12"]
  compatible_architectures = ["arm64"]

  source_code_hash = filebase64sha256("${path.module}/layer.zip")
}

resource "aws_lambda_function" "main" {
  function_name = "${var.function_name}-${var.environment}"
  role          = aws_iam_role.lambda.arn
  handler       = "app.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  layers = [aws_lambda_layer_version.dependencies.arn]

  memory_size = 512
  timeout     = 30

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }
}
```

### With SQS Trigger

```hcl
resource "aws_sqs_queue" "main" {
  name                       = "${var.function_name}-${var.environment}-queue"
  visibility_timeout_seconds = 300  # 5x function timeout
  message_retention_seconds  = 1209600

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "dlq" {
  name                      = "${var.function_name}-${var.environment}-dlq"
  message_retention_seconds = 1209600
}

resource "aws_lambda_event_source_mapping" "sqs" {
  event_source_arn = aws_sqs_queue.main.arn
  function_name    = aws_lambda_function.main.arn
  batch_size       = 10

  maximum_batching_window_in_seconds = 5

  function_response_types = ["ReportBatchItemFailures"]

  filter_criteria {
    filter {
      pattern = jsonencode({
        body = {
          type = ["ORDER"]
        }
      })
    }
  }
}

resource "aws_iam_role_policy" "sqs" {
  name = "${var.function_name}-sqs-policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.main.arn
      }
    ]
  })
}
```

### With Aliases and Provisioned Concurrency

```hcl
resource "aws_lambda_alias" "live" {
  name             = "live"
  function_name    = aws_lambda_function.main.function_name
  function_version = aws_lambda_function.main.version
}

resource "aws_lambda_provisioned_concurrency_config" "main" {
  count = var.environment == "prod" ? 1 : 0

  function_name                     = aws_lambda_function.main.function_name
  qualifier                         = aws_lambda_alias.live.name
  provisioned_concurrent_executions = 10
}
```

## CloudFormation Templates

### Function with VPC

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda in VPC

Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>

Resources:
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Lambda security group
      VpcId: !Ref VpcId
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-vpc-function'
      Runtime: python3.12
      Handler: index.handler
      Role: !GetAtt LambdaRole.Arn
      Timeout: 30
      MemorySize: 512
      VpcConfig:
        SecurityGroupIds:
          - !Ref SecurityGroup
        SubnetIds: !Ref SubnetIds
      Code:
        ZipFile: |
          def handler(event, context):
              return {'statusCode': 200}

  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
```

---

*AWS Lambda Templates | Use with [README.md](README.md)*
