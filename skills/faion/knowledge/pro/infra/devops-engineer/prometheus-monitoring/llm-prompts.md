# LLM Prompts for Prometheus Monitoring

## Setup and Configuration

### Initial Prometheus Setup

```
I need to set up Prometheus monitoring for my Kubernetes cluster.

Context:
- Cluster: [GKE/EKS/AKS/on-prem]
- Node count: [X nodes]
- Namespaces to monitor: [list namespaces]
- Expected time series: [estimate or unknown]
- Storage requirements: [X days retention]
- HA requirements: [yes/no]

Please provide:
1. Helm values for kube-prometheus-stack
2. Resource sizing recommendations
3. Storage configuration
4. Initial alerting rules for cluster health
```

### ServiceMonitor Creation

```
Create a ServiceMonitor for my application:

Application details:
- Name: [app-name]
- Namespace: [namespace]
- Metrics port: [port-number]
- Metrics path: [/metrics or custom]
- Labels: [key=value pairs]
- Scrape interval: [15s/30s/60s]

Additional requirements:
- [x] Drop Go runtime metrics
- [ ] Add custom relabeling
- [ ] Multi-namespace selection

Output as Kubernetes YAML.
```

### Alertmanager Configuration

```
Configure Alertmanager routing for my organization:

Teams and channels:
- Team A: Slack #team-a-alerts, PagerDuty for critical
- Team B: Slack #team-b-alerts, email for all
- Platform: Slack #platform-alerts, PagerDuty for critical

Routing requirements:
- Critical alerts: 2-minute repeat, page immediately
- Warning alerts: 4-hour repeat
- Info alerts: 24-hour repeat
- Group by: alertname, namespace, severity

Provide complete alertmanager.yaml configuration.
```

---

## PromQL Query Development

### Request Metrics Query

```
Write a PromQL query for:

Metric: http_requests_total
Goal: [request rate / error rate / success rate]
Aggregation: by [service / endpoint / method / status]
Time window: [5m / 15m / 1h]
Filters:
- namespace: [namespace]
- status codes: [2xx / 5xx / specific codes]

Include:
1. The query
2. Explanation of what it measures
3. Example output interpretation
```

### Latency Analysis Query

```
Write PromQL queries for latency analysis:

Metric: http_request_duration_seconds (histogram)
Requirements:
- P50, P90, P95, P99 percentiles
- By: [endpoint / service / method]
- Time window: [5m]
- Filter: namespace=[namespace]

Also provide:
- Apdex score calculation (satisfied <0.5s, tolerating <2s)
- Query for latency degradation detection
```

### Resource Usage Query

```
Write PromQL for Kubernetes resource monitoring:

Requirements:
- CPU usage percentage vs limits
- Memory usage percentage vs limits
- CPU throttling detection
- Memory pressure detection

Target:
- Namespace: [namespace]
- Deployment/Pod: [name or all]

Output:
1. Queries for each metric
2. Thresholds for alerting
3. Dashboard panel recommendations
```

### Custom Metric Query

```
Help me write a PromQL query:

I have this metric: [metric_name]
Labels: [list labels]
Type: [counter/gauge/histogram/summary]

I want to:
[Describe what you want to measure]

Current query attempt (optional):
[Your query]

Problem/question:
[What's not working or what you're unsure about]
```

---

## Alerting Rules Development

### SLO-Based Alerts

```
Create SLO-based alerting rules:

Service: [service-name]
SLOs:
- Availability: [99.9% / 99.95% / 99.99%]
- Latency P99: [<500ms / <1s / <2s]
- Error rate: [<1% / <0.1%]

Budget period: [30 days]

Provide:
1. Recording rules for SLIs
2. Error budget burn rate alerts (fast and slow burn)
3. Multi-window, multi-burn-rate alerting strategy
4. Alert annotations with runbook links
```

### Application Alerts

```
Create alerting rules for my application:

Application: [app-name]
Namespace: [namespace]
Team: [team-name]

Alert requirements:
- High error rate (>X%)
- High latency (P99 > Xs)
- Pod crash looping
- High memory usage (>85%)
- CPU throttling
- Deployment replica mismatch

For each alert include:
- Appropriate `for` duration
- Severity level
- Runbook URL placeholder
- Dashboard URL placeholder
```

### Infrastructure Alerts

```
Create infrastructure alerting rules:

Scope:
- [ ] Node-level alerts
- [ ] Cluster-level alerts
- [ ] Storage alerts
- [ ] Network alerts

Specific requirements:
[List specific conditions to alert on]

Environment: [production/staging/development]

Provide PrometheusRule YAML with appropriate thresholds.
```

---

## Troubleshooting

### High Cardinality Investigation

```
Help me investigate high cardinality in Prometheus:

Symptoms:
- Memory usage: [current usage]
- Time series count: [if known]
- Slow queries: [describe slow queries]
- OOM events: [yes/no]

Current configuration:
- Retention: [X days]
- Storage size: [X GB]
- Scrape targets: [count]

Provide:
1. PromQL queries to identify high-cardinality metrics
2. Queries to find label value explosion
3. Recommendations for reduction
4. Relabeling rules to drop problematic metrics
```

