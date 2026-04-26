# Dashboard Setup

## Summary

A methodology for setting up PM dashboards, automated status reports, and cross-tool integrations. Covers tool-specific widget configurations (Jira gadgets, Linear Insights, ClickUp widgets), scheduled Slack/email delivery, and BI connections (Metabase, Grafana, PowerBI). Every report pipeline must include a data-quality guard: if a required metric returns zero results unexpectedly, emit an alert rather than a misleading zero.

## Why

Native PM dashboards cover only single-tool data and require manual refresh. A separate reporting layer aggregates Jira + Linear + GitHub metrics into a unified view, survives tool migrations, and can push data to BI tools where stakeholders already work. Automated delivery removes the weekly "copy-paste to email" ritual while ensuring reports are archived and reproducible.

## When To Use

- Setting up automated sprint or weekly status dashboards pulling from one or more PM tools
- When native PM dashboards cover only part of the reporting need and data must be aggregated
- When stakeholders need a dashboard combining PM metrics with deployment or business data
- Migrating PM tools and needing a neutral reporting layer that can query both old and new tools
- Onboarding a new project: define what metrics matter before picking widgets

## When NOT To Use

- Teams of 1–3 people with a single PM tool — native built-in dashboards are sufficient
- When the bottleneck is process, not reporting — a dashboard showing a broken sprint every week is not the fix
- Real-time alerting (P0 incidents, deploys) — use PagerDuty or Grafana alerting instead
- When PM data is too dirty (inconsistent statuses, missing fields) — fix the process first

## Content

| File | What's inside |
|------|---------------|
| `content/01-dashboard-config.xml` | Tool-specific widget configs: Jira gadgets, Linear views, ClickUp widgets, portfolio dashboard |
| `content/02-reporting.xml` | Automated reporting schedules, Slack Block Kit delivery, report templates |
| `content/03-agent-usage.xml` | Agentic pipeline, subagent patterns, JQL queries, Python reporting script, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-status-report.md` | Weekly status report template with metrics table and risk log |
| `templates/sprint-report.md` | Sprint delivery summary template with burndown and retrospective sections |
| `templates/portfolio-dashboard.yaml` | Portfolio dashboard widget layout configuration |
| `templates/jql-queries.sql` | JQL query collection for common dashboard metrics |
| `templates/prompt-render-status.txt` | Prompt for agent to compute and render a weekly status report |
