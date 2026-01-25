---
name: faion-aws-lambda-reference
description: AWS Lambda serverless compute
---

# AWS Lambda

Serverless function management, layers, event sources, and deployment patterns.

## Function Management

```bash
# List functions
aws lambda list-functions

# Get function configuration
aws lambda get-function --function-name my-function

# Create function
aws lambda create-function \
    --function-name my-function \
    --runtime python3.11 \
    --role arn:aws:iam::123456789012:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30 \
    --memory-size 256

# Update function code
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip

# Update function configuration
aws lambda update-function-configuration \
    --function-name my-function \
    --timeout 60 \
    --memory-size 512 \
    --environment "Variables={KEY1=value1,KEY2=value2}"

# Delete function
aws lambda delete-function --function-name my-function
```

## Invocation

```bash
# Invoke synchronously
aws lambda invoke \
    --function-name my-function \
    --payload '{"key": "value"}' \
    --cli-binary-format raw-in-base64-out \
    response.json

# Invoke asynchronously
aws lambda invoke \
    --function-name my-function \
    --invocation-type Event \
    --payload '{"key": "value"}' \
    --cli-binary-format raw-in-base64-out \
    response.json

# View logs
aws lambda invoke \
    --function-name my-function \
    --log-type Tail \
    --payload '{}' \
    --cli-binary-format raw-in-base64-out \
    response.json \
    --query 'LogResult' --output text | base64 -d
```

## Layers

```bash
# Publish layer version
aws lambda publish-layer-version \
    --layer-name my-layer \
    --description "My layer" \
    --zip-file fileb://layer.zip \
    --compatible-runtimes python3.11 python3.10

# Add layer to function
aws lambda update-function-configuration \
    --function-name my-function \
    --layers arn:aws:lambda:us-east-1:123456789012:layer:my-layer:1

# Delete layer version
aws lambda delete-layer-version \
    --layer-name my-layer \
    --version-number 1
```

## Event Source Mappings

```bash
# Create SQS trigger
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:sqs:us-east-1:123456789012:my-queue \
    --batch-size 10

# Create DynamoDB Streams trigger
aws lambda create-event-source-mapping \
    --function-name my-function \
    --event-source-arn arn:aws:dynamodb:us-east-1:123456789012:table/my-table/stream/... \
    --starting-position LATEST \
    --batch-size 100

# Delete event source mapping
aws lambda delete-event-source-mapping --uuid "uuid-here"
```

## Aliases and Versions

```bash
# Publish version
aws lambda publish-version \
    --function-name my-function \
    --description "v1.0.0"

# Create alias
aws lambda create-alias \
    --function-name my-function \
    --name prod \
    --function-version 1

# Update alias (blue-green deployment)
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --function-version 2 \
    --routing-config AdditionalVersionWeights={"1"=0.1}  # 10% to v1

# Complete switch
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --function-version 2
```

## Deployment Patterns

### Blue-Green Deployment

```bash
# Deploy new version
aws lambda update-function-code --function-name my-function --zip-file fileb://new.zip
aws lambda publish-version --function-name my-function

# Shift traffic gradually
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --routing-config AdditionalVersionWeights={"1"=0.1}

# Complete switch
aws lambda update-alias \
    --function-name my-function \
    --name prod \
    --function-version 2
```

## Sources

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/lambda/)
- [Lambda Runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)
- [Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