### Query Performance Optimization

```
Optimize this slow PromQL query:

Query:
[paste query]

Dashboard/alert context:
- Used in: [dashboard panel / alerting rule / API]
- Refresh interval: [Xs]
- Time range: [last X hours/days]

Current performance:
- Query time: [X seconds]
- Data points: [if known]

Provide:
1. Optimized query
2. Recording rules if beneficial
3. Explanation of improvements
```

### Target Scraping Issues

```
Debug Prometheus scraping issues:

Target: [target description]
Symptoms:
- [ ] Target not appearing in targets list
- [ ] Target shows as down
- [ ] Scrape errors in logs
- [ ] Metrics missing

Configuration:
- ServiceMonitor/PodMonitor: [yes/no, paste if yes]
- Service labels: [labels]
- Pod annotations: [if using annotations]
- Namespace: [namespace]

Network:
- NetworkPolicy: [yes/no]
- Istio/service mesh: [yes/no]

Provide step-by-step debugging guide.
```

---

## Dashboard Development

### Dashboard Design

```
Design a Grafana dashboard for:

Service: [service-name]
Purpose: [overview / debugging / SLO tracking / capacity planning]

Required panels:
- [ ] Request rate
- [ ] Error rate
- [ ] Latency percentiles
- [ ] Resource usage
- [ ] Custom metrics: [list]

Variables needed:
- Namespace selector
- Pod selector
- Time range

Provide:
1. Panel layout recommendations
2. PromQL for each panel
3. Threshold configurations
4. Variable definitions
```

### Dashboard JSON Generation

```
Generate Grafana dashboard JSON for:

Title: [Dashboard Title]
Folder: [Folder name]
Tags: [list tags]

Panels:
1. [Panel 1 description + query]
2. [Panel 2 description + query]
...

Variables:
- [Variable definitions]

Output as complete dashboard JSON compatible with Grafana 10+.
```

---

## Migration and Scaling

### Remote Write Setup

```
Configure Prometheus remote write:

Destination: [Thanos/Cortex/Mimir/VictoriaMetrics/Grafana Cloud]
Endpoint: [URL if known]

Requirements:
- Filter metrics: [include/exclude patterns]
- Batch size: [default/custom]
- Queue configuration: [if needed]
- Authentication: [bearer token/basic auth/mTLS]

Current setup:
- Time series count: [X]
- Ingestion rate: [samples/sec if known]

Provide:
1. Remote write configuration
2. Write relabeling rules
3. Queue tuning recommendations
4. Monitoring queries for remote write health
```

### Federation Setup

```
Configure Prometheus federation:

Architecture:
- Global Prometheus: [location]
- Regional Prometheus instances: [list locations]

Federation requirements:
- Aggregate only: [yes/no]
- Metrics to federate: [patterns/all]
- External labels: [labels for each instance]

Provide:
1. Global Prometheus scrape config
2. Regional Prometheus configuration
3. Recording rules for aggregation
4. Dashboard recommendations for global view
```

---

## Best Practices Review

### Configuration Audit

```
Review my Prometheus configuration:

[Paste prometheus.yaml or Helm values]

Focus areas:
- [ ] Resource sizing
- [ ] Retention settings
- [ ] Scrape configuration
- [ ] Rule evaluation
- [ ] Security settings
- [ ] High availability

Expected workload:
- Time series: [X]
- Scrape targets: [X]
- Query load: [low/medium/high]

Provide:
1. Issues found
2. Improvement recommendations
3. Priority order
```

### Metric Naming Review

```
Review my application's metric naming:

Metrics:
[List metrics with current names]

Application context:
- Language: [Go/Python/Node.js/etc]
- Framework: [if applicable]
- Domain: [web service/database/queue/etc]

Check for:
- Naming convention compliance
- Appropriate metric types
- Label consistency
- HELP strings
- Unit inclusion

Provide corrected names and rationale.
```

---

## Quick Reference Prompts

### Generate Recording Rule

```
Generate a recording rule for: [metric and aggregation]
Labels to preserve: [labels]
Evaluation interval: [30s/1m]
Output naming: [level:metric:operation format]
```

### Generate Alert Rule

```
Generate alert for: [condition description]
Severity: [critical/warning/info]
For duration: [Xm]
Team: [team-name]
Include runbook URL: [yes/no]
```

### Optimize for Grafana

```
Optimize this query for Grafana dashboards:
[query]
Use $__rate_interval variable: [yes/no]
Panel type: [timeseries/stat/gauge/table]
```

### Convert Metric Type

```
Help me convert from [summary/histogram] to [histogram/summary]:
Current metric: [metric definition]
Percentiles needed: [list]
Bucket boundaries: [list]
```
