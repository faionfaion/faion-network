# DORA Metrics

## Summary

Five DORA metrics measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service (MTTR), and Reliability (SLO compliance). Elite teams deploy 973x more frequently and recover 6570x faster than low performers. Measure all five together — high frequency with high CFR signals process problems, not success.

## Why

DORA research proved throughput and stability are not a trade-off: elite teams excel at both. Tracking these metrics exposes bottlenecks (long PR review time, flaky tests, manual approvals) and creates a feedback loop for continuous improvement. Used punitively, they backfire — teams game metrics instead of improving systems.

## When To Use

- Establishing baseline software delivery performance for a team or service
- Identifying delivery bottlenecks (where does lead time accumulate?)
- Evaluating impact of process changes (did trunk-based dev improve deploy frequency?)
- Building engineering dashboards for leadership aligned to business outcomes
- Assessing AI tooling adoption impact on delivery stability (2025: AI improves throughput but increases CFR)

## When NOT To Use

- Individual performance reviews — DORA measures team/system outcomes, not individuals
- Comparing teams without context — team size, domain complexity, and tech debt differ
- Single-metric focus — optimize one metric without watching others (e.g., deploy frequency up but CFR up too)
- Fewer than 30 days of data — baselines are meaningless without sufficient history

## Content

| File | What's inside |
|------|---------------|
| `content/01-five-metrics.xml` | Definitions, elite/high/medium/low benchmarks, how to measure each metric |
| `content/02-implementation.xml` | Data collection checklist, tooling options (Sleuth, LinearB, GitHub/GitLab native), anti-patterns |
| `content/03-examples.xml` | Lead time calculator (Python), CFR calculator, MTTR calculator, PromQL queries |

## Templates

| File | Purpose |
|------|---------|
| `templates/deployment-event.json` | JSON schema for deployment event records |
| `templates/incident-event.json` | JSON schema for incident event records |
| `templates/dora-config.yaml` | DORA metrics collection config (services, targets, data sources) |
| `templates/weekly-report.md` | Weekly DORA report template with all five metrics and action items |
| `templates/prompt-dora-analysis.txt` | LLM prompt for analyzing DORA metric data |
