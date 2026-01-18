# M-DO-007: AWS EC2 Fundamentals

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #aws, #ec2, #cloud, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Managing virtual servers requires understanding instance types, networking, security, and cost optimization. Wrong choices lead to overspending or poor performance.

## Promise

After this methodology, you will provision and manage EC2 instances effectively. Your infrastructure will be secure, scalable, and cost-optimized.

## Overview

Amazon EC2 provides resizable compute capacity in the cloud. This methodology covers instance management, networking, security groups, and best practices.

---

## Framework

### Step 1: AWS CLI Setup

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json

# Verify
aws sts get-caller-identity
```

### Step 2: Instance Types

```
Instance Type Naming: [Family][Generation].[Size]
Example: t3.medium

Families:
├── General Purpose (t3, t3a, m5, m6i)
│   └── Balanced compute, memory, networking
├── Compute Optimized (c5, c6i)
│   └── CPU-intensive workloads
├── Memory Optimized (r5, r6i, x2idn)
│   └── Large databases, caching
├── Storage Optimized (i3, d2)
│   └── High I/O workloads
└── Accelerated (p4, g4, inf1)
    └── ML, graphics, video

Sizes (from t3 family):
├── nano    - 0.5 GB RAM, 2 vCPU
├── micro   - 1 GB RAM, 2 vCPU
├── small   - 2 GB RAM, 2 vCPU
├── medium  - 4 GB RAM, 2 vCPU
├── large   - 8 GB RAM, 2 vCPU
├── xlarge  - 16 GB RAM, 4 vCPU
└── 2xlarge - 32 GB RAM, 8 vCPU
```

### Step 3: Launch Instance (CLI)

```bash
# Find latest Amazon Linux 2023 AMI
AMI_ID=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-2023*-x86_64" \
  --query "Images | sort_by(@, &CreationDate) | [-1].ImageId" \
  --output text)

# Create key pair
aws ec2 create-key-pair \
  --key-name my-key \
  --query "KeyMaterial" \
  --output text > my-key.pem
chmod 400 my-key.pem

# Launch instance
aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-xxx \
  --subnet-id subnet-xxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-server}]' \
  --user-data file://user-data.sh
```

### Step 4: User Data (Bootstrap)

```bash
#!/bin/bash
# user-data.sh

# Update system
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone and run application
cd /home/ec2-user
git clone https://github.com/user/app.git
cd app
docker-compose up -d

# Install CloudWatch agent
yum install -y amazon-cloudwatch-agent
```

### Step 5: Security Groups

```bash
# Create security group
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Web server security group" \
  --vpc-id vpc-xxx

# Allow SSH (restrict to your IP)
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 22 \
  --cidr 203.0.113.0/32

# Allow HTTP/HTTPS
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

### Step 6: Elastic IP and DNS

```bash
# Allocate Elastic IP
aws ec2 allocate-address --domain vpc

# Associate with instance
aws ec2 associate-address \
  --instance-id i-xxx \
  --allocation-id eipalloc-xxx

# Or use dynamic DNS with Route 53
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123 \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "1.2.3.4"}]
      }
    }]
  }'
```

---

## Templates

### EC2 Instance with Terraform

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.web.id]
  subnet_id              = var.subnet_id

  user_data = file("user-data.sh")

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name        = "web-server"
    Environment = var.environment
  }
}

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web server security group"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_eip" "web" {
  instance = aws_instance.web.id
  domain   = "vpc"
}

output "public_ip" {
  value = aws_eip.web.public_ip
}
```

### Auto Scaling Group

```hcl
resource "aws_launch_template" "web" {
  name_prefix   = "web-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = "t3.small"

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(file("user-data.sh"))

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size = 20
      volume_type = "gp3"
      encrypted   = true
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "web-asg"
    }
  }
}

resource "aws_autoscaling_group" "web" {
  name                = "web-asg"
  desired_capacity    = 2
  min_size            = 1
  max_size            = 4
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.web.arn]

  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "web-asg"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
}
```

---

## Examples

### Instance Management

```bash
# List instances
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=web-*" \
  --query "Reservations[].Instances[].{ID:InstanceId,State:State.Name,IP:PublicIpAddress}"

# Start/Stop/Terminate
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx
aws ec2 terminate-instances --instance-ids i-xxx

# Connect via SSH
ssh -i my-key.pem ec2-user@1.2.3.4

# Connect via Session Manager (no SSH key needed)
aws ssm start-session --target i-xxx

# Get instance metadata (from inside EC2)
curl http://169.254.169.254/latest/meta-data/instance-id
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### Cost Optimization

```bash
# Spot Instances (up to 90% discount)
aws ec2 run-instances \
  --instance-type t3.medium \
  --instance-market-options '{"MarketType":"spot","SpotOptions":{"MaxPrice":"0.02"}}' \
  ...

# Reserved Instances
# Purchase via Console for predictable workloads

# Savings Plans
# Flexible commitment for compute usage

# Right-sizing
aws compute-optimizer get-ec2-instance-recommendations \
  --instance-arns arn:aws:ec2:us-east-1:123456789:instance/i-xxx
```

---

## Common Mistakes

1. **Open security groups** - Never 0.0.0.0/0 for SSH
2. **No backups** - Enable EBS snapshots
3. **Wrong instance type** - Profile before choosing
4. **No termination protection** - Enable for production
5. **Unencrypted storage** - Enable EBS encryption

---

## Checklist

- [ ] IAM role attached (not access keys)
- [ ] Security group least privilege
- [ ] EBS encryption enabled
- [ ] CloudWatch monitoring
- [ ] Termination protection (production)
- [ ] Regular AMI backups
- [ ] Right-sized instance type
- [ ] Cost allocation tags

---

## Next Steps

- M-DO-008: AWS Lambda
- M-DO-009: Terraform Basics
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-007 v1.0*
