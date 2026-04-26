# ELK Stack LLM Prompts

## Architecture & Planning

### Design ELK Architecture

```
I need to design an ELK Stack architecture for the following requirements:

- Environment: [production/staging/development]
- Daily log volume: [X GB/day]
- Retention period: [X days]
- Number of log sources: [applications, infrastructure, etc.]
- High availability required: [yes/no]
- Budget constraints: [if any]

Please provide:
1. Recommended cluster topology (node types, counts)
2. Hardware specifications per node type
3. Storage requirements calculation
4. Network architecture
5. Cost estimation if cloud-based
```

### Capacity Planning

```
Help me calculate ELK Stack capacity for:

- Current daily log volume: [X GB]
- Expected growth rate: [X% per month]
- Retention requirements: [X days]
- Search performance SLA: [latency requirements]
- Replication factor: [X replicas]

Calculate:
1. Total storage needed (with growth projection for 1 year)
2. Number of data nodes required
3. JVM heap sizing per node
4. Shard count and sizing strategy
5. When to add capacity based on growth
```

---

## Elasticsearch Configuration

### Index Template Design

```
Create an Elasticsearch index template for [log type] with these requirements:

- Log format: [JSON/plain text/structured]
- Key fields: [list fields: timestamp, level, service, message, etc.]
- Search requirements: [full-text on message, exact match on service, etc.]
- Aggregation needs: [count by level, histogram by time, etc.]
- Retention: [X days]
- Expected document size: [X KB average]

Include:
1. Mapping with appropriate field types
2. Index settings (shards, replicas, refresh interval)
3. ILM policy attachment
4. Alias configuration for rollover
```

### ILM Policy Design

```
Create an ILM policy for [use case] with these phases:

Hot phase:
- Max age: [X days]
- Max size: [X GB]
- Priority: [X]

Warm phase (if needed):
- Trigger: [X days after rollover]
- Actions: [shrink, forcemerge, etc.]

Cold phase (if needed):
- Trigger: [X days]
- Actions: [freeze, move to cold storage]

Delete phase:
- Trigger: [X days total retention]

Include allocation requirements for hot/warm/cold node attributes.
```

### Optimize Slow Queries

```
I have this slow Elasticsearch query taking [X seconds]:

```json
[paste query here]
```

Index mapping:
```json
[paste relevant mapping]
```

Index has [X] documents, [X] shards.

Please:
1. Identify performance bottlenecks
2. Suggest query optimizations
3. Recommend mapping changes if needed
4. Propose index settings adjustments
5. Consider if a different query approach would be better
```

---

## Logstash Pipeline

### Parse Custom Log Format

```
Create a Logstash filter to parse this log format:

Sample logs:
```
[paste 5-10 sample log lines]
```

Requirements:
- Extract these fields: [list required fields]
- Handle multiline: [yes/no, pattern if yes]
- Enrich with: [geoip, user agent parsing, etc.]
- Mask sensitive data: [passwords, credit cards, etc.]
- Output index pattern: [logs-{service}-%{+YYYY.MM.dd}]

Include error handling for malformed logs.
```

### Pipeline Performance Tuning

```
My Logstash pipeline is processing [X events/second] but I need [Y events/second].

Current configuration:
- Pipeline workers: [X]
- Batch size: [X]
- Input: [beats/kafka/file]
- Filters: [list filters used]
- Output: [elasticsearch]

System specs:
- CPU cores: [X]
- RAM: [X GB]
- Disk type: [SSD/HDD]

Please suggest:
1. Pipeline configuration optimizations
2. JVM tuning recommendations
3. Filter optimization strategies
4. Scaling options (horizontal vs vertical)
```

### Multi-Pipeline Architecture

```
Design a Logstash multi-pipeline architecture for:

Log sources:
1. [Application logs - X events/sec]
2. [Nginx access logs - Y events/sec]
3. [Security logs - Z events/sec]
4. [Metrics - N events/sec]

Requirements:
- Isolate heavy processing from lightweight parsing
- Different retention/routing per log type
- Failure in one pipeline shouldn't affect others
- Resource allocation per pipeline

Provide pipelines.yml and individual pipeline configs.
```

---

## Filebeat Configuration

### Kubernetes Autodiscover

```
Configure Filebeat autodiscover for Kubernetes with:

- Namespace filtering: [include/exclude namespaces]
- Pod annotation-based config: [yes/no]
- JSON log parsing: [yes/no]
- Multiline handling for: [Java stack traces, Python tracebacks]
- Add Kubernetes metadata: [pod, namespace, node, labels]
- Custom processors per app type: [list app types with requirements]

Include DaemonSet-compatible configuration.
```

### Application-Specific Config

```
Create Filebeat configuration for [application type]:

Application: [Java Spring Boot / Node.js / Python / Go / etc.]
Log location: [path]
Log format: [JSON / logback pattern / custom]
Sample log:
```
[paste sample]
```

Requirements:
- Parse into structured fields
- Handle multiline (stack traces)
- Extract trace/span IDs for distributed tracing
- Add custom fields: [service name, environment, version]
- Ship to: [Elasticsearch directly / Logstash]
```

---

## Kibana Queries & Dashboards

### Build KQL Query

```
Help me build a KQL query to find:

[Describe what you're looking for in natural language]

Available fields:
- @timestamp (date)
- level (keyword): DEBUG, INFO, WARN, ERROR
- service (keyword): [list services]
- message (text): log message content
- [list other relevant fields]

Requirements:
- Time range: [last X hours/days]
- Must include: [conditions]
- Must exclude: [conditions]
- Sort by: [field and order]
```

### Dashboard Design

