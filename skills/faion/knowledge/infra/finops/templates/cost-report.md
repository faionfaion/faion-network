<!--
purpose: Monthly cloud cost report skeleton — spend, per-team split, waste, and named optimisation actions
consumes: cloud billing export + tagging inventory
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
variables:
  - name: billing_month
    type: string
    required: true
    description: The month this covers, as month and year. Cloud bills land late and get restated - naming the month rather than "last month" is what makes two of these comparable.
  - name: total_spend
    type: string
    required: true
    description: Total spend for the month, with currency. Take it from the billing export, not the console dashboard - the dashboard usually excludes tax, support and marketplace charges.
  - name: budget_amount
    type: string
    required: true
    description: The budget this is measured against, with currency. If nobody set one, say so plainly here rather than omitting the line - "no budget" is the finding.
  - name: largest_driver
    type: string
    required: true
    description: The single service or team that moved the bill most this month, up or down. One name. A report whose headline is "compute" tells the reader nothing they could act on.
  - name: waste_owner_deadline
    type: string
    required: true
    description: The date idle resources listed below must be assigned to a team lead, ISO. Waste sections without a date get re-published unchanged for months; that is the normal failure of this report.
  - name: report_owner
    type: string
    required: true
    description: Who compiles this and chases the actions. Finance can read the number; only somebody with a name will turn off the instance.
-->
# Monthly Cloud Cost Report — {{billing_month}}

Compiled by {{report_owner}}.

## Summary

| Metric | Value |
|--------|-------|
| Total spend | {{total_spend}} |
| vs last month | [+X% / -X%] |
| vs budget | [X%] of {{budget_amount}} |
| Largest cost driver | {{largest_driver}} |

## Cost by Team

| Team | Service | Cost | vs Last Month | % of Total |
|------|---------|------|---------------|------------|
| [Team A] | EC2 | [$X,XXX] | [+X%] | [X%] |
| [Team B] | RDS | [$X,XXX] | [-X%] | [X%] |
| [Team C] | S3 | [$X,XXX] | [+X%] | [X%] |

## Waste Identified

| Resource | Type | Avg CPU/Mem | Monthly Cost | Action |
|----------|------|-------------|--------------|--------|
| [instance id] | EC2 | 2% CPU | [$XXX] | Schedule stop or terminate |
| [db id] | RDS | 5% CPU | [$XXX] | Downsize to t3.small |

## Optimization Opportunities

| Action | Estimated Savings | Effort |
|--------|-------------------|--------|
| Convert baseline EC2 to 1-year Compute SP | [$X,XXX/mo] | Low |
| S3 lifecycle: move logs to Glacier at 90d | [$XXX/mo] | Low |
| Rightsize idle EC2 instances | [$XXX/mo] | Medium |

## Next Steps

- [ ] {{report_owner}}: assign every idle resource above to a team lead by {{waste_owner_deadline}}
- [ ] Finance: review Savings Plan purchase for the committed baseline
- [ ] Engineering: implement S3 lifecycle policy for [bucket names]
