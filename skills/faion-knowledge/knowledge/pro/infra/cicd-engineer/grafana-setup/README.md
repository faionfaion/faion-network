---
id: grafana-setup
name: "Grafana Setup & Provisioning"
domain: OPS
skill: faion-devops-engineer
category: "devops"
version: "2.0"
last_updated: "2026-01"
---

# Grafana Setup & Provisioning

## Overview

Comprehensive guide for Grafana setup, configuration, provisioning, and high availability deployment. Covers modern practices including Grafana Alloy (successor to Grafana Agent), Kubernetes deployments, and infrastructure as code approaches.

## Contents

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step deployment checklists |
| [examples.md](examples.md) | Production-ready configuration examples |
| [templates.md](templates.md) | Reusable templates for common scenarios |
| [llm-prompts.md](llm-prompts.md) | AI-assisted setup prompts |

## Quick Reference

### Deployment Options

| Option | Best For | Complexity |
|--------|----------|------------|
| Docker Compose | Dev/testing, single node | Low |
| Kubernetes + Helm | Production, scalable | Medium |
| High Availability | Enterprise, critical systems | High |
| Grafana Cloud | Managed, zero ops | Low |

### Key Components

| Component | Purpose |
|-----------|---------|
| Grafana Server | Visualization, dashboards |
| Grafana Alloy | Data collection (replaces Agent) |
| Prometheus | Metrics storage |
| Loki | Log aggregation |
| Mimir | Long-term metrics storage |

### Important: Grafana Agent EOL

Grafana Agent reached End-of-Life on **November 1, 2025**. Migrate to **Grafana Alloy**.

```
Grafana Agent Static  --> Grafana Alloy
Grafana Agent Flow    --> Grafana Alloy
Grafana Agent Operator --> Grafana Alloy
```

## Architecture Patterns

### Single Node (Development)

```
+------------------+
|    Grafana       |
|  (SQLite DB)     |
+--------+---------+
         |
    +----+----+
    | Alloy   |
    +---------+
```

### High Availability (Production)

```
                    +-------------+
                    | Load        |
                    | Balancer    |
                    +------+------+
                           |
         +-----------------+------------------+
         |                                    |
+--------+--------+              +------------+--------+
| Grafana Node 1  |              | Grafana Node 2      |
+-----------------+              +---------------------+
         |                                    |
         +----------------+-------------------+
                          |
                 +--------+--------+
                 | PostgreSQL/MySQL |
                 | (Shared DB)      |
                 +-----------------+
```

### Kubernetes Deployment

```
+-------------------------------------------------+
|  Kubernetes Cluster                             |
|  +-------------------------------------------+  |
|  | Monitoring Namespace                      |  |
|  |  +-------------+  +-------------+         |  |
|  |  | Grafana     |  | Prometheus  |         |  |
|  |  | Deployment  |  | StatefulSet |         |  |
|  |  +-------------+  +-------------+         |  |
|  |  +-------------+  +-------------+         |  |
|  |  | Alloy       |  | Loki        |         |  |
|  |  | DaemonSet   |  | StatefulSet |         |  |
|  |  +-------------+  +-------------+         |  |
|  +-------------------------------------------+  |
+-------------------------------------------------+
```

## Installation Methods

### 1. Docker Compose (Quick Start)

```bash
# Clone and start
docker compose up -d
# Access: http://localhost:3000
```

### 2. Kubernetes Helm Chart

```bash
# Add Grafana repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --create-namespace \
  --values values.yaml
```

### 3. Kubernetes Monitoring Helm Chart 2.0

```bash
# Complete monitoring stack (Grafana + Alloy + Prometheus)
helm install k8s-monitoring grafana/k8s-monitoring \
  --namespace monitoring \
  --create-namespace \
  --values k8s-monitoring-values.yaml
```

## Provisioning Overview

Grafana supports **configuration as code** through provisioning:

| Type | Path | Format |
|------|------|--------|
| Data Sources | `/etc/grafana/provisioning/datasources/` | YAML |
| Dashboards | `/etc/grafana/provisioning/dashboards/` | YAML + JSON |
| Alerting | `/etc/grafana/provisioning/alerting/` | YAML |
| Notifiers | `/etc/grafana/provisioning/notifiers/` | YAML |
| Plugins | `/etc/grafana/provisioning/plugins/` | YAML |

## Dashboard as Code

### Options

| Tool | Language | Complexity |
|------|----------|------------|
| Grafonnet | Jsonnet | Medium |
| grafana-dashboard-builder | Python | Low |
| Terraform | HCL | Medium |
| Crossplane | YAML | Medium |

### Grafonnet Example

```jsonnet
local grafana = import 'grafonnet/grafana.libsonnet';

grafana.dashboard.new('My Dashboard')
.addPanel(
  grafana.graphPanel.new('CPU Usage')
  .addTarget(prometheus.target('rate(cpu_usage[5m])'))
)
```

## High Availability Requirements

### Database

| Database | Support | Recommendation |
|----------|---------|----------------|
| SQLite | Single node only | Dev/testing |
| PostgreSQL | HA supported | Production |
| MySQL | HA supported | Production |

### Shared Storage

- Plugins directory
- Dashboard JSON files (if file-based provisioning)
- Alert images (if using image rendering)

### Load Balancer

- SSL termination recommended
- No session affinity required (sessions stored in DB)
- Health check endpoint: `/api/health`

## Security Checklist

- [ ] Change default admin credentials
- [ ] Enable HTTPS/TLS
- [ ] Configure authentication (OAuth, LDAP, SAML)
- [ ] Set up RBAC for dashboards/data sources
- [ ] Restrict anonymous access
- [ ] Enable audit logging
- [ ] Configure secrets management
- [ ] Network policies (Kubernetes)

## Monitoring Grafana

Monitor your Grafana instance with:

- `/metrics` endpoint (Prometheus format)
- `/api/health` for health checks
- Built-in analytics dashboard

Key metrics:

| Metric | Description |
|--------|-------------|
| `grafana_http_request_duration_seconds` | Request latency |
| `grafana_alerting_active_alerts` | Active alerts count |
| `grafana_datasource_request_total` | Data source queries |
| `grafana_api_response_status_total` | API response codes |

## Version Compatibility

| Grafana Version | Helm Chart | Notes |
|-----------------|------------|-------|
| 11.x | 8.x | Current stable |
| 10.x | 7.x | LTS until 2025 |
| 9.x | 6.x | End of support |

## Related Documentation

- [grafana-basics.md](../grafana-basics.md) - Panel types and concepts
- [prometheus-monitoring.md](../prometheus-monitoring.md) - Metrics collection
- [elk-stack-logging.md](../elk-stack-logging.md) - Log aggregation

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Grafana Helm Charts](https://grafana.github.io/helm-charts/)
- [High Availability Setup](https://grafana.com/docs/grafana/latest/setup-grafana/set-up-for-high-availability/)
- [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Grafana Alloy](https://grafana.com/docs/alloy/latest/)
- [K8s Monitoring Helm Chart 2.0](https://grafana.com/blog/2025/01/23/kubernetes-monitoring-helm-chart-2.0-a-simpler-more-predictable-experience/)
