<!-- purpose: Monthly expansion-revenue dashboard -- NRR, expansion by type, top opportunities, trigger performance. -->
<!-- consumes: billing export (MRR by account) + usage-trigger fire/conversion log -->
<!-- produces: Markdown expansion dashboard -->
<!-- depends-on: content/01-core-rules.xml (r4-report-nrr-and-expansion-arr-monthly) -->
<!-- token-budget-impact: ~400-600 tokens when loaded as context -->

# Expansion Revenue Dashboard — <month_yyyy>

## Summary

| Metric | This month | Last month | Change |
|--------|------------|------------|--------|
| Starting MRR | $[X] | $[X] | |
| Expansion MRR | $[X] | $[X] | [+/-X%] |
| Contraction MRR | $[X] | $[X] | |
| Churn MRR | $[X] | $[X] | |
| Net Revenue Retention | [X%] | [X%] | <x_pts> |

## Expansion by Type

| Type | Accounts | MRR | Avg delta/account |
|------|----------|-----|-------------------|
| Usage-limit upgrades | [X] | $[X] | $[X] |
| Feature-based upgrades | [X] | $[X] | $[X] |
| Seat expansion | [X] | $[X] | $[X] |
| Annual plan conversions | [X] | $[X] | $[X] |
| Cross-sells | [X] | $[X] | $[X] |
| **Total** | **[X]** | **$[X]** | |

## Top Expansion Opportunities This Month

| Account | Current plan | Current MRR | Opportunity | Signal | Owner |
|---------|-------------|-------------|-------------|--------|-------|
| [Name] | Basic | $[X] | Upgrade to Pro | [90% limit] | [Name] |
| [Name] | Pro | $[X] | Add 5 seats | <team_grew> | [Name] |
| [Name] | Pro | $[X] | Annual conversion | [12mo customer] | [Name] |

## Trigger Performance

| Trigger type | Fires | Conversions | Conversion rate | Revenue |
|--------------|-------|-------------|-----------------|---------|
| Usage threshold (80%) | [X] | [X] | [X%] | $[X] |
| Advanced feature use | [X] | [X] | [X%] | $[X] |
| Annual upgrade nudge | [X] | [X] | [X%] | $[X] |

## Actions

- [ ] [Follow up on top opportunity 1 — owner]
- [ ] [Kill bottom-performing trigger if <5% conversion — owner]
