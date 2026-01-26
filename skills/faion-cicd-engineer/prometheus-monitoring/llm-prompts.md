# LLM Prompts for Prometheus Monitoring

## Setup and Configuration

### Generate Prometheus Helm Values

```
Generate a kube-prometheus-stack Helm values file for:
- Environment: [production/staging/development]
- Cluster name: [cluster-name]
- Region: [aws-region or gcp-zone]
- Storage class: [storage-class-name]
- Retention: [days] days
- Remote write: [yes/no, if yes specify URL]
- Alertmanager receivers: [slack/pagerduty/email, specify channels/keys]
- Include: [node-exporter/kube-state-metrics/grafana]

Follow best practices for high availability and resource limits.
```

### Create ServiceMonitor for Application

```
Create a Kubernetes ServiceMonitor for:
- Service name: [service-name]
- Namespace: [namespace]
- Metrics port: [port-name or number]
- Metrics path: [/metrics or custom path]
- Scrape interval: [15s/30s/60s]
- Labels to add: [key=value pairs]
- Metrics to drop: [regex pattern for metric names]

Include proper relabeling for pod and namespace labels.
```

### Configure Alertmanager Routing

```
Configure Alertmanager routing for:
- Teams: [list of teams with their Slack channels]
- Critical alerts: [PagerDuty service key, Slack channel]
- Warning alerts: [Slack channel]
- Default receiver: [channel/email]
- Repeat interval: [hours]

Include inhibition rules to suppress warnings when critical alerts are firing.
Include route grouping by alertname and namespace.
```

## Application Instrumentation

### Instrument Python/FastAPI Application

```
Generate Prometheus instrumentation code for a FastAPI application:
- Metrics to track:
  - HTTP request count (by method, endpoint, status)
  - HTTP request duration histogram
  - In-progress requests gauge
  - [Additional custom metrics: describe them]
- Include:
  - Decorator for automatic request tracking
  - /metrics endpoint
  - App version info metric
- Histogram buckets: [default or custom values]

Follow prometheus_client best practices.
```

### Instrument Node.js/Express Application

```
Generate Prometheus instrumentation code for an Express.js application:
- Metrics to track:
  - HTTP request count (by method, route, status)
  - HTTP request duration histogram
  - [Additional custom metrics]
- Include:
  - Express middleware
  - /metrics endpoint
  - Default Node.js metrics
- Use prom-client library.
```

### Instrument Go Application

```
Generate Prometheus instrumentation code for a Go HTTP application:
- Metrics to track:
  - HTTP request count
  - HTTP request duration histogram
  - [Custom business metrics]
- Include:
  - HTTP middleware
  - /metrics endpoint using promhttp
  - Build info metric
- Use prometheus/client_golang library.
```

## PromQL Queries

### Generate PromQL for SLI/SLO

```
Generate PromQL queries for SLI/SLO monitoring:
- Service name: [service-name]
- Availability SLO: [99.9%]
- Latency SLO: P99 < [threshold] seconds
- Error budget calculation

Include:
- Error rate calculation
- Latency percentile calculations (P50, P90, P99)
- Availability calculation
- Error budget remaining
- Burn rate for alerts
```

### Generate PromQL for Resource Monitoring

```
Generate PromQL queries for resource monitoring:
- Namespace: [namespace]
- Resources: [CPU, memory, disk, network]
- Include percentages against limits
- Include node-level aggregations

Queries should work with standard Kubernetes metrics from kube-state-metrics and cadvisor.
```

### Optimize Slow PromQL Query

```
Optimize this PromQL query for better performance:
[paste your slow query]

Context:
- Number of time series: [approximate count]
- Time range typically queried: [hours/days]
- Used in: [dashboard/alert/recording rule]

Suggest:
- Recording rules to pre-compute
- Label selector optimizations
- Aggregation improvements
```

## Alert Rules

### Generate Alert Rules for Microservice

```
Generate PrometheusRule with alert rules for:
- Service name: [service-name]
- Namespace: [namespace]
- Team: [team-name]
- Runbook base URL: [url]

Include alerts for:
- High error rate (threshold: [%], duration: [minutes])
- High latency P99 (threshold: [seconds], duration: [minutes])
- Pod restarts (threshold: [count] in [period])
- High memory usage (threshold: [%], duration: [minutes])
- CPU throttling (threshold: [%], duration: [minutes])
- Deployment unavailable

Each alert should have:
- Appropriate severity label
- Summary and description annotations
- Runbook URL
- Recommended `for` duration
```

