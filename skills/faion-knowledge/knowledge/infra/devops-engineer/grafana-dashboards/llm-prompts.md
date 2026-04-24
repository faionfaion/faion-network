# LLM Prompts for Grafana Dashboards

AI prompts for generating, analyzing, and optimizing Grafana dashboards.

## Dashboard Generation Prompts

### RED Method Dashboard

```
Create a Grafana dashboard JSON for monitoring a [SERVICE_TYPE] service using the RED method.

Requirements:
- Service name: [SERVICE_NAME]
- Metrics prefix: [METRICS_PREFIX] (e.g., http_requests_total, http_request_duration_seconds)
- Data source: Prometheus
- Variables: namespace, service, interval

Include panels for:
1. Overview row with stat panels: Request Rate, Error Rate, P99 Latency, Availability
2. Request details row: Request rate by status (time series), Latency percentiles (time series)
3. Error analysis row: Error rate over time, Top error endpoints (table)

Use thresholds:
- Error rate: green < 1%, yellow < 5%, red >= 5%
- P99 latency: green < 500ms, yellow < 1s, red >= 1s
- Availability: red < 99.5%, yellow < 99.9%, green >= 99.9%

Output complete dashboard JSON with proper gridPos, fieldConfig, and options.
```

### USE Method Dashboard

```
Create a Grafana dashboard JSON for infrastructure monitoring using the USE method.

Requirements:
- Target: [INFRASTRUCTURE_TYPE] (e.g., Kubernetes nodes, VMs, bare metal)
- Metrics source: [METRICS_SOURCE] (e.g., node_exporter, kube-state-metrics)
- Data source: Prometheus
- Variables: node/instance, interval

Include sections for:
1. CPU: Utilization gauge, Saturation (load), Usage over time
2. Memory: Utilization gauge, Saturation (swap I/O), Usage over time
3. Disk: Utilization gauge, Saturation (I/O wait), I/O throughput
4. Network: Bandwidth utilization, Packet errors, Traffic over time

Use thresholds appropriate for production infrastructure:
- CPU: green < 70%, yellow < 90%, red >= 90%
- Memory: green < 80%, yellow < 95%, red >= 95%
- Disk: green < 70%, yellow < 90%, red >= 90%

Output complete dashboard JSON.
```

### SLO Dashboard

```
Create a Grafana dashboard JSON for SLO monitoring.

Requirements:
- Service: [SERVICE_NAME]
- SLO targets:
  - Availability: [TARGET]% (e.g., 99.9%)
  - Latency P99: [TARGET]ms (e.g., 500ms)
- Error budget period: [PERIOD] (e.g., 30 days)
- Data source: Prometheus

Include panels for:
1. Current SLO status: Availability gauge, Latency gauge
2. Error budget: Remaining budget gauge, Budget consumption rate
3. SLO over time: Availability trend, Latency trend
4. Burn rate alerts: Fast burn (2%), slow burn (5%)

Include annotations for:
- Deployments
- Incidents
- SLO breaches

Output complete dashboard JSON with proper SLO calculations.
```

### Kubernetes Namespace Dashboard

```
Create a Grafana dashboard JSON for Kubernetes namespace monitoring.

Requirements:
- Metrics: kube-state-metrics, cAdvisor
- Data source: Prometheus
- Variables: namespace, deployment, pod

Include sections for:
1. Deployment status: Total pods, Running/Pending/Failed counts, Restarts
2. Resource usage: CPU usage vs requests, Memory usage vs requests
3. Resource efficiency: CPU/Memory utilization percentage
4. Network: Ingress/egress traffic by pod
5. Pod details: Table with pod status, restarts, age

Add drill-down links to:
- Pod detail dashboard
- Container logs (Loki)

Output complete dashboard JSON.
```

## Query Generation Prompts

### PromQL Query Generation

```
Generate a PromQL query for [METRIC_DESCRIPTION].

Context:
- Available metrics: [LIST_METRICS]
- Labels: [LIST_LABELS]
- Time range: [TIME_RANGE]
- Aggregation: [AGGREGATION_REQUIREMENT]

Requirements:
- [SPECIFIC_REQUIREMENTS]

Output:
1. The PromQL query
2. Explanation of each function used
3. Expected output format
4. Performance considerations
```

### Recording Rule Generation

