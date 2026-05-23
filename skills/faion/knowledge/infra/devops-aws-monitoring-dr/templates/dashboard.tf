# purpose: Terraform CloudWatch dashboard with API Gateway + Lambda + DynamoDB widgets
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (spec)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.project}-main"
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        width  = 12
        height = 6
        properties = {
          metrics = [["AWS/ApiGateway", "Count", "ApiName", var.api_name], [".", "5XXError", ".", "."]]
          period  = 300
          region  = var.region
          title   = "API Requests + 5xx"
        }
      },
      {
        type   = "metric"
        width  = 12
        height = 6
        properties = {
          metrics = [["AWS/Lambda", "Duration", "FunctionName", var.lambda_name], [".", "Errors", ".", "."], [".", "Throttles", ".", "."]]
          period  = 300
          region  = var.region
          title   = "Lambda"
        }
      }
    ]
  })
}
