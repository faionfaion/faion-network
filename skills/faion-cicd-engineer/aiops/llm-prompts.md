# AIOps LLM Prompts

Prompts for AI assistants working with AIOps implementations.

## Anomaly Detection Prompts

### Analyze Prometheus Metrics for Anomalies

```
You are an AIOps expert analyzing Prometheus metrics. Given the following metric data:

Metric: {METRIC_NAME}
Time range: {START_TIME} to {END_TIME}
Values: {VALUES_ARRAY}
Baseline (7-day average): {BASELINE_VALUE}
Standard deviation: {STDDEV_VALUE}

Analyze for anomalies using these criteria:
1. Z-score threshold: Values >3 standard deviations from baseline
2. Trend analysis: Sudden changes in rate of change
3. Seasonality: Compare to same time period last week

Provide:
1. Is this an anomaly? (yes/no with confidence 0-100%)
2. Anomaly type (spike, drop, drift, pattern_break)
3. Severity (low/medium/high/critical)
4. Possible causes based on metric type
5. Recommended investigation steps
```

### Multi-Signal Incident Evaluation

```
You are evaluating whether multiple anomaly signals constitute an incident.

Detected anomalies:
{ANOMALY_LIST}

For each anomaly, I have:
- Metric name
- Current value
- Deviation from baseline
- Duration of anomaly
- Service/component affected

Rules:
- Minimum 2 convergent signals required for incident
- Signals must affect related components (same service or dependent services)
- Time correlation: anomalies should occur within 5-minute window

Evaluate and provide:
1. Is this an incident? (yes/no)
2. Incident severity
3. Affected service topology
4. Root cause hypothesis (most likely cause)
5. Recommended immediate actions
```

### Baseline Learning Analysis

```
Analyze the following historical data to establish a baseline for anomaly detection:

Metric: {METRIC_NAME}
Service: {SERVICE_NAME}
Data period: {DAYS} days
Data points: {DATA_POINTS}

Consider:
1. Daily patterns (working hours vs off-hours)
2. Weekly patterns (weekdays vs weekends)
3. Monthly patterns (start/end of month)
4. Any detected seasonality

Output:
1. Normal range (min, max, mean, median)
2. Standard deviation
3. Detected patterns with schedules
4. Recommended alert thresholds (warning, critical)
5. Suggested anomaly detection algorithm (z-score, isolation forest, prophet)
6. Confidence level in baseline quality
```

## Automated Remediation Prompts

### Generate Remediation Runbook

```
Generate an automated remediation runbook for the following incident type:

Incident: {INCIDENT_TYPE}
Service: {SERVICE_NAME}
Environment: {ENVIRONMENT}
Technology stack: {TECH_STACK}

Previous similar incidents:
{INCIDENT_HISTORY}

Create a runbook with:
1. Pre-conditions to verify before remediation
2. Step-by-step remediation actions
3. Verification steps after each action
4. Rollback procedure if remediation fails
5. Escalation criteria
6. Human approval checkpoints (if needed)

Format as YAML suitable for automation:
```yaml
runbook:
  name: ...
  trigger: ...
  trust_level: auto|recommend|human_approve
  steps:
    - action: ...
      verify: ...
      rollback: ...
```
```

### Evaluate Remediation Action Risk

```
Evaluate the risk of the following remediation action:

Action: {ACTION_TYPE}
Target: {TARGET_RESOURCE}
Environment: {ENVIRONMENT}
Current time: {TIMESTAMP}
Business hours: {BUSINESS_HOURS}
Recent deployments: {RECENT_DEPLOYMENTS}
Current traffic level: {TRAFFIC_LEVEL}

Assess:
1. Impact scope (how many users/services affected)
2. Reversibility (how easy to undo)
3. Time to execute
4. Probability of success based on historical data
5. Risk of cascading failures

Provide:
1. Risk score (1-10)
2. Recommended trust level (auto/recommend/human_approve/manual_only)
3. Required approvals
4. Suggested execution window
5. Monitoring focus during execution
```

### Post-Remediation Analysis

```
Analyze the outcome of the following remediation:

Incident: {INCIDENT_ID}
Remediation action: {ACTION_TAKEN}
Execution time: {EXECUTION_TIME}
Before metrics: {BEFORE_METRICS}
After metrics: {AFTER_METRICS}
Duration to resolution: {DURATION}

Evaluate:
1. Was the remediation successful? (yes/partial/no)
2. Time to recovery
3. Any side effects observed
4. Comparison to similar past remediations
5. Suggestions for improving the runbook

Generate lessons learned for the knowledge base.
```

## Predictive Analytics Prompts