```
Create Prometheus recording rules for dashboard [DASHBOARD_NAME].

Current expensive queries:
1. [QUERY_1]
2. [QUERY_2]
3. [QUERY_3]

Requirements:
- Evaluation interval: [INTERVAL]
- Rule naming convention: [CONVENTION]
- Output YAML format for Prometheus

For each query, provide:
1. Recording rule name
2. Rule expression
3. Labels to preserve
4. Estimated cardinality reduction
```

## Dashboard Analysis Prompts

### Performance Optimization

```
Analyze this Grafana dashboard JSON for performance issues:

[DASHBOARD_JSON]

Check for:
1. Queries without appropriate time aggregation
2. High cardinality label selections
3. Missing recording rules for expensive queries
4. Inappropriate refresh rates
5. Too many panels loading simultaneously

Output:
1. List of identified issues with severity
2. Specific recommendations for each issue
3. Optimized query alternatives where applicable
4. Recording rules to create
```

### Best Practices Audit

```
Audit this Grafana dashboard against best practices:

[DASHBOARD_JSON]

Evaluate:
1. Dashboard purpose clarity (does it tell a story?)
2. Variable usage (are there enough filters?)
3. Panel organization (logical flow?)
4. Threshold configuration (visual indicators?)
5. Documentation (descriptions, links?)
6. Color consistency
7. Unit configuration
8. Legend positioning

Output:
1. Score (1-10) for each category
2. Specific issues found
3. Recommendations for improvement
4. Priority order for fixes
```

### Migration Assistant

```
Convert this [SOURCE_FORMAT] dashboard to Grafana JSON:

[SOURCE_DASHBOARD]

Requirements:
- Target Grafana version: [VERSION]
- Data source mapping: [MAPPING]
- Preserve: [ELEMENTS_TO_PRESERVE]

Output:
1. Complete Grafana dashboard JSON
2. List of elements that couldn't be converted
3. Manual adjustments needed
4. Warnings about functionality differences
```

## Alert Rule Prompts

### Alert Generation

```
Create Grafana alerting rules for [SERVICE_NAME].

Metrics available:
- [LIST_METRICS]

Create alerts for:
1. High error rate (symptom-based)
2. High latency (P99 > threshold)
3. Low availability
4. Resource exhaustion warnings
5. Anomaly detection (if applicable)

Requirements:
- Severity levels: critical, warning, info
- Include runbook URLs
- Include dashboard links
- Multi-dimensional alerts where appropriate

Output:
1. Prometheus alerting rules YAML
2. Grafana alert rules JSON
3. Recommended notification routing
```

### Alert Optimization

```
Review and optimize these alerting rules:

[ALERTING_RULES]

Check for:
1. Alert fatigue (too sensitive)
2. Missing for duration
3. Alerting on causes vs symptoms
4. Missing labels for routing
5. Incomplete annotations
6. Missing runbook links

Output:
1. Issues found with each rule
2. Optimized rule versions
3. Additional rules to consider
4. Alert routing recommendations
```

## Variable and Filter Prompts

### Variable Generation

```
Generate Grafana template variables for [USE_CASE].

Available label dimensions:
- [LIST_LABELS]

Requirements:
- Enable multi-select where appropriate
- Set up dependent variables (chained)
- Include "All" option where useful
- Configure appropriate refresh settings

Output:
1. Variable definitions JSON
2. Dependency order
3. Default values recommendations
4. Query optimization tips for large cardinality
```

## Transformation Prompts

### Data Transformation

```
Create Grafana transformations to achieve [DESIRED_OUTPUT].

Input data format:
[INPUT_FORMAT]

Desired output:
[OUTPUT_FORMAT]

Requirements:
- [SPECIFIC_REQUIREMENTS]

Output:
1. Transformation steps in order
2. Configuration for each transformation
3. Alternative approaches if available
4. Limitations to be aware of
```

## Documentation Prompts

### Dashboard Documentation

```
Generate documentation for this Grafana dashboard:

[DASHBOARD_JSON]

Include:
1. Dashboard overview and purpose
2. Target audience
3. Key metrics explained
4. Variable usage guide
5. Drill-down navigation
6. Related dashboards
7. Troubleshooting common issues
8. Maintenance notes

Output in Markdown format suitable for a wiki or README.
```

### Runbook Generation

```
Generate runbook for alert [ALERT_NAME].

Alert definition:
[ALERT_DEFINITION]

Dashboard context:
[DASHBOARD_CONTEXT]

Include:
1. Alert meaning and severity
2. Potential causes
3. Diagnostic steps
4. Remediation actions
5. Escalation path
6. Prevention measures
7. Related alerts

Output in Markdown format.
```
