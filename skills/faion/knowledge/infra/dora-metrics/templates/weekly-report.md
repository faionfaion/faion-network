<!--
purpose: Weekly DORA report skeleton — four keys plus reliability, with a per-metric commentary section
consumes: deploy log + incident log + PR cycle-time export
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
variables:
  - name: week_of
    type: string
    required: true
    description: Monday of the week reported, ISO. DORA numbers only mean anything as a series, and a series needs every entry to say which week it is without the reader counting back.
  - name: deploy_frequency_target
    type: string
    required: true
    default: "multiple per day"
    description: The deployment frequency you are actually aiming for this quarter. Copying "elite" out of the report is how a team measures itself against a benchmark nobody agreed to chase.
  - name: lead_time_target
    type: string
    required: true
    default: "under 24h"
    description: Target lead time from first commit to production. State the definition you are using - teams that measure from PR-open instead of first-commit report numbers that are not comparable to anyone's.
  - name: cfr_target
    type: string
    required: true
    default: "under 15%"
    description: Target change failure rate, and what counts as a failure. Rollback only, or any hotfix within 24h? The threshold is worthless until the reader knows which.
  - name: mttr_target
    type: string
    required: true
    default: "under 60m"
    description: Target time to restore, measured from customer impact and not from detection. The gap between those two is usually where the real problem is.
  - name: report_owner
    type: string
    required: true
    description: Who compiles this and answers for the numbers. Metrics with no author drift into decoration by the third week - somebody has to be embarrassed by a bad one.
-->
# DORA Metrics — Week of {{week_of}}

Compiled by {{report_owner}}.

## Summary

| Metric | This Week | Last Week | Target | Status |
|--------|-----------|-----------|--------|--------|
| Deployment Frequency | [X/day] | [X/day] | {{deploy_frequency_target}} | |
| Lead Time | [Xh] | [Xh] | {{lead_time_target}} | |
| Change Failure Rate | [X%] | [X%] | {{cfr_target}} | |
| MTTR | [Xm] | [Xm] | {{mttr_target}} | |
| Reliability | [X%] | [X%] | >99.9% | |

## Deployment Frequency

- Total deployments this week: [X]
- Services with zero deploys: [list or none]
- Notable: [any deployment freeze, incidents, or process changes]

## Lead Time for Changes

- Median lead time: [Xh]
- Longest lead time: [Xh] (PR #[NNN] — [reason])
- Bottleneck stage: [PR review / CI time / deploy queue / other]

## Change Failure Rate

- Failed deployments: [X] of [X] total
- Affected services: [list]
- Root causes: [deploy-time bug / test gap / config error]

## Time to Restore (MTTR)

- Incidents this week: [X] (P1: [X], P2: [X], P3: [X])
- Median MTTR: [Xm]
- Longest: [Xm] (Incident #[NNN])

## Reliability

- Services meeting SLO: [X]/[X]
- SLO violations: [service, SLO type, miss percentage]

## Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | | | |
| 2 | | | |
