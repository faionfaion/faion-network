# Grafana Dashboards

## Summary

Grafana is the leading open-source observability platform for visualizing metrics, logs, and traces. Use the RED method (Rate, Errors, Duration) for service dashboards and the USE method (Utilization, Saturation, Errors) for infrastructure. Provision dashboards as code via ConfigMaps or GitOps — never rely on UI-only dashboards that vanish on pod restart.

## Why

Ad-hoc dashboard creation leads to sprawl, inconsistent metrics, and no version history. A maturity model approach (Low → Medium → High) moves teams from reactive to systematic observability: variables for dynamic filtering, hierarchical drill-downs (cluster → namespace → pod), and GitOps provisioning that survives cluster rebuilds.

## When To Use

- Visualizing Prometheus, Loki, or Elasticsearch data for ops teams
- Building SLO dashboards showing error budgets alongside availability
- Creating on-call runbook dashboards with annotated deployment markers
- Standardizing observability across microservices with shared dashboard templates
- Grafana 12+: using Tabs to segment large dashboards without splitting metrics

## When NOT To Use

- Business intelligence / analytics — use dedicated BI tools (Looker, Metabase)
- Alerting without Alertmanager/Grafana Alerting configured — dashboards alone do not page
- Replacing application logging — Grafana shows metrics, not log content (use Explore for that)
- Public customer-facing status pages — use Statuspage or similar

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-principles.xml` | RED/USE/Four Golden Signals frameworks, variable types, visualization selection guide |
| `content/02-provisioning.xml` | Dashboard-as-code via ConfigMap, GitOps pattern, dashboard maturity model |
| `content/03-examples.xml` | DORA dashboard JSON, RED method panel queries, SLO gauge configuration |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-create-dashboard.txt` | LLM prompt for generating a Grafana dashboard for a given service |
