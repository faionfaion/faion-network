---
name: faion-aws-networking-reference
description: AWS VPC, IAM, CloudFormation, CloudWatch
---

# AWS Networking & Infrastructure

CLI reference for IAM, CloudFormation, and CloudWatch.

## IAM (Identity and Access Management)

### User Management

```bash
# List users
aws iam list-users

# Create user
aws iam create-user --user-name my-user

# Create access key
aws iam create-access-key --user-name my-user

# Delete access key
aws iam delete-access-key --user-name my-user --access-key-id AKIAIOSFODNN7EXAMPLE

# Add user to group
aws iam add-user-to-group --user-name my-user --group-name developers
```

### Role Management

```bash
# Create role
aws iam create-role \
    --role-name my-role \
    --assume-role-policy-document file://trust-policy.json

# Attach managed policy
aws iam attach-role-policy \
    --role-name my-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Assume role
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/my-role \
    --role-session-name my-session
```

### Policy Management

```bash
# Create policy
aws iam create-policy \
    --policy-name my-policy \
    --policy-document file://policy.json

# Create policy version
aws iam create-policy-version \
    --policy-arn arn:aws:iam::123456789012:policy/my-policy \
    --policy-document file://new-policy.json \
    --set-as-default
```

## CloudFormation

### Stack Management

```bash
# Create stack
aws cloudformation create-stack \
    --stack-name my-stack \
    --template-body file://template.yaml \
    --parameters ParameterKey=Environment,ParameterValue=production \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

# Update stack
aws cloudformation update-stack \
    --stack-name my-stack \
    --template-body file://template.yaml

# Delete stack
aws cloudformation delete-stack --stack-name my-stack

# Wait for completion
aws cloudformation wait stack-create-complete --stack-name my-stack
```

### Change Sets

```bash
# Create change set
aws cloudformation create-change-set \
    --stack-name my-stack \
    --change-set-name my-changes \
    --template-body file://template.yaml

# Describe change set
aws cloudformation describe-change-set \
    --stack-name my-stack \
    --change-set-name my-changes

# Execute change set
aws cloudformation execute-change-set \
    --stack-name my-stack \
    --change-set-name my-changes
```

## CloudWatch

### Logs

```bash
# List log groups
aws logs describe-log-groups

# Create log group
aws logs create-log-group --log-group-name /my-app/logs

# Filter log events
aws logs filter-log-events \
    --log-group-name /my-app/logs \
    --filter-pattern "ERROR" \
    --start-time $(date -d '1 hour ago' +%s)000

# Tail logs
aws logs tail /my-app/logs --follow

# Set retention
aws logs put-retention-policy \
    --log-group-name /my-app/logs \
    --retention-in-days 30
```

### Metrics

```bash
# List metrics
aws cloudwatch list-metrics --namespace AWS/EC2

# Get metric statistics
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
    --period 300 \
    --statistics Average Maximum

# Put custom metric
aws cloudwatch put-metric-data \
    --namespace MyApp \
    --metric-name RequestCount \
    --value 100 \
    --unit Count
```

### Alarms

```bash
# Create alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "High CPU" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic

# Delete alarm
aws cloudwatch delete-alarms --alarm-names "High CPU"
```

## Security Best Practices

### Credential Management

```bash
# Rotate access keys
aws iam create-access-key --user-name my-user
aws iam delete-access-key --user-name my-user --access-key-id OLD_KEY

# Enable MFA
aws iam enable-mfa-device \
    --user-name my-user \
    --serial-number arn:aws:iam::123456789012:mfa/my-user \
    --authentication-code1 123456 \
    --authentication-code2 789012
```

### Logging

```bash
# Enable CloudTrail
aws cloudtrail create-trail \
    --name my-trail \
    --s3-bucket-name my-trail-bucket \
    --is-multi-region-trail

# Enable VPC Flow Logs
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids vpc-0123456789abcdef0 \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name vpc-flow-logs
```

## Troubleshooting

```bash
# Check identity
aws sts get-caller-identity

# Check permissions
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::123456789012:user/my-user \
    --action-names s3:GetObject \
    --resource-arns arn:aws:s3:::my-bucket/*

# Debug mode
aws s3 ls --debug
```

## Sources

- [IAM User Guide](https://docs.aws.amazon.com/iam/latest/userguide/)
- [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/latest/userguide/)
- [CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS CLI IAM Reference](https://docs.aws.amazon.com/cli/latest/reference/iam/)
- [CloudFormation CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/)
