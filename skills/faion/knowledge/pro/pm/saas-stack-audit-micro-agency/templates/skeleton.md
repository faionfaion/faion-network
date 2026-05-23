<!-- purpose: SaaSAuditReport skeleton with 5-bucket classification -->
<!-- consumes: card export + last-login data + client list -->
<!-- produces: scaffold consumed by classifier step -->
<!-- depends-on: content/01-core-rules.xml#r1-full-stack-inventory -->
<!-- token-budget-impact: ~150 tokens -->

# SaaS Audit — [quarter]

**Owner:** [founder role] / [person]
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Inventory

| tool_id | vendor | monthly_cost_usd | last_login_days | tied_to_revenue | duplicate_of | bucket | evidence |
|---------|--------|------------------|----|----|----|----|---|
| linear | Linear | 60 | 1 | true | null | keep | "primary issue tracker" |
| jira | Atlassian | 35 | 64 | false | linear | cancel | "duplicate; last login 64d" |

## Kill list

- items: [tool_id, ...]
- signed_by: [founder handle]
- signed_at: YYYY-MM-DD

## Spend

- spend_before: $...
- spend_forecast_after: $...
