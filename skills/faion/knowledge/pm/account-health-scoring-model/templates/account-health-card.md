<!--

purpose: Per-account health score card (single account, weekly)
consumes: signals from timesheet, CRM, billing
produces: single-account health card markdown
depends-on: signal-thresholds.md
token-budget-impact: low (~250 tokens per account)
-->



# Account Health Card — <client_name>

- **Week:** <period_label>
- **Tier:** <health_tier>
- **Score:** <health_score>
- **Trend:** <trend>

## Signals

| # | Signal              | Source           | Value | Score (0/1/2) |
|---|---------------------|------------------|-------|---------------|
| 1 | Utilization         | timesheet        |       |               |
| 2 | DM engagement       | calendar+email   |       |               |
| 3 | Scope-creep delta   | SOW vs. tickets  |       |               |
| 4 | Payment punctuality | invoice ledger   |       |               |
| 5 | Referral/advocacy   | CRM notes        |       |               |
| 6 | Sponsor stability   | org chart        |       |               |

## Action this week

- <action_this_week>

## Notes

- <notes>
