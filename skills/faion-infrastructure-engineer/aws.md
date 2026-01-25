---
name: faion-aws-cli-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS CLI Skill

AWS CLI operations for cloud infrastructure management: compute, storage, serverless, containers, databases, and monitoring.

## Configuration

### Installation

```bash
# Install AWS CLI v2 (Linux)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify
aws --version
```

### Profile Management

```bash
# Configure default profile
aws configure
# Input: Access Key ID, Secret Access Key, Region, Output format

# Configure named profile
aws configure --profile production

# List profiles
aws configure list-profiles

# Use specific profile
aws s3 ls --profile production
export AWS_PROFILE=production
```

### Environment Variables

```bash
# Authentication
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_SESSION_TOKEN="your-session-token"

# Region
export AWS_DEFAULT_REGION="us-east-1"
export AWS_REGION="us-east-1"

# Output format
export AWS_DEFAULT_OUTPUT="json"  # json | text | table | yaml
```

### Credentials File

```ini
# ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

[production]
aws_access_key_id = PROD_ACCESS_KEY
aws_secret_access_key = PROD_SECRET_KEY

[development]
role_arn = arn:aws:iam::123456789012:role/DevRole
source_profile = default
```

### Config File

```ini
# ~/.aws/config
[default]
region = us-east-1
output = json

[profile production]
region = eu-west-1
output = table

[profile development]
region = us-west-2
role_arn = arn:aws:iam::123456789012:role/DevRole
source_profile = default
```

## Service References

| File | Services | Description |
|------|----------|-------------|
| [aws-ec2-ecs.md](aws-ec2-ecs.md) | EC2, ECS, EKS, ECR | Compute: instances, containers, orchestration |
| [aws-lambda.md](aws-lambda.md) | Lambda | Serverless functions, layers, triggers |
| [aws-s3-storage.md](aws-s3-storage.md) | S3, RDS, Aurora | Storage, databases, backups |
| [aws-networking.md](aws-networking.md) | IAM, CloudFormation, CloudWatch | Networking, infrastructure, monitoring |

## Deployment Pattern

```bash
# Build and push Docker image
docker build -t my-app:latest .
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI
docker tag my-app:latest $ECR_URI/my-app:latest
docker push $ECR_URI/my-app:latest

# Update ECS service
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --force-new-deployment

# Wait for deployment
aws ecs wait services-stable --cluster my-cluster --services my-service
```

## Sources

- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS Best Practices](https://aws.amazon.com/architecture/well-architected/)
- [AWS CLI Configuration Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [AWS Environment Variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)
