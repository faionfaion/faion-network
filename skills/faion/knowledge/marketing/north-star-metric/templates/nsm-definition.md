<!--
purpose: North Star Metric definition sheet — calculation, justification, current state, input metrics
consumes: analytics access + retention cohort data
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~250-600 tokens when loaded as context
variables:
  - name: nsm_name
    type: string
    required: true
    description: The metric's short name, said the way the team will say it in a standup - "Weekly Active Teams". Not a formula and not an acronym nobody expands.
  - name: nsm_calculation
    type: text
    required: true
    description: The exact calculation - the population, the action, the window. "Count of unique teams that completed at least one task in the last 7 days". Anyone with database access must be able to reproduce your number from this sentence alone.
  - name: customer_value_link
    type: text
    required: true
    description: How this metric represents value the customer received, not effort you expended. If it goes up when customers are doing more work for the same outcome, you have picked a vanity metric.
  - name: revenue_hypothesis
    type: text
    required: true
    description: The evidence or hypothesis that this predicts revenue - a cohort correlation you measured, or the untested belief stated as untested. Say which of the two it is.
  - name: current_value
    type: string
    required: true
    description: Today's value with the date it was read. A North Star without a starting point cannot show movement, and nobody will remember what it was when this is reviewed next quarter.
  - name: target_value
    type: string
    required: true
    description: The value you are aiming for and the date you expect it. Pick a date close enough that being wrong is embarrassing while the people who set it are still here.
-->
# North Star Metric: {{nsm_name}}

## Definition

{{nsm_calculation}}

## Why This Metric?

1. **Customer value:** {{customer_value_link}}
2. **Revenue correlation:** {{revenue_hypothesis}}
3. **Actionability:** [Which teams can move this metric and how]

## Current State

- Value: {{current_value}}
- Trend: [up / down / flat] [%] vs last period
- Target: {{target_value}}

## Input Metrics

| Input Metric | Owner Team | Current | Target |
|--------------|------------|---------|--------|
| [Input 1] | | | |
| [Input 2] | | | |
| [Input 3] | | | |

## Dashboard Link

[URL]

## Validation Test Results (last run: [date])

- NSM up → retention up: [yes / no / inconclusive]
- NSM down → churn up: [yes / no / inconclusive]
- Next review: [date]
