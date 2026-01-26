# AWS Architecture Examples

## Three-Tier VPC Architecture

```hcl
# Three-tier VPC architecture with Terraform
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project}-${var.environment}"
  cidr = "10.0.0.0/16"

  azs             = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"
  one_nat_gateway_per_az = var.environment == "prod"

  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Flow Logs
  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true
  flow_log_max_aggregation_interval    = 60

  # Tags for Kubernetes
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}
```

---

## EKS Cluster (Kubernetes)

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.project}-${var.environment}"
  cluster_version = "1.31"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  # Encryption
  cluster_encryption_config = {
    provider_key_arn = aws_kms_key.eks.arn
    resources        = ["secrets"]
  }

  # Managed node groups
  eks_managed_node_groups = {
    general = {
      name           = "general"
      instance_types = ["m7g.medium"]  # Graviton
      ami_type       = "AL2023_ARM_64_STANDARD"

      min_size     = 2
      max_size     = 10
      desired_size = 3

      disk_size = 50

      labels = {
        workload = "general"
      }
    }

    spot = {
      name           = "spot"
      instance_types = ["m7g.medium", "m7g.large", "m6g.medium"]
      capacity_type  = "SPOT"
      ami_type       = "AL2023_ARM_64_STANDARD"

      min_size     = 0
      max_size     = 10
      desired_size = 2

      labels = {
        workload = "spot"
      }

      taints = [{
        key    = "spot"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  # Add-ons
  cluster_addons = {
    coredns                = { most_recent = true }
    kube-proxy             = { most_recent = true }
    vpc-cni                = { most_recent = true }
    aws-ebs-csi-driver     = { most_recent = true }
    eks-pod-identity-agent = { most_recent = true }
  }

  # Pod Identity
  enable_cluster_creator_admin_permissions = true
}
```

---

## Aurora Serverless v2 (PostgreSQL)

```hcl
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 9.0"

  name           = "${var.project}-${var.environment}"
  engine         = "aurora-postgresql"
  engine_version = "16.4"
  engine_mode    = "provisioned"

  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name

  security_group_rules = {
    vpc_ingress = {
      cidr_blocks = module.vpc.private_subnets_cidr_blocks
    }
  }

  # Serverless v2 configuration
  serverlessv2_scaling_configuration = {
    min_capacity = 0.5
    max_capacity = 16
  }

  instance_class = "db.serverless"
  instances = {
    writer = {}
    reader = {}
  }

  # Encryption
  storage_encrypted = true
  kms_key_id        = aws_kms_key.rds.arn

  # Backup
  backup_retention_period      = var.environment == "prod" ? 30 : 7
  preferred_backup_window      = "02:00-04:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"

  # High availability
  deletion_protection = var.environment == "prod"
  skip_final_snapshot = var.environment != "prod"

  # Performance Insights
  performance_insights_enabled          = true
  performance_insights_retention_period = var.environment == "prod" ? 731 : 7

  # Enhanced monitoring
  monitoring_interval = 60

  # IAM authentication
  iam_database_authentication_enabled = true
}
```

---

## Application Load Balancer

```hcl
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"

  name    = "${var.project}-${var.environment}"
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets

  # Security
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

---

## S3 with CloudFront (CDN)

```hcl
# S3 bucket for static assets
module "s3_static" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket = "${var.project}-${var.environment}-static"

  # Block public access
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  # Versioning
  versioning = {
    enabled = true
  }

  # Encryption
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  # Lifecycle rules
  lifecycle_rule = [
    {
      id      = "archive"
      enabled = true

      transition = [
        {
          days          = 90
          storage_class = "STANDARD_IA"
        },
        {
          days          = 180
          storage_class = "GLACIER_IR"
        }
      ]

      noncurrent_version_expiration = {
        days = 30
      }
    }
  ]

  # CORS
  cors_rule = [
    {
      allowed_methods = ["GET", "HEAD"]
      allowed_origins = ["https://${var.domain}"]
      allowed_headers = ["*"]
      max_age_seconds = 3600
    }
  ]
}

# CloudFront distribution
module "cloudfront" {
  source  = "terraform-aws-modules/cloudfront/aws"
  version = "~> 3.0"

  aliases = ["static.${var.domain}"]

  comment             = "${var.project} static assets"
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_100"
  retain_on_delete    = false
  wait_for_deployment = false

  # Origin Access Control for S3
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

    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD"]
    compress        = true

    cache_policy_id          = "658327ea-f89d-4fab-a63d-7e88639e58f6"  # CachingOptimized
    origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"  # CORS-S3Origin
  }

  viewer_certificate = {
    acm_certificate_arn      = module.acm_cloudfront.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
```

---

## Serverless API (Lambda + API Gateway)

```hcl
# Lambda function
module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 7.0"

  function_name = "${var.project}-${var.environment}-api"
  description   = "API Lambda function"
  handler       = "main.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]  # Graviton

  source_path = "${path.module}/../src"

  memory_size = 256
  timeout     = 30

  # VPC (optional)
  vpc_subnet_ids         = module.vpc.private_subnets
  vpc_security_group_ids = [module.lambda_sg.security_group_id]

  # Environment
  environment_variables = {
    ENVIRONMENT = var.environment
    LOG_LEVEL   = var.environment == "prod" ? "INFO" : "DEBUG"
  }

  # X-Ray tracing
  tracing_mode = "Active"

  # Permissions
  attach_policy_json = true
  policy_json = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query"
        ]
        Resource = module.dynamodb.dynamodb_table_arn
      }
    ]
  })
}

# API Gateway
module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "~> 5.0"

  name          = "${var.project}-${var.environment}"
  description   = "HTTP API Gateway"
  protocol_type = "HTTP"

  cors_configuration = {
    allow_headers = ["*"]
    allow_methods = ["*"]
    allow_origins = ["https://${var.domain}"]
  }

  # Custom domain
  domain_name                 = "api.${var.domain}"
  domain_name_certificate_arn = module.acm.acm_certificate_arn

  # Integrations
  integrations = {
    "ANY /{proxy+}" = {
      lambda_arn             = module.lambda.lambda_function_arn
      payload_format_version = "2.0"
    }
  }

  # Throttling
  default_route_settings = {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }
}
```

---

## DynamoDB Table

```hcl
module "dynamodb" {
  source  = "terraform-aws-modules/dynamodb-table/aws"
  version = "~> 4.0"

  name     = "${var.project}-${var.environment}"
  hash_key = "pk"
  range_key = "sk"

  billing_mode = "PAY_PER_REQUEST"  # On-demand

  attributes = [
    {
      name = "pk"
      type = "S"
    },
    {
      name = "sk"
      type = "S"
    },
    {
      name = "gsi1pk"
      type = "S"
    },
    {
      name = "gsi1sk"
      type = "S"
    }
  ]

  global_secondary_indexes = [
    {
      name            = "gsi1"
      hash_key        = "gsi1pk"
      range_key       = "gsi1sk"
      projection_type = "ALL"
    }
  ]

  # Encryption
  server_side_encryption_enabled     = true
  server_side_encryption_kms_key_arn = aws_kms_key.dynamodb.arn

  # Point-in-time recovery
  point_in_time_recovery_enabled = true

  # TTL
  ttl_attribute_name = "ttl"
  ttl_enabled        = true
}
```

---

## EventBridge + SQS (Event-Driven)

```hcl
# EventBridge Rule
resource "aws_cloudwatch_event_rule" "order_created" {
  name        = "${var.project}-${var.environment}-order-created"
  description = "Capture order created events"

  event_pattern = jsonencode({
    source      = ["${var.project}.orders"]
    detail-type = ["OrderCreated"]
  })
}

resource "aws_cloudwatch_event_target" "sqs" {
  rule      = aws_cloudwatch_event_rule.order_created.name
  target_id = "send-to-sqs"
  arn       = module.sqs.queue_arn

  dead_letter_config {
    arn = module.sqs_dlq.queue_arn
  }
}

# SQS Queue
module "sqs" {
  source  = "terraform-aws-modules/sqs/aws"
  version = "~> 4.0"

  name = "${var.project}-${var.environment}-orders"

  visibility_timeout_seconds = 60
  message_retention_seconds  = 1209600  # 14 days
  receive_wait_time_seconds  = 20       # Long polling

  # Dead letter queue
  redrive_policy = {
    deadLetterTargetArn = module.sqs_dlq.queue_arn
    maxReceiveCount     = 3
  }

  # Encryption
  sqs_managed_sse_enabled = true
}

module "sqs_dlq" {
  source  = "terraform-aws-modules/sqs/aws"
  version = "~> 4.0"

  name = "${var.project}-${var.environment}-orders-dlq"

  message_retention_seconds = 1209600  # 14 days
  sqs_managed_sse_enabled   = true
}
```

---

## Step Functions (Orchestration)

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
        Next     = "SendConfirmation"
        Catch = [{
          ErrorEquals = ["PaymentError"]
          Next        = "OrderFailed"
        }]
      }
      SendConfirmation = {
        Type     = "Task"
        Resource = module.lambda_notification.lambda_function_arn
        End      = true
      }
      OrderFailed = {
        Type  = "Fail"
        Error = "OrderProcessingFailed"
        Cause = "Order processing failed at one of the steps"
      }
    }
  })

  logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.sfn.arn}:*"
    include_execution_data = true
    level                  = "ALL"
  }

  tracing_configuration {
    enabled = true
  }
}
```

---

## CloudWatch Monitoring

```hcl
# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.project}-${var.environment}"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "API Gateway Requests"
          region = var.region
          metrics = [
            ["AWS/ApiGateway", "Count", "ApiId", module.api_gateway.api_id]
          ]
          period = 300
          stat   = "Sum"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "Lambda Duration"
          region = var.region
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", module.lambda.lambda_function_name]
          ]
          period = 300
          stat   = "Average"
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6
        properties = {
          title  = "DynamoDB Consumed Capacity"
          region = var.region
          metrics = [
            ["AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", module.dynamodb.dynamodb_table_id],
            ["AWS/DynamoDB", "ConsumedWriteCapacityUnits", "TableName", module.dynamodb.dynamodb_table_id]
          ]
          period = 300
          stat   = "Sum"
        }
      }
    ]
  })
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${var.project}-${var.environment}-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Lambda function errors exceeded threshold"

  dimensions = {
    FunctionName = module.lambda.lambda_function_name
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "api_5xx" {
  alarm_name          = "${var.project}-${var.environment}-api-5xx"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5XXError"
  namespace           = "AWS/ApiGateway"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "API Gateway 5XX errors exceeded threshold"

  dimensions = {
    ApiId = module.api_gateway.api_id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# SNS Topic for alerts
resource "aws_sns_topic" "alerts" {
  name              = "${var.project}-${var.environment}-alerts"
  kms_master_key_id = aws_kms_key.sns.id
}
```

---

## IAM Role with Least Privilege

```hcl
# EKS Pod Identity
module "app_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "~> 1.0"

  name = "${var.project}-${var.environment}-app"

  associations = {
    app = {
      cluster_name    = module.eks.cluster_name
      namespace       = "app"
      service_account = "app"
    }
  }

  additional_policy_arns = {
    policy = aws_iam_policy.app.arn
  }
}

resource "aws_iam_policy" "app" {
  name = "${var.project}-${var.environment}-app"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3Access"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          module.s3_static.s3_bucket_arn,
          "${module.s3_static.s3_bucket_arn}/*"
        ]
      },
      {
        Sid    = "SecretsAccess"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:${var.project}/${var.environment}/*"
        ]
      },
      {
        Sid    = "KMSDecrypt"
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = [
          aws_kms_key.secrets.arn
        ]
      }
    ]
  })
}
```
