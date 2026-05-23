# purpose: terraform basic Lambda function with execution role + IAM least-privilege
# consumes: see ../AGENTS.md ## Prerequisites + content/02-output-contract.xml
# produces: provisioned AWS resources conforming to the methodology spec
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~600-1500 tokens when loaded as context
resource "aws_iam_role" "lambda" {
  name = "${local.name_prefix}-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.name_prefix}-function"
  retention_in_days = 30
  tags              = local.common_tags
}

resource "aws_lambda_function" "main" {
  function_name = "${local.name_prefix}-function"
  role          = aws_iam_role.lambda.arn
  filename      = "function.zip"

  handler       = "app.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]
  memory_size   = 512
  timeout       = 30

  tracing_config { mode = "Active" }

  environment {
    variables = {
      LOG_LEVEL   = "INFO"
      ENVIRONMENT = var.environment
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda]
  tags       = local.common_tags
}
