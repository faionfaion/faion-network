# ELK Stack LLM Prompts

## Cluster Design Prompts

### Initial Architecture Design

```
Design an ELK Stack architecture for the following requirements:

Environment: [production/staging/development]
Expected log volume: [X GB/day]
Retention requirement: [X days/months]
Number of applications: [X]
Deployment platform: [Docker/Kubernetes/VMs/Cloud]
Budget constraints: [high/medium/low]

Consider:
1. Node topology (master, data, ingest, coordinating)
2. Sharding strategy
3. Replica configuration
4. Hot-warm-cold tiers
5. Resource sizing (CPU, memory, storage)
6. High availability requirements
7. Disaster recovery approach

Output:
- Architecture diagram description
- Node specifications
- Estimated resource costs
- Scaling recommendations
```

### Capacity Planning

```
Calculate ELK Stack capacity requirements:

Current metrics:
- Daily log volume: [X GB]
- Number of log sources: [X]
- Average log size: [X KB]
- Peak ingestion rate: [X events/second]
- Query patterns: [dashboard refresh rate, concurrent users]
- Retention period: [X days]

Growth projections:
- Expected growth rate: [X% per month]
- Planning horizon: [X months]

Calculate:
1. Total storage needed
2. Number of data nodes required
3. Shard count and sizing
4. Memory requirements
5. CPU requirements
6. Network bandwidth needs
7. ILM policy thresholds
```

## Configuration Prompts

### Index Template Generation

```
Generate an Elasticsearch index template for:

Log type: [application/access/audit/metrics]
Fields to index:
- [field1]: [type, analyzed/keyword]
- [field2]: [type, analyzed/keyword]
- [field3]: [type, analyzed/keyword]

Requirements:
- Shard count: [X]
- Replica count: [X]
- Refresh interval: [X seconds]
- ILM policy: [policy name]

Generate:
1. Index template JSON
2. Mapping definitions with appropriate types
3. Settings for performance
4. Aliases configuration
```

### Logstash Pipeline Design

```
Design a Logstash pipeline for:

Input sources:
- [Source 1]: [format, protocol]
- [Source 2]: [format, protocol]

Log format examples:
```
[paste example log lines]
```

Processing requirements:
- Parse [specific fields]
- Enrich with [GeoIP, DNS, etc.]
- Mask sensitive data: [patterns]
- Transform: [specific transformations]

Output targets:
- Primary: [Elasticsearch/Kafka]
- Secondary: [optional]

Generate:
1. Complete pipeline configuration
2. Grok patterns for parsing
3. Filter chain logic
4. Error handling with DLQ
5. Performance tuning settings
```

### Filebeat Configuration

```
Generate Filebeat configuration for:

Log sources:
- [Path 1]: [log type, multiline?]
- [Path 2]: [log type, multiline?]

Deployment: [bare metal/Docker/Kubernetes]

Requirements:
- Multiline patterns: [yes/no, pattern]
- Additional fields: [service, environment]
- Processors needed: [list]
- Output: [Elasticsearch direct/Logstash]

Security:
- TLS: [yes/no]
- Authentication: [basic/API key]

Generate complete filebeat.yml with:
1. Input definitions
2. Multiline configuration
3. Processors
4. Output configuration
5. Logging settings
```

## Query Prompts

### KQL Query Generation

```
Generate KQL queries for the following use cases:

Index pattern: [logs-*]

Use cases:
1. [Find all errors in service X in the last hour]
2. [Find slow requests (>1s) with specific user]
3. [Count logs by level for each service]
4. [Find authentication failures by IP]

For each query, provide:
1. KQL query syntax
2. Equivalent Elasticsearch DSL
3. Suggested visualization type
4. Performance considerations
```

### Dashboard Query Optimization

```
Optimize these Kibana dashboard queries for better performance:

Current queries:
```
[paste current queries]
```

Dashboard refresh rate: [X seconds]
Index size: [X GB]
Concurrent users: [X]

Analyze and suggest:
1. Query rewrites for efficiency
2. Aggregation optimizations
3. Index/shard recommendations
4. Caching strategies
5. Pre-computed rollups if applicable
```

## Troubleshooting Prompts

### Cluster Health Issues

```
Diagnose ELK Stack cluster issue:

Symptoms:
- [Describe symptoms: slow queries, unassigned shards, etc.]

Cluster status:
```
[paste _cluster/health output]
```

Node stats:
```
[paste relevant _nodes/stats output]
```

Recent changes:
- [List any recent changes]

Analyze:
1. Root cause identification
2. Immediate remediation steps
3. Long-term fixes
4. Prevention measures
```

### Ingestion Problems

