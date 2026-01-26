# LLM Prompts for Grafana

## Dashboard Creation

### Create Application Dashboard

```
Create a Grafana dashboard JSON for monitoring a {service_type} application with:

Application: {app_name}
Namespace variable: yes
Data source: Prometheus

Include panels for:
1. Overview row with stat panels:
   - Request rate (req/s)
   - Error rate (%)
   - P99 latency (seconds)
   - Active pods count

2. Traffic row with time series:
   - Request rate by status code (2xx green, 4xx yellow, 5xx red)
   - Request rate by endpoint

3. Latency row:
   - Latency percentiles (p50, p95, p99)
   - Latency heatmap

4. Resources row:
   - CPU utilization by pod
   - Memory utilization by pod

5. Logs row (Loki):
   - Application logs filtered by namespace

Use these metrics:
- HTTP: http_requests_total, http_request_duration_seconds_bucket
- K8s: kube_pod_info, kube_pod_status_phase, container_cpu_usage_seconds_total, container_memory_usage_bytes

Add deployment annotations.
Set 30s refresh rate.
Use $__rate_interval for rate() functions.
```

### Create SLO Dashboard

```
Create a Grafana SLO dashboard JSON for:

Service: {service_name}
SLO targets:
- Availability: {availability_target}% (e.g., 99.9%)
- Latency P99: {latency_target}ms
- Error budget period: {period} (e.g., 30d)

Include:
1. Gauge panels showing current SLO compliance
2. Error budget remaining (percentage and time)
3. Burn rate indicators (1h, 6h, 24h windows)
4. Time series showing SLI trends over the budget period
5. Alert status panel

Use Prometheus metrics:
- http_requests_total for availability
- http_request_duration_seconds_bucket for latency

Color thresholds:
- Green: meeting SLO
- Yellow: within 10% of SLO breach
- Red: SLO breached
```

## Panel Creation

### Create Time Series Panel

```
Create a Grafana time series panel JSON for:

Title: {panel_title}
Metric: {prometheus_query}
Breakdown by: {label} (e.g., status, pod, endpoint)

Requirements:
- Legend as table on right with mean, max, last values
- Multi-tooltip sorted descending
- Smooth line interpolation
- 20% fill opacity
- Color overrides for specific values (if applicable)
- Unit: {unit} (e.g., reqps, bytes, seconds, percent)
- Thresholds: green < {warn_value}, yellow < {critical_value}, red >= {critical_value}

Grid position: {"h": 8, "w": 12, "x": {x}, "y": {y}}
```

### Create Stat Panel

```
Create a Grafana stat panel JSON for:

Title: {panel_title}
Metric: {prometheus_query}
Unit: {unit}

Requirements:
- Show last non-null value
- Color by value
- Area sparkline graph
- Thresholds: {threshold_config}
- Grid position: {"h": 4, "w": 6, "x": {x}, "y": {y}}
```

### Create Table Panel

```
Create a Grafana table panel JSON for:

Title: {panel_title}
Data: {prometheus_query}
Format: instant query, table format

Columns to show: {columns}
Columns to hide: Time, __name__, job, instance
Column renames: {rename_map}

Add status column with value mappings:
- Running: green
- Pending: yellow
- Failed: red

Sort by: {sort_column} descending
Grid position: {"h": 6, "w": 24, "x": 0, "y": {y}}
```

## Alert Creation

### Create Symptom-Based Alert

```
Create a Grafana alert rule for:

Alert name: {alert_name}
Condition: {condition_description}

Prometheus query: {query}
Threshold: {operator} {value} (e.g., > 5 for error rate > 5%)
Duration: {for_duration} (e.g., 5m)

Labels:
- severity: {critical|warning|info}
- team: {team_name}
- service: {service_name}

Annotations:
- summary: {brief_description}
- description: Include current value using {{ $values.A }}
- runbook_url: {runbook_link}

Focus on user-facing symptoms, not infrastructure events.
```

### Create Multi-Condition Alert

```
Create a Grafana alert with multiple conditions:

Alert name: {alert_name}

Conditions (ALL must be true):
1. {condition_1} (query, threshold)
2. {condition_2} (query, threshold)

OR conditions (ANY triggers):
1. {condition_1}
2. {condition_2}

Evaluation interval: 1m
For duration: {for_duration}

Include proper no-data and error handling states.
```

## Variable Creation

### Create Cascading Variables

```
Create Grafana variable definitions for cascading filters:

1. datasource variable (prometheus type)
2. namespace variable (query from kube_namespace_labels)
3. service variable (filtered by $namespace)
4. pod variable (filtered by $namespace and $service, multi-select, include all)

All variables should:
- Refresh on dashboard load or time range change as appropriate
- Be sorted alphabetically
- Have clear labels
```

## Dashboard Transformation

### Convert Dashboard to Template

```
Take this Grafana dashboard JSON and convert it to a reusable template:

{dashboard_json}

Requirements:
1. Replace hardcoded values with variables
2. Add datasource variable
3. Add namespace/environment variable
4. Parameterize thresholds where sensible
5. Add documentation Text panel
6. Ensure all panels use $__rate_interval
7. Add deployment/incident annotations
8. Output as provisioning-ready JSON
```

### Optimize Dashboard Performance

```
Analyze this Grafana dashboard and suggest optimizations:

{dashboard_json}

Check for:
1. Queries that could use recording rules
2. Panels with unnecessary high cardinality
3. Excessive refresh rates
4. Missing instant query flags on tables
5. Redundant panels that could be combined
6. Variables that refresh too frequently

Provide:
- List of issues found
- Suggested recording rules (PromQL)
- Optimized dashboard JSON
```

## Data Source Configuration

### Configure Prometheus with Exemplars

```
Create Grafana data source provisioning YAML for Prometheus with:

URL: {prometheus_url}
Features:
- Exemplars enabled, linked to Tempo
- Custom scrape interval: {interval}
- HTTP POST method
- Alerting enabled

Include correlations to Loki for logs.
```

### Configure Loki with Derived Fields

```
Create Grafana data source provisioning YAML for Loki with:

URL: {loki_url}
Features:
- Derived field to extract trace IDs
- Link to Tempo for distributed tracing
- Max lines: 1000

Pattern: traceID=(\w+) or trace_id=(\w+)
```

## Troubleshooting Prompts

### Debug Empty Panel

```
My Grafana panel shows "No data". Help me debug:

Panel config:
{panel_json}

Data source: {datasource_type}
Query: {query}

I've verified:
- [ ] Data source connectivity
- [ ] Metrics exist in Prometheus
- [ ] Time range is correct
- [ ] Variables resolve correctly

What else should I check? Provide step-by-step debugging.
```

### Fix Slow Dashboard

```
My Grafana dashboard is slow to load. Current config:

Dashboard: {dashboard_json}
Load time: {current_load_time}
Panel count: {panel_count}
Time range: {time_range}

Analyze and provide:
1. Which queries are likely slow
2. Recording rules to pre-compute
3. Panels to optimize or remove
4. Recommended refresh interval
```

## Migration Prompts

### Migrate from Grafana 9 to 11

```
Migrate this Grafana 9 dashboard to Grafana 11:

{old_dashboard_json}

Update:
- Schema version to 39
- Angular panels to React equivalents
- Deprecated panel options
- Alert rule format to unified alerting
- Variable syntax if needed

Output the updated JSON with migration notes.
```

---

*LLM Prompts for Grafana | faion-cicd-engineer*
