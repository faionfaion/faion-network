# Reporting Dashboards

## Summary

Automated PM reporting: tool-specific dashboard configuration (Jira, Linear, ClickUp), scheduled report generation for weekly status and sprint reviews, Slack digest delivery, and BI tool integration (PowerBI, Metabase, Grafana) via API ETL. Report agents query PM tools as read-only, validate data before sending (zero committed → abort, not 0% completion), and archive every generated report. Dashboard data is only as clean as underlying PM data — garbage in, garbage out.

## Why

Manual status reporting is the most common PM overhead for engineering leads. Automating sprint metrics collection (velocity, completion rate, blocked items) eliminates a weekly task and makes metrics consistent and comparable across sprints. BI integrations (Grafana, Metabase) enable trend analysis over time that native PM tool dashboards cannot provide. The key rule: separate report generation from report delivery — validate before sending.

## When To Use

- Sprint-cadence status reporting requires manual data collection from multiple PM tools
- Stakeholders need a consolidated view across several projects without PM tool access
- PM tool native reports are insufficient and data needs cross-referencing with external sources
- Automated Slack digests needed on a fixed schedule (daily standup summary, weekly status)
- PM data needs to feed into BI tools for trend analysis over time

## When NOT To Use

- Team of 1-3 people where a quick manual update is faster than building dashboard automation
- PM tool's native dashboard covers all stakeholder needs — adding automation creates maintenance burden
- Regulated environments needing report provenance and immutability guarantees — automated reports lack audit trails unless outputs are explicitly archived
- Real-time operational dashboards (incident response) — PM dashboards lag by minutes to hours

## Content

| File | What's inside |
|------|---------------|
| `content/01-dashboard-rules.xml` | Dashboard setup rules, data quality requirements, report schema rules, Slack delivery constraints |
| `content/02-automation-etl.xml` | Scheduled report agent patterns, ETL pipeline rules, tool-specific API gotchas, BI integration setup |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-status-report.md` | Weekly status report markdown template with exec summary, metrics table, risks, next week focus |
| `templates/sprint-report.md` | Sprint report template with delivery summary, burndown, quality metrics, retrospective highlights |
| `templates/jira-metrics-fetcher.py` | Python script to pull Jira sprint metrics and post to Slack |
