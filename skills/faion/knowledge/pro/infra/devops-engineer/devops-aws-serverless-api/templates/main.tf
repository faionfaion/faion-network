# purpose: Terraform skeleton: Lambda + API Gateway HTTP API + DynamoDB + EventBridge + SQS DLQ
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (config)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

module "lambda" {
  source        = "terraform-aws-modules/lambda/aws"
  version       = "~> 7.0"
  function_name = "${var.project}-handler"
  handler       = "app.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]
  tracing_mode  = "Active"
  publish       = true
  environment_variables = { TABLE = aws_dynamodb_table.main.name }
}

module "api_gateway" {
  source        = "terraform-aws-modules/apigateway-v2/aws"
  version       = "~> 5.0"
  name          = "${var.project}-http"
  protocol_type = "HTTP"
  cors_configuration = {
    allow_origins = ["https://app.example.com"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["content-type", "authorization"]
  }
  domain_name = var.domain
  default_route_settings = {
    throttling_burst_limit = 5000
    throttling_rate_limit  = 1000
  }
}

resource "aws_dynamodb_table" "main" {
  name         = "${var.project}-main"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"
  attribute { name = "pk" type = "S" }
  attribute { name = "sk" type = "S" }
  point_in_time_recovery { enabled = true }
}

resource "aws_sqs_queue" "dlq" {
  name = "${var.project}-dlq"
}