```
Design a Kibana dashboard for [purpose: operations/security/business]:

Target audience: [DevOps/Developers/Management]
Key metrics to display:
1. [metric 1]
2. [metric 2]
3. [metric 3]

Visualizations needed:
- Time series: [what to show over time]
- Aggregations: [counts, averages, percentiles]
- Tables: [what data to list]
- Maps: [geographic data if applicable]

Data source index pattern: [logs-*]

Provide:
1. Dashboard layout recommendation
2. Visualization definitions (type, aggregations, filters)
3. Filters and controls to include
4. Drill-down capabilities
```

### Alerting Rules

```
Create Kibana alerting rules for:

Scenario: [describe the alert scenario]

Conditions:
- Threshold: [count/rate/percentage]
- Time window: [X minutes]
- Group by: [field if applicable]

Actions:
- Notification channels: [Slack/email/PagerDuty]
- Message template: [what info to include]
- Recovery notification: [yes/no]

Provide:
1. Rule configuration (KQL/ES query)
2. Threshold settings
3. Action configuration
4. Recommended check interval
```

---

## Troubleshooting

### Diagnose Cluster Issues

```
My Elasticsearch cluster is showing [symptom]:

Symptoms:
- Cluster status: [red/yellow]
- Error messages: [paste relevant errors]
- Recent changes: [what changed before issue]

Cluster info:
- Version: [X.X.X]
- Node count: [X]
- Index count: [X]
- Total data size: [X GB]

Please help:
1. Identify likely root cause
2. Provide diagnostic commands to run
3. Suggest remediation steps
4. Recommend preventive measures
```

### Debug Ingestion Pipeline

```
Logs are not appearing in Elasticsearch. Debug the pipeline:

Architecture: [Filebeat -> Logstash -> Elasticsearch / Filebeat -> Elasticsearch]

Symptoms:
- [describe what's happening/not happening]

Checks already done:
- [list what you've verified]

Please provide:
1. Step-by-step debugging checklist
2. Commands to verify each component
3. Common issues to check
4. Log locations to examine
```

### Performance Investigation

```
Investigate ELK performance issue:

Problem: [slow queries / high latency / memory pressure / disk issues]

Metrics:
- CPU usage: [X%]
- Heap usage: [X%]
- Disk I/O: [if known]
- Query latency: [X ms]
- Indexing rate: [X docs/sec]

When it started: [time/date or event that triggered]
Correlation with: [deployment, traffic spike, etc.]

Provide:
1. Diagnostic queries to run
2. Metrics to examine
3. Likely causes ranked by probability
4. Resolution steps for each cause
```

---

## Migration & Upgrades

### Version Upgrade Plan

```
Plan upgrade from Elasticsearch [current version] to [target version]:

Current setup:
- Cluster size: [X nodes]
- Data size: [X TB]
- Downtime tolerance: [zero/minimal/acceptable window]
- Client applications: [list apps using ES]

Provide:
1. Pre-upgrade checklist
2. Upgrade strategy (rolling/full restart)
3. Step-by-step upgrade procedure
4. Rollback plan
5. Post-upgrade validation steps
```

### Data Migration

```
Migrate data from [source] to ELK Stack:

Source system: [Splunk/CloudWatch/custom/etc.]
Data volume: [X GB total, X GB/day ongoing]
Data format: [describe format]
Historical data: [how far back to migrate]

Requirements:
- Zero data loss
- Minimal impact on source system
- Field mapping to ELK schema
- Validation of migrated data

Provide:
1. Migration architecture
2. Tool recommendations
3. Step-by-step migration plan
4. Validation queries
```

---

## Security Configuration

### RBAC Setup

```
Design RBAC for ELK Stack with these user types:

1. [Admin - full access]
2. [Developer - read logs for their services]
3. [Support - read-only all logs]
4. [Auditor - read security logs only]

Requirements:
- Index-level permissions
- Field-level security: [hide PII fields from certain roles]
- Document-level security: [filter by tenant/environment]
- Kibana space separation: [if needed]

Provide:
1. Role definitions
2. User mappings
3. Kibana space configuration
4. API key policies for automation
```

### Security Hardening

```
Harden ELK Stack for [compliance requirement: SOC2/HIPAA/PCI-DSS/GDPR]:

Current state:
- TLS: [enabled/disabled]
- Authentication: [native/LDAP/SAML]
- Network: [public/private]

Provide:
1. Security configuration checklist
2. Network architecture recommendations
3. Encryption requirements
4. Audit logging setup
5. Access control policies
6. Data retention/deletion procedures for compliance
```

---

## Cost Optimization

### Reduce Storage Costs

```
Optimize ELK storage costs:

Current state:
- Total storage: [X TB]
- Monthly cost: [$X]
- Retention: [X days]
- Index patterns: [list]

Usage patterns:
- How often old data is queried: [frequently/rarely/never]
- Critical vs nice-to-have data: [describe]

Provide:
1. Storage tier recommendations (hot/warm/cold/frozen)
2. Compression strategies
3. Retention policy adjustments
4. Index optimization (shrink, forcemerge)
5. Projected cost savings
```

### Right-Size Cluster

```
Right-size ELK cluster for actual usage:

Current resources:
- [X] nodes with [specs]
- Total cost: [$X/month]

Actual metrics (last 30 days):
- Peak CPU: [X%]
- Peak memory: [X%]
- Peak disk I/O: [if known]
- Search rate: [X queries/min]
- Indexing rate: [X docs/sec]

Provide:
1. Assessment of over/under provisioning
2. Recommended node configuration
3. Scaling triggers to monitor
4. Cost comparison (current vs recommended)
```
