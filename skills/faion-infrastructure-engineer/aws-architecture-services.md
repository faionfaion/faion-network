---
id: aws-architecture-services
name: "AWS Architecture - Services"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# AWS Architecture - Services

Production-ready patterns for EKS, RDS Aurora, Application Load Balancer, S3, and CloudFront.

## EKS Cluster

### Production Configuration

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "${var.project}-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  cluster_encryption_config = {
    provider_key_arn = aws_kms_key.eks.arn
    resources        = ["secrets"]
  }

  eks_managed_node_groups = {
    general = {
      name           = "general"
      instance_types = ["t3.medium"]
      min_size       = 2
      max_size       = 10
      desired_size   = 3
      disk_size      = 50
      labels         = { workload = "general" }
    }

    spot = {
      name           = "spot"
      instance_types = ["t3.medium", "t3.large", "t3a.medium"]
      capacity_type  = "SPOT"
      min_size       = 0
      max_size       = 10
      desired_size   = 2
      labels         = { workload = "spot" }
      taints         = [{ key = "spot", value = "true", effect = "NO_SCHEDULE" }]
    }
  }

  cluster_addons = {
    coredns            = { most_recent = true }
    kube-proxy         = { most_recent = true }
    vpc-cni            = { most_recent = true }
    aws-ebs-csi-driver = {
      most_recent              = true
      service_account_role_arn = module.ebs_csi_irsa.iam_role_arn
    }
  }

  enable_irsa               = true
  manage_aws_auth_configmap = true
  aws_auth_roles = [{
    rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/Admin"
    username = "admin"
    groups   = ["system:masters"]
  }]
}
```

### EKS Best Practices

- Use private subnets for nodes
- Enable IRSA for pod-level IAM
- Use managed add-ons (CoreDNS, kube-proxy, VPC CNI)
- Spot instances for non-critical workloads
- EBS CSI driver for persistent storage
- Enable Cluster Autoscaler

## RDS Aurora

### High-Availability Database

```hcl
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 8.0"

  name           = "${var.project}-${var.environment}"
  engine         = "aurora-postgresql"
  engine_version = "15.4"
  instance_class = "db.r6g.large"
  instances      = {
    1 = {}
    2 = { instance_class = "db.r6g.large" }
  }

  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name
  security_group_rules = {
    vpc_ingress = { cidr_blocks = module.vpc.private_subnets_cidr_blocks }
  }

  storage_encrypted   = true
  kms_key_id         = aws_kms_key.rds.arn

  backup_retention_period      = var.environment == "prod" ? 30 : 7
  preferred_backup_window      = "02:00-04:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"
  auto_minor_version_upgrade   = true

  deletion_protection = var.environment == "prod"
  skip_final_snapshot = var.environment != "prod"

  performance_insights_enabled          = true
  performance_insights_retention_period = var.environment == "prod" ? 731 : 7
  monitoring_interval                   = 60
  iam_database_authentication_enabled   = true
}
```

### RDS Best Practices

- Multi-AZ with at least 2 instances
- Enable encryption at rest and in transit
- 30 days backup retention for production
- Enable Performance Insights
- Use IAM authentication when possible
- Add read replicas for read-heavy workloads

## Application Load Balancer

### HTTPS with SSL Termination

```hcl
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"

  name    = "${var.project}-${var.environment}"
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets

  security_group_ingress_rules = {
    all_http  = { from_port = 80, to_port = 80, ip_protocol = "tcp", cidr_ipv4 = "0.0.0.0/0" }
    all_https = { from_port = 443, to_port = 443, ip_protocol = "tcp", cidr_ipv4 = "0.0.0.0/0" }
  }
  security_group_egress_rules = {
    all = { ip_protocol = "-1", cidr_ipv4 = module.vpc.vpc_cidr_block }
  }

  access_logs = {
    bucket = module.alb_logs.s3_bucket_id
    prefix = "alb"
  }

  listeners = {
    http-redirect = {
      port     = 80
      protocol = "HTTP"
      redirect = { port = "443", protocol = "HTTPS", status_code = "HTTP_301" }
    }
    https = {
      port            = 443
      protocol        = "HTTPS"
      certificate_arn = module.acm.acm_certificate_arn
      forward         = { target_group_key = "app" }
    }
  }

  target_groups = {
    app = {
      name_prefix          = "app-"
      protocol             = "HTTP"
      port                 = 8000
      target_type          = "ip"
      deregistration_delay = 30
      health_check = {
        enabled             = true
        path                = "/health"
        port                = "traffic-port"
        healthy_threshold   = 2
        unhealthy_threshold = 3
        timeout             = 5
        interval            = 30
        matcher             = "200"
      }
    }
  }
}
```

### ALB Best Practices

- Redirect HTTP to HTTPS
- Use ACM for certificates
- Store access logs in S3
- Proper health check endpoints
- Use `ip` target type for EKS/Fargate
- 30s deregistration delay for graceful shutdown

## S3 with CloudFront

### Static Assets Distribution

```hcl
module "s3_static" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.0"

  bucket = "${var.project}-${var.environment}-static"

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  versioning = { enabled = true }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = { sse_algorithm = "AES256" }
    }
  }

  lifecycle_rule = [{
    id      = "archive"
    enabled = true
    transition = [
      { days = 90, storage_class = "STANDARD_IA" },
      { days = 180, storage_class = "GLACIER" }
    ]
    noncurrent_version_expiration = { days = 30 }
  }]

  cors_rule = [{
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["https://${var.domain}"]
    allowed_headers = ["*"]
    max_age_seconds = 3600
  }]
}

module "cloudfront" {
  source  = "terraform-aws-modules/cloudfront/aws"
  version = "~> 3.0"

  aliases             = ["static.${var.domain}"]
  comment             = "${var.project} static assets"
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_100"
  retain_on_delete    = false
  wait_for_deployment = false

  create_origin_access_control = true
  origin_access_control = {
    s3_oac = {
      description      = "CloudFront access to S3"
      origin_type      = "s3"
      signing_behavior = "always"
      signing_protocol = "sigv4"
    }
  }

  origin = {
    s3_static = {
      domain_name           = module.s3_static.s3_bucket_bucket_regional_domain_name
      origin_access_control = "s3_oac"
    }
  }

  default_cache_behavior = {
    target_origin_id       = "s3_static"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6"  # CachingOptimized
    origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"  # CORS-S3Origin
  }

  viewer_certificate = {
    acm_certificate_arn = module.acm_cloudfront.acm_certificate_arn
    ssl_support_method  = "sni-only"
  }
}
```

### S3/CloudFront Best Practices

- Block public S3 access
- Use Origin Access Control (OAC, not legacy OAI)
- Enable versioning for rollback
- Lifecycle policies for cost optimization
- Enable CloudFront compression
- Use managed cache policies

## Common Pitfalls

1. **Overly permissive IAM:** Using `*` resources and actions. Always scope to specific ARNs.
2. **Public S3 buckets:** Enable block public access. Use CloudFront or presigned URLs.
3. **Single AZ deployments:** Critical workloads must span multiple AZs.
4. **No encryption:** Encrypt all storage and data transfer.
5. **Missing monitoring:** Without CloudWatch alarms, issues go unnoticed.
6. **Hardcoded credentials:** Use IAM roles, Secrets Manager, or Parameter Store.

## Sources

- [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [RDS Aurora User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.BestPractices.html)
- [ALB Best Practices](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/best-practices.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/best-practices.html)
