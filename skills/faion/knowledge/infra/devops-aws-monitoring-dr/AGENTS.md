# AWS Monitoring, Alerting, and Disaster Recovery

## Summary

**One-sentence:** Produces a monitoring + DR spec: CloudWatch dashboards per tier, tiered alarms (page/business-hours/digest), X-Ray tracing, and a tested DR strategy (backup/pilot-light/warm-standby/active-active) matched to RTO/RPO.

**One-paragraph:** Production AWS workloads need CloudWatch dashboards per tier, metric alarms tiered by severity (critical=page, warning=business-hours, info=digest), X-Ray distributed tracing across Lambda + API Gateway, and a DR strategy actually tested on a schedule. Output is a spec that maps each tier (API / compute / DB / queue) to its dashboard widgets + alarm thresholds + SNS topic, names the DR strategy (backup / pilot-light / warm-standby / active-active) selected against RTO/RPO, and declares the DR-drill cadence. Untested DR is no DR.

**Ефективно для:**

- New prod AWS workload — monitoring + DR baseline.
- Existing arch без dashboards / alarms — add observability.
- DR runbook design / test для business-critical service.
- WA review для Reliability + OpEx pillars.

## Applies If (ALL must hold)

- Workload runs on AWS prod (any tier).
- RTO/RPO targets defined (or can be negotiated).
- CloudWatch + SNS budget acceptable (~$10-50/mo per workload).

## Skip If (ANY kills it)

- Dev / staging — basic alarms only.
- Third-party stack (Datadog / New Relic) already deployed — integrate CloudWatch as source instead.
- Throwaway sandbox account.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload tier map | list of API / compute / DB / queue components | architecture diagram |
| RTO / RPO targets | hours | business / SLO |
| On-call rotation | named team + PagerDuty / OpsGenie | ops team |
| DR budget | $/mo | finance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[backup-strategies]] | DR strategy depends on backup posture |
| [[aws-well-architected-checklists]] | Reliability + OpEx pillar items |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: dashboard-per-tier, alarms-tiered, xray-active, dr-strategy-matches-rto, dr-drill-cadence, skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for monitoring+DR spec + valid/invalid + forbidden | 1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: no-tiered-alarms, untested-dr, x-ray-disabled, dashboard-noise | 900 |
| `content/04-procedure.xml` | essential | 6 steps: tier-map → dashboards → alarms → X-Ray → DR strategy → DR drill | 900 |
| `content/05-examples.xml` | reference | Worked example: e-commerce SaaS warm-standby DR | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on RTO + budget → DR strategy | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-dashboards` | sonnet | Per-tier dashboard widget composition. |
| `set-alarm-thresholds` | sonnet | Latency / error-rate threshold math. |
| `pick-dr-strategy` | opus | Strategic — depends on RTO + budget. |

## Templates

| File | Purpose |
|------|---------|
| `templates/monitoring-dr-spec.md.j2` | Markdown skeleton for the monitoring+DR spec |
| `templates/monitoring-dr-spec.md` | Markdown skeleton for the monitoring+DR spec Generated from `templates/monitoring-dr-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/dashboard.tf` | Terraform CloudWatch dashboard with API Gateway + Lambda + DynamoDB widgets |
| `templates/alarms.tf` | Terraform tiered alarms with SNS topics (critical / warning / info) |
| `templates/_smoke-test.json` | Minimum spec used by validate-devops-aws-monitoring-dr.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-aws-monitoring-dr.py` | Validate the spec artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[backup-strategies]]
- [[aws-well-architected-checklists]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when scoping monitoring + DR for any prod AWS workload.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/dashboard.tf`

```hcl
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
```

### `templates/alarms.tf`

```hcl
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
```

### `templates/_smoke-test.json`

```json
{
  "workload": "checkout-api",
  "rto_hours": 4,
  "rpo_hours": 1,
  "dashboards_per_tier": [
    "api",
    "lambda",
    "dynamodb"
  ],
  "alarm_severities": [
    "critical",
    "warning",
    "info"
  ],
  "xray_active": true,
  "dr_strategy": "warm-standby",
  "dr_region_pair": "us-east-1->us-west-2",
  "drill_cadence_months": 3
}
```
