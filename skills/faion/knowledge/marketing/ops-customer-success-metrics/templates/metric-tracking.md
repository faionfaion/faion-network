<!-- purpose: Monthly CS metrics report -- NPS/CSAT, cohort retention, survey cadence, leading-indicator alerts. -->
<!-- consumes: NPS/CSAT survey results + cohort retention data -->
<!-- produces: Markdown metrics report -->
<!-- depends-on: content/01-core-rules.xml (r4-nps-csat-cadence, r2-cohort-retention-curves) -->
<!-- token-budget-impact: ~350-550 tokens when loaded as context -->

# Customer Success Metrics — <month_yyyy>

## Key Metrics vs. Targets

| Metric | Current | Target | Status | MoM Change |
|--------|---------|--------|--------|------------|
| NPS | [X] | >50 | [Hit/Miss] | [+/-X] |
| CSAT | <x_5> | >4.5/5 | [Hit/Miss] | [+/-X] |
| Time to value | <x_days> | <7 days | [Hit/Miss] | [+/-X] |
| Core feature adoption | [X%] | >80% | [Hit/Miss] | [+/-X%] |
| Expansion rate (12mo) | [X%] | >20% | [Hit/Miss] | |
| Net Revenue Retention | [X%] | >100% | [Hit/Miss] | |

## Cohort Retention

| Signup cohort | Starting customers | Active (this month) | Retention | Avg health | NRR |
|---------------|--------------------|---------------------|-----------|------------|-----|
| [3 months ago] | [X] | [X] | [X%] | [X] | [X%] |
| [2 months ago] | [X] | [X] | [X%] | [X] | [X%] |
| [1 month ago] | [X] | [X] | [X%] | [X] | — |

## NPS Detail

- Responses this month: [X] (minimum 50 for statistical reliability)
- Promoters (9-10): [X] ([X%])
- Passives (7-8): [X] ([X%])
- Detractors (0-6): [X] ([X%])
- Top detractor theme: [one sentence]
- Top promoter theme: [one sentence]

## Survey Fatigue Check

- Active NPS survey: <yes_no>
- Active CSAT survey: <yes_no>
- Note: Do not run both simultaneously on the same account within 30 days

## Leading Indicator Alerts This Month

| Signal | Accounts | MRR at risk | Action taken |
|--------|----------|-------------|--------------|
| Usage drop >30% in 14d | [X] | $[X] | <outreach> |
| Support escalation | [X] | $[X] | <escalated> |
| Failed payment | [X] | $[X] | <billing_follow_up> |

## Improvements Shipped

- [Change made to onboarding or product this month that affected TTV or adoption — link to ticket]