```
Troubleshoot log ingestion issues:

Problem:
- [Describe: logs not appearing, delays, parsing failures]

Components involved:
- Beats version: [X]
- Logstash version: [X]
- Elasticsearch version: [X]

Error messages:
```
[paste relevant error logs]
```

Configuration snippets:
```
[paste relevant config]
```

Diagnose:
1. Likely cause
2. Verification steps
3. Fix recommendations
4. Monitoring suggestions
```

### Performance Tuning

```
Optimize ELK Stack performance:

Current metrics:
- Indexing rate: [X docs/sec, target: Y]
- Search latency: [X ms, target: Y]
- CPU usage: [X%]
- Heap usage: [X%]
- GC frequency: [X]

Cluster configuration:
- Nodes: [count, specs]
- Indices: [count, avg size, shard count]
- Queries: [describe query patterns]

Identify:
1. Performance bottlenecks
2. Configuration improvements
3. Scaling recommendations
4. Query optimizations
5. Index optimizations
```

## Migration Prompts

### Version Upgrade Planning

```
Plan ELK Stack upgrade:

Current version: [X.Y.Z]
Target version: [A.B.C]

Cluster details:
- Node count: [X]
- Data size: [X TB]
- Criticality: [high/medium/low]

Generate:
1. Pre-upgrade checklist
2. Breaking changes to address
3. Upgrade procedure (rolling/full restart)
4. Rollback plan
5. Validation tests
6. Downtime estimation
```

### Cloud Migration

```
Plan migration to Elastic Cloud/AWS OpenSearch:

Current setup:
- Self-hosted: [Docker/K8s/VMs]
- Version: [X.Y.Z]
- Data size: [X TB]
- Ingestion rate: [X GB/day]

Target:
- Platform: [Elastic Cloud/AWS OpenSearch/Azure]
- Requirements: [HA, DR, compliance]

Generate:
1. Target architecture
2. Migration strategy (snapshot/reindex)
3. Network requirements
4. Cost estimation approach
5. Cutover procedure
6. Validation checklist
```

## Security Prompts

### RBAC Design

```
Design Elasticsearch RBAC for:

User groups:
- [Group 1]: [access needs]
- [Group 2]: [access needs]
- [Group 3]: [access needs]

Index patterns:
- [Pattern 1]: [sensitivity level]
- [Pattern 2]: [sensitivity level]

Requirements:
- Field-level security: [yes/no]
- Document-level security: [yes/no]
- Anonymous access: [yes/no]

Generate:
1. Role definitions
2. Role mappings
3. User creation scripts
4. API key policies
5. Audit logging config
```

### Security Hardening

```
Harden ELK Stack security:

Current state:
- TLS: [enabled/disabled]
- Authentication: [type]
- Authorization: [configured/not]
- Network: [public/private]

Compliance requirements:
- [SOC2/HIPAA/PCI-DSS/etc.]

Generate:
1. Security configuration changes
2. TLS setup steps
3. Network isolation recommendations
4. Audit logging configuration
5. Secrets management approach
6. Security monitoring rules
```

## Monitoring & Alerting Prompts

### Alert Rule Creation

```
Create alerting rules for ELK Stack monitoring:

Priority alerts needed:
1. [Alert type]: [threshold]
2. [Alert type]: [threshold]
3. [Alert type]: [threshold]

Notification channels:
- [Slack/Email/PagerDuty]

Generate:
1. Watcher/Alerting rule JSON
2. Condition logic
3. Action configuration
4. Throttling settings
5. Escalation rules
```

### Dashboard Design

```
Design Kibana dashboard for:

Purpose: [Operations/Security/Business]

Key metrics:
- [Metric 1]
- [Metric 2]
- [Metric 3]

Visualizations needed:
- [Type 1]: [data]
- [Type 2]: [data]
- [Type 3]: [data]

Filters:
- [Filter 1]
- [Filter 2]

Generate:
1. Dashboard layout description
2. Visualization configurations
3. Filter setup
4. Drill-down suggestions
5. Saved search definitions
```

## Integration Prompts

### Application Logging Setup

```
Configure structured logging for:

Application: [language/framework]
Current logging: [describe current approach]

Target fields:
- Standard: [@timestamp, level, message, service]
- Custom: [list custom fields]

Requirements:
- Correlation IDs: [trace_id, span_id]
- Sensitive data masking: [patterns]
- Performance impact: [minimal/acceptable]

Generate:
1. Logging library configuration
2. JSON format specification
3. Correlation ID implementation
4. Masking patterns
5. Filebeat input configuration
```

### CI/CD Integration

```
Integrate ELK Stack into CI/CD pipeline:

CI/CD tool: [GitHub Actions/GitLab CI/Jenkins]

Stages to add:
1. [Log configuration validation]
2. [Dashboard deployment]
3. [Alert rule deployment]
4. [Index template updates]

Generate:
1. Pipeline stage definitions
2. Validation scripts
3. Deployment scripts
4. Rollback procedures
5. Testing approach
```

---

*ELK Stack LLM Prompts | faion-cicd-engineer*