### Capacity Planning Forecast

```
Forecast resource capacity needs based on historical trends:

Resource: {RESOURCE_TYPE}
Current usage: {CURRENT_USAGE}
Capacity limit: {CAPACITY_LIMIT}
Historical data: {TIME_SERIES_DATA}
Expected events: {KNOWN_EVENTS}

Provide:
1. Forecast for next 7/14/30 days
2. Days until capacity threshold (80%, 90%, 100%)
3. Confidence interval
4. Recommended scaling actions with timing
5. Cost estimate for additional capacity
6. Alternative optimization suggestions
```

### Failure Prediction Analysis

```
Analyze system health indicators for failure prediction:

Service: {SERVICE_NAME}
Metrics snapshot:
- CPU: {CPU_USAGE}
- Memory: {MEMORY_USAGE}
- Disk I/O: {DISK_IO}
- Network latency: {LATENCY}
- Error rate: {ERROR_RATE}
- Request rate: {REQUEST_RATE}
- GC pause time: {GC_PAUSE}
- Thread count: {THREAD_COUNT}

Historical failures for this service:
{FAILURE_HISTORY}

Predict:
1. Failure probability in next hour (0-100%)
2. Risk level (low/medium/high/critical)
3. Most likely failure mode
4. Top 3 contributing factors
5. Preventive actions recommended
6. Monitoring alerts to configure
```

## Root Cause Analysis Prompts

### Automated RCA

```
Perform root cause analysis for the following incident:

Incident timeline:
{TIMELINE_EVENTS}

Affected services:
{SERVICE_LIST}

Metric anomalies:
{ANOMALY_DATA}

Recent changes (24h):
- Deployments: {DEPLOYMENTS}
- Config changes: {CONFIG_CHANGES}
- Infrastructure changes: {INFRA_CHANGES}

Dependent services:
{DEPENDENCY_MAP}

Analyze and provide:
1. Most probable root cause (with confidence %)
2. Contributing factors
3. Affected blast radius
4. Evidence supporting the hypothesis
5. Alternative hypotheses to investigate
6. Preventive measures for future
```

### Postmortem Generation

```
Generate a postmortem document for:

Incident ID: {INCIDENT_ID}
Duration: {START_TIME} to {END_TIME}
Severity: {SEVERITY}
Services affected: {SERVICES}
Customer impact: {IMPACT}

Timeline:
{TIMELINE}

Root cause:
{ROOT_CAUSE}

Remediation actions:
{ACTIONS}

Generate a postmortem with:
1. Executive summary (2-3 sentences)
2. Impact assessment (users, revenue, SLA)
3. Timeline of events
4. Root cause analysis
5. What went well
6. What could be improved
7. Action items with owners and due dates
8. Lessons learned
9. Recommendations for detection/prevention
```

## Integration Prompts

### CI/CD Risk Assessment

```
Assess deployment risk for the following change:

Pull request: {PR_DETAILS}
Changed files:
{FILE_CHANGES}

Change categories:
- Infrastructure: {INFRA_CHANGES}
- Database: {DB_CHANGES}
- API: {API_CHANGES}
- Frontend: {FRONTEND_CHANGES}

Test results: {TEST_RESULTS}
Code coverage delta: {COVERAGE_DELTA}

Recent deployment history:
{DEPLOYMENT_HISTORY}

Assess:
1. Deployment risk score (1-10)
2. Risk factors identified
3. Recommended deployment strategy (standard/canary/blue-green)
4. Required monitoring during rollout
5. Rollback triggers to configure
6. Approval requirements
```

### Alert Correlation

```
Correlate and deduplicate the following alerts:

Active alerts:
{ALERT_LIST}

For each alert:
- Alert name
- Source
- Severity
- Start time
- Affected resource
- Labels/tags

Correlation rules:
- Time window: 5 minutes
- Same service
- Related metrics (CPU + Memory + Latency)
- Dependency chain

Provide:
1. Grouped alert clusters
2. Primary incident for each cluster
3. Root alert (likely cause)
4. Symptom alerts (effects)
5. Suggested combined alert name
6. Unified severity
7. Recommended notification strategy (avoid alert fatigue)
```

## Usage Guidelines

1. **Context is key** - Always provide full context including environment, tech stack, and historical data
2. **Be specific** - Use actual metric names, service names, and values when possible
3. **Request structured output** - Ask for YAML/JSON when automation will consume the response
4. **Include constraints** - Specify trust levels, approval requirements, and safety boundaries
5. **Iterate** - Use follow-up prompts to refine analysis or get more details

---

*AIOps LLM Prompts | faion-cicd-engineer*
