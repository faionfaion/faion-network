# purpose: Terraform tiered alarms with SNS topics (critical / warning / info)
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (spec)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

resource "aws_sns_topic" "critical" { name = "${var.project}-critical" }
resource "aws_sns_topic" "warning" { name = "${var.project}-warning" }

resource "aws_cloudwatch_metric_alarm" "api_5xx_critical" {
  alarm_name          = "${var.project}-api-5xx-critical"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5XXError"
  namespace           = "AWS/ApiGateway"
  period              = 60
  statistic           = "Sum"
  threshold           = 10
  alarm_actions       = [aws_sns_topic.critical.arn]
}
