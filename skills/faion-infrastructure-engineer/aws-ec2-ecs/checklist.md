# AWS EC2 & ECS Checklist

Step-by-step implementation guides for EC2 and ECS deployments.

## EC2 Instance Setup

### Pre-Launch

- [ ] Select appropriate instance type (consider Graviton for cost savings)
- [ ] Choose AMI (Amazon Linux 2023, Ubuntu 24.04, custom)
- [ ] Create/select key pair for SSH access
- [ ] Design VPC and subnet placement
- [ ] Create security groups with least-privilege rules
- [ ] Create IAM instance profile (not access keys)
- [ ] Plan tagging strategy (Name, Environment, Project, Owner)

### Launch Configuration

- [ ] Configure instance metadata service (IMDSv2 required)
- [ ] Set up user data script for initialization
- [ ] Configure EBS volumes (gp3 recommended)
- [ ] Enable detailed monitoring if needed
- [ ] Configure placement group (for performance)
- [ ] Enable termination protection for production

### Post-Launch

- [ ] Verify instance running and passing status checks
- [ ] Test SSH/SSM connectivity
- [ ] Install and configure CloudWatch agent
- [ ] Configure log shipping to CloudWatch Logs
- [ ] Set up backup schedule (AWS Backup or snapshots)
- [ ] Add to load balancer target group

---

## ECS Fargate Service Setup

### Prerequisites

- [ ] ECR repository created
- [ ] Docker image built and pushed
- [ ] VPC with private subnets configured
- [ ] ALB or NLB created (if public-facing)
- [ ] ECS task execution role created
- [ ] ECS task role created (for AWS API access)
- [ ] CloudWatch log group created

### Cluster Setup

- [ ] Create ECS cluster
- [ ] Configure capacity providers (FARGATE, FARGATE_SPOT)
- [ ] Enable Container Insights
- [ ] Set default capacity provider strategy

### Task Definition

- [ ] Define task family name
- [ ] Set network mode to `awsvpc`
- [ ] Configure CPU and memory (right-sized)
- [ ] Define container definitions:
  - [ ] Image URI with specific tag (immutable)
  - [ ] Port mappings
  - [ ] Environment variables (use Secrets Manager for secrets)
  - [ ] Health check command
  - [ ] Log configuration (awslogs driver)
  - [ ] Resource limits
  - [ ] Read-only root filesystem
  - [ ] Non-root user
- [ ] Configure execution role ARN
- [ ] Configure task role ARN
- [ ] Set ephemeral storage if needed

### Service Configuration

- [ ] Create service in cluster
- [ ] Set desired task count
- [ ] Configure deployment settings:
  - [ ] Minimum healthy percent (100% for zero-downtime)
  - [ ] Maximum percent (200% for rolling updates)
  - [ ] Deployment circuit breaker
- [ ] Configure network:
  - [ ] Select private subnets
  - [ ] Attach security groups
  - [ ] Disable public IP assignment
- [ ] Configure load balancer:
  - [ ] Select target group
  - [ ] Container name and port
  - [ ] Health check grace period
- [ ] Configure service discovery (optional)

### Auto Scaling

- [ ] Register scalable target
- [ ] Configure target tracking scaling:
  - [ ] CPU utilization target
  - [ ] Memory utilization target
  - [ ] Request count per target
- [ ] Set scale-in/scale-out cooldown
- [ ] Configure min/max capacity

### Validation

- [ ] Verify tasks running in service
- [ ] Check task health in target group
- [ ] Verify CloudWatch logs streaming
- [ ] Test application endpoint
- [ ] Verify auto-scaling triggers
- [ ] Test deployment rollback

---

## Security Hardening Checklist

### IAM

- [ ] Use IAM roles, not access keys
- [ ] Apply least-privilege policies
- [ ] Enable MFA for console access
- [ ] Use AWS Access Analyzer

### Network

- [ ] Tasks in private subnets
- [ ] Security groups with minimal rules
- [ ] VPC endpoints for AWS services
- [ ] No direct internet access for tasks

### Container

- [ ] Scan images for vulnerabilities
- [ ] Use immutable image tags
- [ ] Run as non-root user
- [ ] Read-only root filesystem
- [ ] No privileged containers
- [ ] Resource limits configured

### Secrets

- [ ] Store secrets in Secrets Manager/Parameter Store
- [ ] Reference secrets in task definition
- [ ] Rotate secrets automatically
- [ ] No secrets in environment variables

### Logging & Monitoring

- [ ] CloudWatch Logs enabled
- [ ] Container Insights enabled
- [ ] CloudTrail logging for API calls
- [ ] Alarm on failed deployments
- [ ] Alarm on unhealthy targets

---

## Cost Optimization Checklist

### EC2

- [ ] Use Graviton instances where possible
- [ ] Right-size instances (use Compute Optimizer)
- [ ] Use Reserved Instances for baseline
- [ ] Use Spot Instances for fault-tolerant workloads
- [ ] Enable instance stop/start scheduling
- [ ] Delete unused EBS volumes
- [ ] Use gp3 instead of gp2

### ECS Fargate

- [ ] Right-size task CPU/memory
- [ ] Use FARGATE_SPOT for batch/dev workloads
- [ ] Enable auto-scaling (don't over-provision)
- [ ] Use bin-packing for EC2 launch type
- [ ] Review task execution patterns
- [ ] Delete unused task definitions

### General

- [ ] Enable Cost Explorer
- [ ] Set up billing alarms
- [ ] Tag resources for cost allocation
- [ ] Review unused/idle resources weekly

---

*AWS EC2 & ECS Checklist | faion-infrastructure-engineer*
