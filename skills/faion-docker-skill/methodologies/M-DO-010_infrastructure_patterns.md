# M-DO-010: Infrastructure Patterns

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #infrastructure, #patterns, #architecture, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Infrastructure grows organically without clear patterns. Teams reinvent solutions, create inconsistent environments, and struggle with scaling and reliability.

## Promise

After this methodology, you will apply proven infrastructure patterns. Your systems will be scalable, resilient, and maintainable.

## Overview

Infrastructure patterns are reusable solutions to common problems. This methodology covers networking, compute, data, and reliability patterns.

---

## Framework

### Step 1: Network Patterns

```
Three-Tier Network Architecture:

Public Subnets (DMZ)
├── Load Balancers
├── Bastion Hosts
└── NAT Gateways

Private Subnets (Application)
├── Application Servers
├── API Servers
└── Workers

Private Subnets (Data)
├── Databases
├── Cache Clusters
└── Search Engines
```

```hcl
# Multi-AZ VPC Pattern
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "production"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false  # One per AZ for HA

  enable_dns_hostnames = true
  enable_dns_support   = true

  # Database subnet group
  create_database_subnet_group = true
}
```

### Step 2: Load Balancing Patterns

```hcl
# Application Load Balancer Pattern
resource "aws_lb" "app" {
  name               = "app-alb"
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets

  enable_deletion_protection = true

  access_logs {
    bucket  = aws_s3_bucket.logs.id
    prefix  = "alb"
    enabled = true
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# HTTP to HTTPS redirect
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# Path-based routing
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}
```

### Step 3: Auto Scaling Patterns

```hcl
# Auto Scaling with Target Tracking
resource "aws_autoscaling_group" "app" {
  name                = "app-asg"
  desired_capacity    = 2
  min_size            = 2
  max_size            = 10
  vpc_zone_identifier = module.vpc.private_subnets
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 75
    }
  }

  tag {
    key                 = "Name"
    value               = "app-asg"
    propagate_at_launch = true
  }
}

# CPU-based scaling
resource "aws_autoscaling_policy" "cpu" {
  name                   = "cpu-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 70.0
  }
}

# Request-based scaling
resource "aws_autoscaling_policy" "requests" {
  name                   = "request-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = "${aws_lb.app.arn_suffix}/${aws_lb_target_group.app.arn_suffix}"
    }
    target_value = 1000.0
  }
}
```

### Step 4: Database Patterns

```hcl
# Multi-AZ RDS Pattern
resource "aws_db_instance" "main" {
  identifier = "app-db"

  engine         = "postgres"
  engine_version = "16.1"
  instance_class = "db.t3.medium"

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "app"
  username = "admin"
  password = random_password.db.result

  multi_az               = true
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "app-db-final"

  performance_insights_enabled = true
  monitoring_interval          = 60
  monitoring_role_arn          = aws_iam_role.rds_monitoring.arn
}

# Read Replica Pattern
resource "aws_db_instance" "replica" {
  identifier = "app-db-replica"

  replicate_source_db = aws_db_instance.main.identifier
  instance_class      = "db.t3.medium"

  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = 0  # No backups for replica
  skip_final_snapshot     = true
}
```

### Step 5: Caching Patterns

```hcl
# ElastiCache Redis Cluster Pattern
resource "aws_elasticache_replication_group" "main" {
  replication_group_id = "app-redis"
  description          = "Redis cluster for app"

  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.t3.medium"
  num_cache_clusters   = 2  # 1 primary + 1 replica

  automatic_failover_enabled = true
  multi_az_enabled           = true

  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = random_password.redis.result

  snapshot_retention_limit = 7
  snapshot_window          = "04:00-05:00"
}

# Cache-Aside Pattern (Application Level)
# 1. Check cache
# 2. If miss, query database
# 3. Store in cache
# 4. Return result
```

### Step 6: High Availability Patterns

```
Multi-Region Active-Passive:

Region A (Primary)           Region B (DR)
├── ALB                      ├── ALB (standby)
├── ECS/EC2                  ├── ECS/EC2 (minimal)
├── RDS (primary)      →     ├── RDS (read replica)
├── ElastiCache              ├── ElastiCache
└── S3 (origin)        →     └── S3 (replica)

Route 53 Health Checks + Failover
```

```hcl
# Route 53 Failover Pattern
resource "aws_route53_health_check" "primary" {
  fqdn              = "primary.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_record" "app" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier  = "primary"
  health_check_id = aws_route53_health_check.primary.id

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "app_failover" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "secondary"

  alias {
    name                   = aws_lb.secondary.dns_name
    zone_id                = aws_lb.secondary.zone_id
    evaluate_target_health = true
  }
}
```

---

## Templates

### Blue-Green Deployment

```hcl
# Blue-Green with ALB
resource "aws_lb_target_group" "blue" {
  name     = "app-blue"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
  }
}

resource "aws_lb_target_group" "green" {
  name     = "app-green"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
  }
}

# Switch traffic by changing the forward action
resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type = "forward"

    forward {
      target_group {
        arn    = aws_lb_target_group.blue.arn
        weight = var.blue_weight  # 100 for blue, 0 for green
      }
      target_group {
        arn    = aws_lb_target_group.green.arn
        weight = var.green_weight  # 0 for blue, 100 for green
      }
    }
  }
}
```

### Circuit Breaker Pattern

```yaml
# AWS App Mesh / Envoy configuration
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualNode
metadata:
  name: app-node
spec:
  listeners:
    - portMapping:
        port: 3000
        protocol: http
      outlierDetection:
        baseEjectionDuration: 30s
        interval: 10s
        maxEjectionPercent: 100
        maxServerErrors: 5
```

---

## Examples

### Microservices Infrastructure

```
                    ┌─────────────┐
                    │   Route 53  │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │     ALB     │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │ Service │       │ Service │       │ Service │
    │    A    │       │    B    │       │    C    │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
         │      ┌──────────┴──────────┐      │
         │      │                     │      │
    ┌────┴──────┴─┐               ┌───┴──────┴───┐
    │   RDS       │               │  ElastiCache │
    └─────────────┘               └──────────────┘
```

### Serverless Event-Driven

```
                    ┌─────────────┐
                    │  API Gateway│
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │   Lambda    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
         │   SQS   │  │  SNS    │  │ DynamoDB│
         └────┬────┘  └────┬────┘  └─────────┘
              │            │
         ┌────┴────┐  ┌────┴────┐
         │ Worker  │  │ Lambda  │
         │ Lambda  │  │ (Fan-out)│
         └─────────┘  └─────────┘
```

---

## Common Mistakes

1. **Single AZ deployment** - Always use multi-AZ
2. **No auto scaling** - Fixed capacity wastes money
3. **Direct database access** - Use connection pooling
4. **No health checks** - Unhealthy instances receive traffic
5. **Public databases** - Always use private subnets

---

## Checklist

- [ ] Multi-AZ for all critical components
- [ ] Load balancer with health checks
- [ ] Auto scaling configured
- [ ] Database in private subnet
- [ ] Encryption at rest and in transit
- [ ] Backup and recovery tested
- [ ] Monitoring and alerting
- [ ] DR plan documented

---

## Next Steps

- M-DO-009: Terraform Basics
- M-DO-005: Kubernetes Basics
- M-DO-001: GitHub Actions

---

*Methodology M-DO-010 v1.0*
