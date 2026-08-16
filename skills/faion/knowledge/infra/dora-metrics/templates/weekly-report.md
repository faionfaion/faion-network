<!--

purpose: Weekly DORA report skeleton — four keys plus reliability, with a per-metric commentary section
consumes: deploy log + incident log + PR cycle-time export
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
-->


# DORA Metrics — Week of <week_of>

Compiled by <report_owner>.

## Summary

| Metric | This Week | Last Week | Target | Status |
|--------|-----------|-----------|--------|--------|
| Deployment Frequency | [X/day] | [X/day] | <deploy_frequency_target> | |
| Lead Time | [Xh] | [Xh] | <lead_time_target> | |
| Change Failure Rate | [X%] | [X%] | <cfr_target> | |
| MTTR | [Xm] | [Xm] | <mttr_target> | |
| Reliability | [X%] | [X%] | >99.9% | |

## Deployment Frequency

- Total deployments this week: [X]
- Services with zero deploys: [list or none]
- Notable: [any deployment freeze, incidents, or process changes]

## Lead Time for Changes

- Median lead time: [Xh]
- Longest lead time: [Xh] (PR #<longest_lead_time> — <reason>)
- Bottleneck stage: <bottleneck_stage>

## Change Failure Rate

- Failed deployments: [X] of [X] total
- Affected services: <list>
- Root causes: <root_causes>

## Time to Restore (MTTR)

- Incidents this week: [X] (P1: [X], P2: [X], P3: [X])
- Median MTTR: [Xm]
- Longest: [Xm] (Incident #<longest>)

## Reliability

- Services meeting SLO: [X]/[X]
- SLO violations: [service, SLO type, miss percentage]

## Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | | | |
| 2 | | | |
