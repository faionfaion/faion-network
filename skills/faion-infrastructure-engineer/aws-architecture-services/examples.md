# AWS Architecture Services - Examples

Production-ready Terraform configurations for AWS services.

## EKS Cluster

### Production Configuration

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.project}-${var.environment}"
  cluster_version = "1.31"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Endpoint access
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  # Secrets encryption
  cluster_encryption_config = {
    provider_key_arn = aws_kms_key.eks.arn
    resources        = ["secrets"]
  }

  # Managed node groups
  eks_managed_node_groups = {
    # General workloads - Graviton for cost efficiency
    general = {
      name           = "general"
      instance_types = ["t4g.medium", "t4g.large"]  # Graviton
      ami_type       = "AL2023_ARM_64_STANDARD"
      min_size       = 2
      max_size       = 10
      desired_size   = 3
      disk_size      = 50
      labels         = { workload = "general" }
    }

    # Spot instances for fault-tolerant workloads
    spot = {
      name           = "spot"
      instance_types = ["t4g.medium", "t4g.large", "m6g.medium"]
      ami_type       = "AL2023_ARM_64_STANDARD"
      capacity_type  = "SPOT"
      min_size       = 0
      max_size       = 20
      desired_size   = 2
      labels         = { workload = "spot" }
      taints = [{
        key    = "spot"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  # Managed add-ons
  cluster_addons = {
    coredns    = { most_recent = true }
    kube-proxy = { most_recent = true }
    vpc-cni    = { most_recent = true }
    aws-ebs-csi-driver = {
      most_recent              = true
      service_account_role_arn = module.ebs_csi_irsa.iam_role_arn
    }
  }

  # IRSA and auth
  enable_irsa               = true
  manage_aws_auth_configmap = true

  aws_auth_roles = [{
    rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/Admin"
    username = "admin"
    groups   = ["system:masters"]
  }]

  tags = local.common_tags
}
```

## RDS Aurora

### High-Availability PostgreSQL

```hcl
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 9.0"

  name           = "${var.project}-${var.environment}"
  engine         = "aurora-postgresql"
  engine_version = "16.4"

  # Graviton instances for better price-performance
  instance_class = "db.r7g.large"

  instances = {
    writer = {}
    reader = {
      instance_class = "db.r7g.large"
      promotion_tier = 1
    }
  }

  # Networking
  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name

  security_group_rules = {
    vpc_ingress = {
      cidr_blocks = module.vpc.private_subnets_cidr_blocks
    }
  }

  # Encryption
  storage_encrypted = true
  kms_key_id        = aws_kms_key.rds.arn

  # Backup and maintenance
  backup_retention_period      = var.environment == "prod" ? 30 : 7
  preferred_backup_window      = "02:00-04:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"
  auto_minor_version_upgrade   = true

  # Protection
  deletion_protection = var.environment == "prod"
  skip_final_snapshot = var.environment != "prod"

  # Monitoring
  performance_insights_enabled          = true
  performance_insights_retention_period = var.environment == "prod" ? 731 : 7
  monitoring_interval                   = 60

  # Authentication
  iam_database_authentication_enabled = true

  tags = local.common_tags
}
```

## Application Load Balancer

### HTTPS with SSL Termination

```hcl
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"

  name    = "${var.project}-${var.environment}"
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets

  # Security groups
  security_group_ingress_rules = {
    all_http = {
      from_port   = 80
      to_port     = 80
      ip_protocol = "tcp"
      cidr_ipv4   = "0.0.0.0/0"
    }
    all_https = {
      from_port   = 443
      to_port     = 443
      ip_protocol = "tcp"
      cidr_ipv4   = "0.0.0.0/0"
    }
  }

  security_group_egress_rules = {
    all = {
      ip_protocol = "-1"
      cidr_ipv4   = module.vpc.vpc_cidr_block
    }
  }

  # Access logs
  access_logs = {
    bucket = module.alb_logs.s3_bucket_id
    prefix = "alb"
  }

  # Listeners
  listeners = {
    http-redirect = {
      port     = 80
      protocol = "HTTP"
      redirect = {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }
    https = {
      port            = 443
      protocol        = "HTTPS"
      certificate_arn = module.acm.acm_certificate_arn
      ssl_policy      = "ELBSecurityPolicy-TLS13-1-2-2021-06"
      forward = {
        target_group_key = "app"
      }
    }
  }

  # Target groups
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

  tags = local.common_tags
}
```

## S3 with CloudFront

### Static Assets Distribution

```hcl
# S3 Bucket
module "s3_static" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket = "${var.project}-${var.environment}-static"

  # Block all public access
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  # Versioning
  versioning = { enabled = true }

  # Encryption
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  # Lifecycle rules
  lifecycle_rule = [{
    id      = "archive"
    enabled = true

    transition = [
      { days = 90, storage_class = "STANDARD_IA" },
      { days = 180, storage_class = "GLACIER" }
    ]

    noncurrent_version_expiration = { days = 30 }
  }]

  # CORS
  cors_rule = [{
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["https://${var.domain}"]
    allowed_headers = ["*"]
    max_age_seconds = 3600
  }]

  tags = local.common_tags
}

# CloudFront Distribution
module "cloudfront" {
  source  = "terraform-aws-modules/cloudfront/aws"
  version = "~> 3.0"

  aliases             = ["static.${var.domain}"]
  comment             = "${var.project} static assets"
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http2and3"
  price_class         = "PriceClass_100"
  retain_on_delete    = false
  wait_for_deployment = false

  # Origin Access Control (OAC) - replaces OAI
  create_origin_access_control = true
  origin_access_control = {
    s3_oac = {
      description      = "CloudFront access to S3"
      origin_type      = "s3"
      signing_behavior = "always"
      signing_protocol = "sigv4"
    }
  }

  # Origins
  origin = {
    s3_static = {
      domain_name           = module.s3_static.s3_bucket_bucket_regional_domain_name
      origin_access_control = "s3_oac"
    }
  }

  # Cache behavior
  default_cache_behavior = {
    target_origin_id       = "s3_static"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    # Managed policies
    cache_policy_id            = "658327ea-f89d-4fab-a63d-7e88639e58f6"  # CachingOptimized
    origin_request_policy_id   = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"  # CORS-S3Origin
    response_headers_policy_id = "5cc3b908-e619-4b99-88e5-2cf7f45965bd"  # CORS-with-preflight
  }

  # SSL Certificate
  viewer_certificate = {
    acm_certificate_arn      = module.acm_cloudfront.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  tags = local.common_tags
}
```

## EventBridge Event-Driven Architecture

### Cross-Service Event Routing

```hcl
# Custom Event Bus
resource "aws_cloudwatch_event_bus" "main" {
  name = "${var.project}-${var.environment}"
  tags = local.common_tags
}

# Archive for replay
resource "aws_cloudwatch_event_archive" "main" {
  name             = "${var.project}-${var.environment}-archive"
  event_source_arn = aws_cloudwatch_event_bus.main.arn
  retention_days   = 30
}

# Event Rule - Order Created
resource "aws_cloudwatch_event_rule" "order_created" {
  name           = "order-created"
  event_bus_name = aws_cloudwatch_event_bus.main.name

  event_pattern = jsonencode({
    source      = ["com.${var.project}.orders"]
    detail-type = ["Order Created"]
  })

  tags = local.common_tags
}

# Target - Lambda for notifications
resource "aws_cloudwatch_event_target" "notify_customer" {
  rule           = aws_cloudwatch_event_rule.order_created.name
  event_bus_name = aws_cloudwatch_event_bus.main.name
  target_id      = "notify-customer"
  arn            = aws_lambda_function.notify_customer.arn

  # Dead-letter queue
  dead_letter_config {
    arn = aws_sqs_queue.dlq.arn
  }

  # Retry policy
  retry_policy {
    maximum_event_age_in_seconds = 3600
    maximum_retry_attempts       = 3
  }
}

# Target - SQS for analytics
resource "aws_cloudwatch_event_target" "analytics" {
  rule           = aws_cloudwatch_event_rule.order_created.name
  event_bus_name = aws_cloudwatch_event_bus.main.name
  target_id      = "analytics-queue"
  arn            = aws_sqs_queue.analytics.arn

  # Input transformer
  input_transformer {
    input_paths = {
      orderId   = "$.detail.orderId"
      timestamp = "$.time"
    }
    input_template = <<EOF
{
  "event_type": "order_created",
  "order_id": <orderId>,
  "event_time": <timestamp>
}
EOF
  }
}
```

## Lambda with API Gateway

### Serverless API

```hcl
# Lambda Function
module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 7.0"

  function_name = "${var.project}-${var.environment}-api"
  handler       = "main.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]  # Graviton

  source_path = "${path.module}/src"

  # VPC configuration (if needed)
  vpc_subnet_ids         = module.vpc.private_subnets
  vpc_security_group_ids = [aws_security_group.lambda.id]

  # Environment
  environment_variables = {
    ENVIRONMENT = var.environment
    DB_SECRET   = aws_secretsmanager_secret.db.arn
  }

  # Permissions
  attach_policy_statements = true
  policy_statements = {
    secrets = {
      effect    = "Allow"
      actions   = ["secretsmanager:GetSecretValue"]
      resources = [aws_secretsmanager_secret.db.arn]
    }
  }

  # Provisioned concurrency (for production)
  provisioned_concurrent_executions = var.environment == "prod" ? 10 : 0

  tags = local.common_tags
}

# API Gateway
module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "~> 5.0"

  name          = "${var.project}-${var.environment}"
  protocol_type = "HTTP"

  # CORS
  cors_configuration = {
    allow_headers = ["content-type", "authorization"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_origins = ["https://${var.domain}"]
  }

  # Domain
  domain_name                 = "api.${var.domain}"
  domain_name_certificate_arn = module.acm.acm_certificate_arn

  # Routes
  routes = {
    "GET /health" = {
      integration = {
        uri = module.lambda.lambda_function_arn
      }
    }
    "ANY /{proxy+}" = {
      integration = {
        uri = module.lambda.lambda_function_arn
      }
    }
  }

  tags = local.common_tags
}
```

## Step Functions Orchestration

### Order Processing Workflow

```hcl
resource "aws_sfn_state_machine" "order_processing" {
  name     = "${var.project}-${var.environment}-order-processing"
  role_arn = aws_iam_role.step_functions.arn

  definition = jsonencode({
    Comment = "Order processing workflow"
    StartAt = "ValidateOrder"
    States = {
      ValidateOrder = {
        Type     = "Task"
        Resource = module.lambda_validate.lambda_function_arn
        Next     = "ProcessPayment"
        Catch = [{
          ErrorEquals = ["ValidationError"]
          Next        = "OrderFailed"
        }]
      }
      ProcessPayment = {
        Type     = "Task"
        Resource = module.lambda_payment.lambda_function_arn
        Next     = "FulfillOrder"
        Retry = [{
          ErrorEquals     = ["PaymentServiceError"]
          IntervalSeconds = 5
          MaxAttempts     = 3
          BackoffRate     = 2
        }]
        Catch = [{
          ErrorEquals = ["PaymentFailed"]
          Next        = "OrderFailed"
        }]
      }
      FulfillOrder = {
        Type     = "Task"
        Resource = module.lambda_fulfill.lambda_function_arn
        Next     = "OrderComplete"
      }
      OrderComplete = {
        Type = "Succeed"
      }
      OrderFailed = {
        Type  = "Fail"
        Error = "OrderProcessingFailed"
        Cause = "Order could not be processed"
      }
    }
  })

  tags = local.common_tags
}
```

---

*AWS Architecture Services Examples | faion-infrastructure-engineer*