### Generate CI/CD Pipeline Alerts

```
Generate alert rules for CI/CD pipeline monitoring:
- CI/CD tool: [Jenkins/GitLab CI/GitHub Actions/ArgoCD]
- Metrics source: [exporter name or custom]
- Team: [team-name]

Include alerts for:
- High failure rate
- Long queue times
- Slow pipelines
- [Tool-specific]:
  - ArgoCD: sync failures, unhealthy apps
  - Jenkins: executor starvation
  - GitLab: runner capacity

Include appropriate thresholds and durations.
```

### Review and Improve Alert Rules

```
Review these Prometheus alert rules and suggest improvements:

[paste your PrometheusRule YAML]

Check for:
- Missing `for` clause (flapping prevention)
- Appropriate severity levels
- Useful annotations (summary, description, runbook_url)
- Label best practices
- Query efficiency
- False positive potential
- Coverage gaps
```

## Dashboards

### Design Grafana Dashboard

```
Design a Grafana dashboard structure for:
- Service: [service-name]
- Dashboard purpose: [overview/debugging/SLO tracking]

Include panels for:
- [List specific metrics/visualizations needed]

For each panel, provide:
- Panel type (stat, timeseries, table, etc.)
- PromQL query
- Visualization settings
- Thresholds

Use variables for: namespace, pod, time range.
Follow RED method (Rate, Errors, Duration) or USE method (Utilization, Saturation, Errors).
```

### Generate Dashboard JSON

```
Generate Grafana dashboard JSON for:
- Service: [service-name]
- Panels:
  - Request rate (timeseries)
  - Error rate (stat with thresholds)
  - P50/P90/P99 latency (timeseries)
  - Pod CPU usage (timeseries)
  - Pod memory usage (timeseries)
  - [Additional panels]

Include:
- Prometheus datasource variable
- Namespace variable
- Pod variable
- Appropriate refresh interval
- Time range picker
```

## Troubleshooting

### Debug Missing Metrics

```
Help debug why metrics are not appearing in Prometheus:

Symptoms:
- Service: [service-name]
- Expected metric: [metric-name]
- Prometheus shows: [no data/partial data/error]

I've checked:
- [List what you've already verified]

Provide a systematic debugging checklist including:
- Target discovery verification
- Scrape config validation
- Network connectivity
- Metric endpoint testing
- Relabeling verification
```

### Debug High Cardinality

```
Help identify and fix high cardinality issues:

Symptoms:
- Prometheus memory: [current usage]
- Time series count: [count]
- Slow queries: [example queries]

Provide:
- PromQL to identify high cardinality metrics
- Common causes checklist
- Remediation strategies
- Recording rule suggestions to reduce cardinality
```

### Optimize Prometheus Performance

```
Help optimize Prometheus performance:

Current setup:
- Version: [version]
- Targets: [count]
- Scrape interval: [seconds]
- Retention: [days]
- Storage size: [GB]
- Memory usage: [GB]
- Query latency: [seconds for typical queries]

Issues:
- [Describe performance problems]

Suggest optimizations for:
- Scrape configuration
- Recording rules
- Retention settings
- Remote write configuration
- Resource allocation
- Query patterns
```

## Migration and Integration

### Migrate from Custom Metrics to Standard

```
Help migrate custom metrics to follow Prometheus naming conventions:

Current metrics:
[list current metric names]

For each metric:
- Suggest standard name following <namespace>_<name>_<unit>_total pattern
- Suggest appropriate labels
- Provide recording rules to maintain backward compatibility during migration
```

### Integrate with External System

```
Generate configuration to integrate Prometheus with:
- System: [Thanos/Cortex/VictoriaMetrics/Datadog/New Relic]
- Use case: [long-term storage/federation/migration]

Include:
- Remote write/read configuration
- Required labels
- Metric filtering
- Authentication setup
- Performance considerations
```

## Recording Rules

### Generate Recording Rules for Dashboard

```
Generate recording rules for a frequently-used dashboard:

Dashboard queries:
[paste the PromQL queries used in dashboard panels]

For each query:
- Create appropriate recording rule
- Follow naming convention: level:metric:operations
- Group related rules
- Set appropriate evaluation interval
```

### Generate SLO Recording Rules

```
Generate recording rules for SLO tracking:

Service: [service-name]
SLOs:
- Availability: [target %]
- Latency P99: [threshold] seconds

Generate:
- SLI recording rules
- Error budget calculation
- Burn rate recording rules (1h, 6h, 24h, 3d windows)
- Multi-window burn rate for alerts
```
