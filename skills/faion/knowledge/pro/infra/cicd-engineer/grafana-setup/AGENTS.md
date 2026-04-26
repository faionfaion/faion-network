# Grafana Setup and Provisioning

## Summary

Grafana setup methodology covering Docker Compose, Kubernetes Helm, and High Availability deployment patterns, with configuration-as-code provisioning for data sources, dashboards, and alerting. Grafana Agent reached EOL on November 1, 2025 — all new deployments must use Grafana Alloy. HA requires PostgreSQL or MySQL (SQLite is single-node only); no session affinity needed since sessions are stored in the database.

## Why

Provisioning Grafana via configuration files (YAML + JSON) instead of the UI prevents configuration drift, enables GitOps workflows, and allows reproducible deployments across environments. Without provisioning, every new environment requires manual dashboard and datasource setup, which breaks consistency and slows incident response.

## When To Use

- Deploying Grafana for the first time in any environment (Docker, K8s, VM)
- Migrating from Grafana Agent to Grafana Alloy (mandatory — Agent EOL Nov 2025)
- Setting up HA Grafana for production with PostgreSQL backend
- Configuring alerting pipelines with contact points and notification policies
- Managing Grafana infrastructure as code with Terraform or Helm

## When NOT To Use

- Quick local exploration with no persistence requirement — use `docker run grafana/grafana` directly
- When Grafana Cloud is available and operational complexity must be zero
- When the only requirement is viewing existing dashboards — no setup needed, just access

## Content

| File | What's inside |
|------|---------------|
| `content/01-deployment.xml` | Docker Compose and Helm deployment rules, HA requirements (PostgreSQL, load balancer), Alloy migration rule |
| `content/02-provisioning.xml` | Datasource and dashboard provider YAML rules, alerting provisioning structure, secrets-via-env-vars rule |
| `content/03-examples.xml` | Basic dev stack docker-compose, HA docker-compose with two Grafana nodes + nginx, Kubernetes values.yaml |

## Templates

| File | Purpose |
|------|---------|
| `templates/datasources.yaml` | Prometheus, Loki, Tempo, PostgreSQL datasource provisioning YAML |
| `templates/dashboards.yaml` | Dashboard provider config with folder-based organization |
| `templates/alerting-rules.yaml` | Alert rules, contact points, notification policies, mute timings |
| `templates/grafana.ini` | Production grafana.ini with security, OAuth, HA alerting, metrics sections |
| `templates/alloy-config.alloy` | Grafana Alloy config for K8s pod/node scraping and log collection |
