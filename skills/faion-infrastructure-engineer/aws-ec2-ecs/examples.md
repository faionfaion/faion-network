# AWS EC2 & ECS CLI Examples

AWS CLI commands for EC2, ECS, and ECR operations.

## EC2 Commands

### Instance Management

```bash
# List running instances
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running" \
    --query "Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PublicIpAddress,Tags[?Key=='Name'].Value|[0]]" \
    --output table

# Launch instance (Graviton, recommended)
aws ec2 run-instances \
    --image-id ami-0123456789abcdef0 \
    --instance-type t4g.micro \
    --key-name my-key-pair \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-0123456789abcdef0 \
    --iam-instance-profile Name=my-instance-profile \
    --metadata-options "HttpTokens=required,HttpEndpoint=enabled" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-instance},{Key=Environment,Value=production}]'

# Start/stop/terminate
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0

# Wait for instance running
aws ec2 wait instance-running --instance-ids i-0123456789abcdef0

# Get instance console output
aws ec2 get-console-output --instance-id i-0123456789abcdef0
```

### Security Groups

```bash
# Create security group
aws ec2 create-security-group \
    --group-name my-app-sg \
    --description "Security group for my application" \
    --vpc-id vpc-0123456789abcdef0

# Add HTTPS ingress (public)
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Add SSH ingress (from bastion only)
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --source-group sg-bastion123456789

# Remove rule
aws ec2 revoke-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
```

### AMI Management

```bash
# Create AMI from instance
aws ec2 create-image \
    --instance-id i-0123456789abcdef0 \
    --name "my-ami-$(date +%Y%m%d-%H%M%S)" \
    --description "Production AMI" \
    --no-reboot

# Copy AMI to another region
aws ec2 copy-image \
    --source-image-id ami-0123456789abcdef0 \
    --source-region us-east-1 \
    --region eu-west-1 \
    --name "my-ami-eu-copy"

# List AMIs
aws ec2 describe-images \
    --owners self \
    --query "Images[*].[ImageId,Name,CreationDate]" \
    --output table

# Deregister AMI
aws ec2 deregister-image --image-id ami-0123456789abcdef0
```

---

## ECS Commands

### Cluster Management

```bash
# Create cluster with Fargate
aws ecs create-cluster \
    --cluster-name my-cluster \
    --capacity-providers FARGATE FARGATE_SPOT \
    --default-capacity-provider-strategy \
        capacityProvider=FARGATE,weight=1,base=1 \
        capacityProvider=FARGATE_SPOT,weight=4 \
    --settings name=containerInsights,value=enabled

# List clusters
aws ecs list-clusters

# Describe cluster
aws ecs describe-clusters \
    --clusters my-cluster \
    --include ATTACHMENTS SETTINGS STATISTICS

# Delete cluster
aws ecs delete-cluster --cluster my-cluster
```

### Task Definitions

```bash
# Register task definition from file
aws ecs register-task-definition \
    --cli-input-json file://task-definition.json

# List task definitions
aws ecs list-task-definitions --family-prefix my-app

# Describe task definition
aws ecs describe-task-definition --task-definition my-app:5

# Deregister task definition
aws ecs deregister-task-definition --task-definition my-app:1
```

### Services

```bash
# Create service
aws ecs create-service \
    --cluster my-cluster \
    --service-name my-service \
    --task-definition my-app:5 \
    --desired-count 2 \
    --launch-type FARGATE \
    --platform-version LATEST \
    --network-configuration "awsvpcConfiguration={
        subnets=[subnet-private1,subnet-private2],
        securityGroups=[sg-app],
        assignPublicIp=DISABLED
    }" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=app,containerPort=8080" \
    --health-check-grace-period-seconds 60 \
    --deployment-configuration "minimumHealthyPercent=100,maximumPercent=200,deploymentCircuitBreaker={enable=true,rollback=true}"

# Update service (deploy new version)
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --task-definition my-app:6 \
    --force-new-deployment

# Scale service
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --desired-count 4

# List services
aws ecs list-services --cluster my-cluster

# Describe service
aws ecs describe-services \
    --cluster my-cluster \
    --services my-service

# Delete service
aws ecs delete-service \
    --cluster my-cluster \
    --service my-service \
    --force
```

### Tasks

```bash
# List running tasks
aws ecs list-tasks \
    --cluster my-cluster \
    --service-name my-service

# Describe tasks
aws ecs describe-tasks \
    --cluster my-cluster \
    --tasks task-id-1 task-id-2

# Run one-off task
aws ecs run-task \
    --cluster my-cluster \
    --task-definition my-migration:1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={
        subnets=[subnet-private1],
        securityGroups=[sg-task],
        assignPublicIp=DISABLED
    }"

# Stop task
aws ecs stop-task \
    --cluster my-cluster \
    --task task-id \
    --reason "Manual stop"

# Execute command in container (ECS Exec)
aws ecs execute-command \
    --cluster my-cluster \
    --task task-id \
    --container app \
    --interactive \
    --command "/bin/sh"
```

### Auto Scaling

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/my-cluster/my-service \
    --min-capacity 2 \
    --max-capacity 10

# Create target tracking policy (CPU)
aws application-autoscaling put-scaling-policy \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/my-cluster/my-service \
    --policy-name cpu-target-tracking \
    --policy-type TargetTrackingScaling \
    --target-tracking-scaling-policy-configuration '{
        "TargetValue": 70.0,
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
        },
        "ScaleOutCooldown": 60,
        "ScaleInCooldown": 300
    }'
```

---

## ECR Commands

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.us-east-1.amazonaws.com

# Create repository with scanning
aws ecr create-repository \
    --repository-name my-app \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability IMMUTABLE

# List repositories
aws ecr describe-repositories

# List images
aws ecr list-images --repository-name my-app

# Get image scan results
aws ecr describe-image-scan-findings \
    --repository-name my-app \
    --image-id imageTag=v1.0.0

# Delete untagged images
aws ecr batch-delete-image \
    --repository-name my-app \
    --image-ids "$(aws ecr list-images \
        --repository-name my-app \
        --filter tagStatus=UNTAGGED \
        --query 'imageIds[*]' \
        --output json)"

# Set lifecycle policy (keep last 10 images)
aws ecr put-lifecycle-policy \
    --repository-name my-app \
    --lifecycle-policy-text '{
        "rules": [{
            "rulePriority": 1,
            "description": "Keep last 10 images",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 10
            },
            "action": { "type": "expire" }
        }]
    }'
```

---

## CloudWatch Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /ecs/my-app

# Set retention
aws logs put-retention-policy \
    --log-group-name /ecs/my-app \
    --retention-in-days 30

# Tail logs
aws logs tail /ecs/my-app --follow

# Get recent logs
aws logs get-log-events \
    --log-group-name /ecs/my-app \
    --log-stream-name ecs/app/task-id \
    --limit 100
```

---

*AWS EC2 & ECS CLI Examples | faion-infrastructure-engineer*
