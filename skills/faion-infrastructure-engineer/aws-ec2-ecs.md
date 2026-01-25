---
name: faion-aws-ec2-ecs-reference
description: AWS EC2, ECS, EKS compute services
---

# AWS Compute: EC2, ECS, EKS

CLI reference for AWS compute services: EC2 instances, ECS containers, and EKS Kubernetes.

## EC2 (Elastic Compute Cloud)

### Instance Management

```bash
# List running instances
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running" \
    --query "Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PublicIpAddress]" \
    --output table

# Launch instance
aws ec2 run-instances \
    --image-id ami-0123456789abcdef0 \
    --instance-type t3.micro \
    --key-name my-key-pair \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-0123456789abcdef0 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-instance}]'

# Start/stop/terminate
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0

# Wait for instance running
aws ec2 wait instance-running --instance-ids i-0123456789abcdef0
```

### Security Groups

```bash
# Create security group
aws ec2 create-security-group \
    --group-name my-sg \
    --description "My security group" \
    --vpc-id vpc-0123456789abcdef0

# Add inbound rules
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --cidr 10.0.0.0/8

aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Remove inbound rule
aws ec2 revoke-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 22 \
    --cidr 10.0.0.0/8
```

### AMI Management

```bash
# Create AMI from instance
aws ec2 create-image \
    --instance-id i-0123456789abcdef0 \
    --name "my-ami-$(date +%Y%m%d)" \
    --description "My AMI" \
    --no-reboot

# Copy AMI to another region
aws ec2 copy-image \
    --source-image-id ami-0123456789abcdef0 \
    --source-region us-east-1 \
    --region eu-west-1 \
    --name "my-ami-copy"

# Deregister AMI
aws ec2 deregister-image --image-id ami-0123456789abcdef0
```

## ECS (Elastic Container Service)

### Cluster Management

```bash
# Create cluster
aws ecs create-cluster \
    --cluster-name my-cluster \
    --capacity-providers FARGATE FARGATE_SPOT \
    --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1

# List clusters
aws ecs list-clusters

# Describe cluster
aws ecs describe-clusters --clusters my-cluster
```

### Task Definitions

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# task-definition.json:
{
  "family": "my-app",
  "networkMode": "awsvpc",
  "containerDefinitions": [{
    "name": "app",
    "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest",
    "portMappings": [{ "containerPort": 8080, "protocol": "tcp" }],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/my-app",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole"
}

# Deregister task definition
aws ecs deregister-task-definition --task-definition my-app:1
```

### Services

```bash
# Create service
aws ecs create-service \
    --cluster my-cluster \
    --service-name my-service \
    --task-definition my-app:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-123,subnet-456],securityGroups=[sg-789],assignPublicIp=ENABLED}" \
    --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=app,containerPort=8080

# Update service
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --task-definition my-app:2 \
    --force-new-deployment

# Delete service
aws ecs delete-service --cluster my-cluster --service my-service --force
```

### ECR (Container Registry)

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name my-app

# List images
aws ecr list-images --repository-name my-app

# Delete image
aws ecr batch-delete-image \
    --repository-name my-app \
    --image-ids imageTag=latest
```

## EKS (Elastic Kubernetes Service)

### Cluster Management

```bash
# Create cluster
aws eks create-cluster \
    --name my-cluster \
    --role-arn arn:aws:iam::123456789012:role/eks-cluster-role \
    --resources-vpc-config subnetIds=subnet-123,subnet-456,securityGroupIds=sg-789

# Update kubeconfig
aws eks update-kubeconfig --name my-cluster --region us-east-1

# Describe cluster
aws eks describe-cluster --name my-cluster

# Delete cluster
aws eks delete-cluster --name my-cluster
```

### Node Groups

```bash
# Create node group
aws eks create-nodegroup \
    --cluster-name my-cluster \
    --nodegroup-name my-nodes \
    --node-role arn:aws:iam::123456789012:role/eks-node-role \
    --subnets subnet-123 subnet-456 \
    --instance-types t3.medium \
    --scaling-config minSize=2,maxSize=10,desiredSize=3

# Update node group
aws eks update-nodegroup-config \
    --cluster-name my-cluster \
    --nodegroup-name my-nodes \
    --scaling-config minSize=2,maxSize=20,desiredSize=5

# Delete node group
aws eks delete-nodegroup --cluster-name my-cluster --nodegroup-name my-nodes
```

### Add-ons

```bash
# List add-ons
aws eks list-addons --cluster-name my-cluster

# Create add-on
aws eks create-addon \
    --cluster-name my-cluster \
    --addon-name vpc-cni \
    --addon-version v1.15.0-eksbuild.2

# Update add-on
aws eks update-addon \
    --cluster-name my-cluster \
    --addon-name vpc-cni \
    --addon-version v1.16.0-eksbuild.1
```

## Sources

- [EC2 User Guide](https://docs.aws.amazon.com/ec2/latest/userguide/)
- [ECS Developer Guide](https://docs.aws.amazon.com/ecs/latest/developerguide/)
- [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [ECR User Guide](https://docs.aws.amazon.com/ecr/latest/userguide/)
