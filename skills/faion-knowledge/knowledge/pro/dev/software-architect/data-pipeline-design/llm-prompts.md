# LLM Prompts for Data Pipeline Design

Effective prompts for LLM-assisted data pipeline design, architecture review, and troubleshooting.

---

## Table of Contents

1. [Pipeline Architecture Design](#pipeline-architecture-design)
2. [Technology Selection](#technology-selection)
3. [ETL/ELT Pattern Design](#etlelt-pattern-design)
4. [Streaming Pipeline Design](#streaming-pipeline-design)
5. [Orchestration Design](#orchestration-design)
6. [Data Quality Implementation](#data-quality-implementation)
7. [Performance Optimization](#performance-optimization)
8. [Architecture Review](#architecture-review)
9. [Troubleshooting](#troubleshooting)
10. [Migration Planning](#migration-planning)

---

## Pipeline Architecture Design

### Initial Architecture Design

```
Design a data pipeline architecture for the following use case:

**Business Context:**
- Industry: [e-commerce/fintech/healthcare/SaaS/IoT]
- Primary use case: [analytics/ML/operational/compliance]
- Data consumers: [BI analysts/data scientists/applications/partners]

**Data Characteristics:**
- Volume: [X] records per day / [Y] GB daily
- Velocity: [batch daily/hourly/real-time streaming]
- Variety: [structured/semi-structured/unstructured]
- Sources: [databases/APIs/events/files/IoT sensors]

**Requirements:**
- Latency SLA: [hours/minutes/seconds/milliseconds]
- Availability: [99.9%/99.99%]
- Retention: [30 days/1 year/7 years]
- Compliance: [GDPR/HIPAA/SOC2/none]

**Constraints:**
- Budget: [startup/mid-market/enterprise]
- Team skills: [SQL only/Python/Spark/Kafka experience]
- Existing infrastructure: [AWS/GCP/Azure/on-prem/hybrid]

Please provide:
1. High-level architecture diagram (ASCII or Mermaid)
2. Technology stack recommendations with rationale
3. Data flow description
4. Key design decisions and trade-offs
5. Estimated complexity and implementation phases
```

### Batch vs Streaming Decision

```
I need to decide between batch and streaming for this data pipeline:

**Use Case:**
[Describe specific business use case]

**Current State:**
- Data sources: [list sources]
- Current processing: [batch/manual/none]
- Pain points: [list issues]

**Requirements:**
- End users need data freshness of: [hours/minutes/seconds]
- Peak data volume: [X records/events per second]
- Processing complexity: [simple aggregations/complex ML/joins across sources]
- Exact-once semantics: [required/nice-to-have/not needed]

**Questions:**
1. Should I use batch, streaming, or lambda architecture?
2. What are the trade-offs for each option?
3. If streaming, what processing guarantees do I need?
4. How does this choice affect cost and complexity?
5. What's the migration path if requirements change?
```

### End-to-End Pipeline Design

```
Design an end-to-end data pipeline with the following specifications:

**Sources:**
- PostgreSQL database (OLTP): Orders, Customers, Products
- REST API: Marketing campaigns (daily sync)
- Kafka: User clickstream events (real-time)
- S3: Historical CSV exports

**Destinations:**
- Snowflake data warehouse (analytics)
- Redis (real-time features for ML)
- Reverse ETL to Salesforce

**Processing Requirements:**
- Daily aggregations for BI dashboards
- Real-time user session enrichment
- ML feature engineering (batch + real-time)
- Data quality validation at each layer

**Please provide:**
1. Architecture diagram showing all components
2. Data flow for each source to destination
3. Technology choices for each component
4. Error handling strategy
5. Monitoring and observability approach
6. Cost estimation (compute + storage)
```

---

## Technology Selection

### Orchestration Tool Selection

```
Help me select a data orchestration tool for my team:

**Team Profile:**
- Size: [X] data engineers, [Y] analytics engineers
- Python experience: [beginner/intermediate/advanced]
- DevOps capabilities: [limited/moderate/strong]
- Current tools: [none/Cron/Luigi/custom scripts]

**Pipeline Characteristics:**
- Number of pipelines: [10/50/200+]
- Average DAG complexity: [simple linear/moderate/complex with branching]
- Execution environment: [local/Kubernetes/cloud managed]
- SLA requirements: [best effort/99%/99.9%]

**Key Requirements:**
- [ ] Asset-centric vs task-centric approach
- [ ] Strong testing capabilities
- [ ] Data lineage and observability
- [ ] Easy local development
- [ ] Managed cloud option available
- [ ] Integration with [dbt/Spark/specific tools]

Compare Apache Airflow, Dagster, and Prefect for this scenario:
1. Feature comparison matrix
2. Pros and cons for our specific needs
3. Migration effort if switching later
4. Total cost of ownership estimate
5. Your recommendation with rationale
```

### Data Warehouse Selection

```
Help me choose a cloud data warehouse:

**Workload Profile:**
- Query patterns: [BI dashboards/ad-hoc analytics/ML training/all]
- Concurrency: [X] concurrent queries peak
- Query complexity: [simple aggregations/complex joins/window functions]
- Data volume: [X] TB current, [Y] TB projected in 2 years

**Data Characteristics:**
- Update pattern: [append-only/occasional updates/frequent updates]
- Schema changes: [rare/monthly/frequent]
- Semi-structured data: [none/some JSON/heavy JSON/nested arrays]

**Integration Requirements:**
- BI tools: [Tableau/Looker/Power BI/Metabase]
- dbt compatibility: essential
- Reverse ETL: [Hightouch/Census/custom]
- ML workloads: [in-warehouse/external training]

**Constraints:**
- Cloud provider: [AWS only/GCP only/Azure only/multi-cloud]
- Budget: [cost-sensitive/moderate/cost-not-primary-concern]
- Team expertise: [SQL only/Python/both]

Compare Snowflake, BigQuery, Databricks, and Redshift:
1. Performance for our query patterns
2. Cost modeling for our volume
3. Ease of management
4. Ecosystem and integrations
5. Your recommendation
```

### Streaming Platform Selection

```
I need to select a streaming platform for real-time data processing:

**Requirements:**
- Throughput: [X] events per second
- Latency: p99 < [Y] milliseconds
- Ordering: [per-key/global/not required]
- Retention: [hours/days/indefinite replay]
- Processing: [simple routing/stateful/complex event processing]

**Existing Infrastructure:**
- Cloud: [AWS/GCP/Azure]
- Kubernetes: [yes/no]
- Team Kafka experience: [none/basic/advanced]

**Use Cases:**
1. [Use case 1]
2. [Use case 2]
3. [Use case 3]

Compare:
- Apache Kafka (self-managed)
- Confluent Cloud
- AWS Kinesis
- Google Pub/Sub
- Redpanda

For each option provide:
1. Fit for our use cases
2. Operational complexity
3. Cost estimate
4. Scaling characteristics
5. Ecosystem and tooling
```

---

## ETL/ELT Pattern Design

### ELT with Medallion Architecture

```
Design a medallion architecture (Bronze/Silver/Gold) for this use case:

**Data Sources:**
- Source 1: [description, volume, frequency]
- Source 2: [description, volume, frequency]
- Source 3: [description, volume, frequency]

**Business Requirements:**
- Analytics: [specific dashboard/report requirements]
- ML: [feature engineering needs]
- Operational: [reverse ETL destinations]

**For each layer, please define:**

**Bronze Layer:**
- Ingestion approach (full/incremental/CDC)
- Schema handling (inferred/enforced)
- Partitioning strategy
- Retention policy
- Error handling

**Silver Layer:**
- Cleaning transformations
- Standardization rules
- Deduplication logic
- Data quality checks
- Grain of tables

**Gold Layer:**
- Business entities and facts
- Aggregation levels
- Metric definitions
- Access patterns optimization
- Refresh frequency

Also provide:
- dbt project structure
- Data quality framework
- Lineage documentation approach
```

### dbt Project Design

```
Help me design a dbt project structure for this analytics stack:

**Data Sources:**
- Stripe (payments, subscriptions, customers)
- Salesforce (accounts, opportunities, contacts)
- Product database (users, events, features)
- Marketing (campaigns, ad spend)

**Business Domains:**
- Finance: MRR, churn, LTV calculations
- Sales: pipeline, conversion metrics
- Product: DAU, retention, feature adoption
- Marketing: CAC, attribution, ROI

**Team Structure:**
- Central data team: 3 analytics engineers
- Domain analysts: 2 per business area
- Data consumers: 50+ stakeholders

Design the following:
1. Project folder structure
2. Naming conventions
3. Materialization strategy by model type
4. Testing strategy
5. Documentation approach
6. CI/CD pipeline
7. How to handle cross-domain models
```

### ETL for Compliance

```
Design an ETL pipeline with compliance requirements:

**Compliance Framework:**
- Regulations: [GDPR/HIPAA/SOC2/PCI-DSS]
- Data residency: [specific regions required]
- Retention limits: [X years, then delete]
- Right to deletion: [must support]

**Sensitive Data Types:**
- PII fields: [name, email, address, etc.]
- PHI fields: [if applicable]
- Financial data: [if applicable]

**Requirements:**
1. Data must be encrypted at rest and in transit
2. Access must be logged and auditable
3. Masking for non-production environments
4. Lineage for compliance reporting
5. Automated PII detection

Design the pipeline including:
1. Encryption strategy
2. Tokenization/masking approach
3. Access control model
4. Audit logging implementation
5. Data retention automation
6. Right-to-deletion implementation
7. Tools and technologies
```

---

## Streaming Pipeline Design

### Real-Time Analytics Pipeline

```
Design a real-time analytics pipeline:

**Use Case:**
[Describe real-time analytics requirement]

**Input:**
- Event sources: [list]
- Event schema: [provide schema or describe]
- Volume: [events/second]
- Ordering requirements: [per-key/global/none]

**Processing:**
- Aggregation windows: [tumbling/sliding/session]
- Window sizes: [1 min/5 min/1 hour]
- Stateful operations: [joins/dedup/sessionization]
- Late data handling: [drop/reprocess/watermark]

**Output:**
- Sink: [dashboard/API/warehouse/cache]
- Latency target: [end-to-end]
- Exactly-once required: [yes/no]

Provide:
1. Architecture diagram
2. Technology selection (Kafka, Flink, etc.)
3. Processing topology
4. State management approach
5. Fault tolerance design
6. Monitoring strategy
7. Sample code or pseudocode
```

### Kafka Pipeline Design

```
Design a Kafka-based data pipeline:

**Event Types:**
1. [Event 1]: [schema, volume, importance]
2. [Event 2]: [schema, volume, importance]
3. [Event 3]: [schema, volume, importance]

**Requirements:**
- Guaranteed delivery
- Ordered processing per [key]
- Consumer groups: [list consumers]
- Replay capability for [duration]

**Questions to answer:**
1. Topic design (one topic vs multiple, naming)
2. Partition strategy (key selection, partition count)
3. Schema management (Avro/JSON/Protobuf, registry)
4. Producer configuration (acks, idempotence, batching)
5. Consumer configuration (group management, offset handling)
6. Error handling (DLQ, retry topics)
7. Monitoring (metrics, alerts)

Also provide:
- Topic configuration YAML
- Producer code template
- Consumer code template
- Kafka Connect configuration if applicable
```

### CDC Pipeline Design

```
Design a Change Data Capture (CDC) pipeline:

**Source Database:**
- Type: [PostgreSQL/MySQL/MongoDB/Oracle]
- Tables to capture: [list tables]
- Estimated change volume: [changes/second]
- Capture requirements: [inserts only/updates/deletes/schema changes]

**Processing Requirements:**
- Transform on capture: [minimal/full transformation]
- Multiple destinations: [list destinations]
- Ordering guarantees: [per-table/per-key/global]

**Destination(s):**
- Primary: [data warehouse/data lake]
- Secondary: [cache/search index/replica]

Design including:
1. CDC tool selection (Debezium, Fivetran, etc.)
2. Kafka topic structure
3. Schema handling strategy
4. Initial snapshot approach
5. Handling deletes (soft delete, tombstone)
6. Recovery and replay procedures
7. Monitoring and alerting
```

---

## Orchestration Design

### Airflow DAG Design

```
Design Airflow DAGs for this data pipeline:

**Pipeline Overview:**
[Describe the overall data flow]

**Tasks:**
1. [Task 1]: [type, dependencies, duration, retry policy]
2. [Task 2]: [type, dependencies, duration, retry policy]
...

**Requirements:**
- Schedule: [cron expression]
- SLA: [max duration before alert]
- Retries: [number, backoff strategy]
- Dependencies: [external systems, sensors]
- Parallelism: [max concurrent tasks]

**Special Considerations:**
- Backfill capability needed: [yes/no]
- Dynamic task generation: [yes/no]
- Cross-DAG dependencies: [list]
- Data intervals: [aware/unaware]

Provide:
1. DAG structure diagram
2. Complete DAG Python code
3. Operator selection for each task
4. XCom usage if needed
5. Error handling and alerting
6. Testing approach
7. Deployment and CI/CD
```

### Dagster Asset Graph

```
Design a Dagster asset graph for this data platform:

**Data Assets:**
1. [Asset 1]: [description, source, materialization]
2. [Asset 2]: [description, dependencies, materialization]
...

**Requirements:**
- Partitioning: [daily/hourly/custom]
- Freshness policies: [by asset]
- Auto-materialization: [rules]
- Software-defined assets focus

**Infrastructure:**
- Execution: [local/K8s/hybrid]
- Scheduling: [time-based/asset-based/sensor]
- Observability integration: [tools]

Provide:
1. Asset dependency graph
2. Asset definitions with decorators
3. Resources and I/O managers
4. Schedules and sensors
5. Jobs for grouped execution
6. Repository organization
7. Testing strategy
```

---

## Data Quality Implementation

### Quality Framework Design

```
Design a data quality framework for this data platform:

**Data Platform:**
- Layers: [ingestion/staging/mart]
- Key tables: [list critical tables]
- Data volumes: [by table]
- Update frequency: [by table]

**Quality Dimensions to Cover:**
1. Completeness: [null rate thresholds]
2. Accuracy: [validation rules]
3. Consistency: [cross-table checks]
4. Timeliness: [freshness SLAs]
5. Uniqueness: [deduplication rules]
6. Validity: [format/range checks]

**Requirements:**
- Block bad data: [which pipelines]
- Alert and continue: [which pipelines]
- Quality scoring: [weighted dimensions]
- Trend monitoring: [anomaly detection]

Design including:
1. Tool selection (GX, Soda, dbt tests, custom)
2. Check placement in pipeline
3. Severity levels and actions
4. Alerting and escalation
5. Quality dashboards
6. Data contract templates
7. Implementation roadmap
```

### Great Expectations Suite

```
Create a Great Expectations suite for this table:

**Table:** [table_name]
**Schema:**
| Column | Type | Description | Business Rules |
|--------|------|-------------|----------------|
| [col1] | [type] | [desc] | [rules] |
...

**Critical Quality Checks:**
1. [Check 1]: [expectation type, parameters]
2. [Check 2]: [expectation type, parameters]
...

**Thresholds:**
- Row count: min [X], max [Y]
- Null tolerance: [by column]
- Anomaly detection: [enabled/disabled]

Provide:
1. Complete expectation suite Python code
2. Validation action configuration
3. Data docs setup
4. Integration with orchestrator
5. Alerting configuration
```

---

## Performance Optimization

### Pipeline Performance Tuning

```
Help me optimize this slow data pipeline:

**Current State:**
- Pipeline duration: [X hours/minutes]
- Target duration: [Y]
- Bottleneck stage: [if known]
- Data volume: [rows/GB]

**Infrastructure:**
- Compute: [Spark cluster/single node/serverless]
- Storage: [S3/warehouse/local]
- Network: [within region/cross-region]

**Pipeline Details:**
- Processing type: [Spark/Python/SQL]
- Transformations: [describe heavy operations]
- I/O patterns: [reads/writes/shuffles]

**Current Configuration:**
[Paste relevant configs]

**Code/Query:**
[Paste relevant code or query]

Analyze and provide:
1. Identified bottlenecks
2. Quick wins (config changes)
3. Code optimizations
4. Infrastructure recommendations
5. Partitioning/bucketing strategies
6. Caching opportunities
7. Parallelization improvements
8. Cost vs performance trade-offs
```

### Spark Job Optimization

```
Optimize this Spark job:

**Job Details:**
- Input size: [X GB]
- Output size: [Y GB]
- Current duration: [Z minutes]
- Shuffle size: [if known]
- Memory issues: [OOM/spill to disk/none]

**Cluster Configuration:**
- Executors: [count] x [memory] x [cores]
- Driver: [memory]
- Dynamic allocation: [enabled/disabled]

**Job Code:**
```python
[Paste Spark code]
```

**Execution Plan:**
[Paste explain plan if available]

Provide:
1. Code optimizations (joins, aggregations, UDFs)
2. Configuration tuning
3. Partition strategy improvements
4. Memory management
5. Serialization improvements
6. Caching strategy
7. Broadcast join opportunities
8. Estimated improvement
```

---

## Architecture Review

### Pipeline Architecture Review

```
Review this data pipeline architecture:

**Architecture Diagram:**
[Paste ASCII diagram or describe]

**Components:**
1. [Component 1]: [technology, purpose, configuration]
2. [Component 2]: [technology, purpose, configuration]
...

**Data Flow:**
[Describe data flow]

**Current Issues (if any):**
- [Issue 1]
- [Issue 2]

**Review Criteria:**
1. Scalability: Can it handle 10x growth?
2. Reliability: Single points of failure?
3. Performance: Bottlenecks?
4. Cost: Over/under-provisioned?
5. Security: Data protection?
6. Maintainability: Operational complexity?
7. Data quality: Validation coverage?

Provide:
1. Strengths of current architecture
2. Identified issues and risks
3. Recommendations (prioritized)
4. Migration path for improvements
5. Quick wins vs long-term changes
```

### Production Readiness Review

```
Review this pipeline for production readiness:

**Pipeline Details:**
[Describe pipeline]

**Current State:**
- Development status: [dev/staging/partial prod]
- Testing coverage: [describe]
- Documentation: [describe]
- Monitoring: [describe]

**Checklist Review:**

**Reliability:**
- [ ] Retry logic implemented
- [ ] Dead letter queues configured
- [ ] Idempotency ensured
- [ ] Circuit breakers in place
- [ ] Graceful degradation planned

**Observability:**
- [ ] Logging structured and centralized
- [ ] Metrics exported
- [ ] Dashboards created
- [ ] Alerts configured
- [ ] Runbooks written

**Data Quality:**
- [ ] Schema validation
- [ ] Data quality checks
- [ ] Freshness monitoring
- [ ] Anomaly detection

**Security:**
- [ ] Secrets managed securely
- [ ] Access controls implemented
- [ ] Encryption configured
- [ ] Audit logging enabled

**Operations:**
- [ ] Deployment automated
- [ ] Rollback procedures documented
- [ ] Backup/recovery tested
- [ ] Scaling policies defined

Review and identify gaps for each category.
```

---

## Troubleshooting

### Pipeline Failure Diagnosis

```
Help me troubleshoot this pipeline failure:

**Symptoms:**
- Error message: [paste error]
- Failure point: [task/stage]
- Failure frequency: [first time/intermittent/consistent]
- Last successful run: [date/time]

**Recent Changes:**
- [List any recent changes]

**Environment:**
- Platform: [Airflow/Dagster/Spark/etc.]
- Infrastructure: [cloud/on-prem]
- Data volume at failure: [if relevant]

**Logs:**
```
[Paste relevant log excerpts]
```

**What I've Tried:**
1. [Attempt 1]
2. [Attempt 2]

Please:
1. Analyze the error and logs
2. Identify likely root causes
3. Provide debugging steps
4. Suggest fixes (most likely to least)
5. Recommend prevention measures
```

### Data Quality Issue Investigation

```
Investigate this data quality issue:

**Issue:**
[Describe the data quality problem]

**Impact:**
- Affected tables: [list]
- Affected records: [count/percentage]
- Business impact: [describe]
- Duration: [when first noticed]

**Symptoms:**
- Missing data: [fields/records]
- Incorrect values: [describe]
- Duplicates: [if applicable]
- Schema issues: [if applicable]

**Pipeline Context:**
- Last successful refresh: [date]
- Recent pipeline changes: [list]
- Source system changes: [if known]

**Initial Findings:**
[Any investigation done so far]

Help me:
1. Identify root cause
2. Determine scope of impact
3. Create remediation plan
4. Implement data fix
5. Prevent recurrence
```

### Kafka Consumer Lag

```
Help troubleshoot Kafka consumer lag:

**Symptoms:**
- Consumer group: [name]
- Lag: [messages behind]
- Topics affected: [list]
- Started: [when]

**Consumer Details:**
- Technology: [Kafka Streams/Flink/Python/etc.]
- Instances: [count]
- Processing type: [simple/stateful]
- Average processing time: [per message]

**Configuration:**
```
[Paste consumer configuration]
```

**Metrics:**
- Input rate: [messages/second]
- Processing rate: [messages/second]
- Rebalances: [frequency]
- Errors: [if any]

**Infrastructure:**
- Consumer resources: [CPU/memory]
- Kafka cluster: [brokers/partitions]

Diagnose and provide:
1. Root cause analysis
2. Immediate mitigation
3. Configuration changes
4. Scaling recommendations
5. Monitoring improvements
```

---

## Migration Planning

### On-Prem to Cloud Migration

```
Plan a data pipeline migration to cloud:

**Current State:**
- Infrastructure: [describe on-prem setup]
- Pipelines: [count, technologies]
- Data volume: [current and growth]
- Team skills: [describe]

**Target State:**
- Cloud provider: [AWS/GCP/Azure]
- Managed services preference: [high/medium/low]
- Lift-and-shift vs rearchitect: [preference]

**Constraints:**
- Timeline: [months]
- Budget: [range]
- Downtime tolerance: [none/minimal/flexible]
- Compliance: [requirements]

**Key Workloads:**
1. [Workload 1]: [criticality, complexity]
2. [Workload 2]: [criticality, complexity]
...

Create:
1. Migration phases
2. Workload prioritization
3. Technology mapping (current to cloud)
4. Cutover strategy
5. Rollback plan
6. Risk assessment
7. Success criteria
8. Timeline estimate
```

### Legacy ETL Modernization

```
Plan modernization of legacy ETL:

**Current State:**
- ETL tool: [Informatica/DataStage/SSIS/custom scripts]
- Pipelines: [count]
- Lines of code: [estimate]
- Documentation: [good/poor/none]
- Knowledge holders: [how many people]

**Pain Points:**
1. [Pain point 1]
2. [Pain point 2]
...

**Target Stack:**
- [Proposed modern stack]

**Goals:**
- Reduce maintenance effort
- Improve observability
- Enable self-service
- Improve performance
- Reduce costs

Create:
1. Assessment framework for pipelines
2. Prioritization criteria
3. Migration patterns (convert/rewrite/retire)
4. POC recommendation
5. Phased migration plan
6. Training requirements
7. Risk mitigation
8. Success metrics
```

---

## Prompt Engineering Tips

### Effective Prompting

1. **Provide context**: Include business requirements, constraints, and existing infrastructure
2. **Be specific about scale**: Volume, latency, and growth projections matter
3. **State constraints clearly**: Budget, team skills, compliance requirements
4. **Ask for trade-offs**: Understanding alternatives helps decision-making
5. **Request diagrams**: Visual representations clarify complex architectures
6. **Include code/config**: Paste actual code for optimization/troubleshooting
7. **Specify output format**: Ask for checklists, tables, or step-by-step guides

### Follow-up Prompts

```
# Deep dive on recommendation
"Explain more about [specific recommendation]. What are the implementation details?"

# Alternative exploration
"What if we chose [alternative] instead? What would change?"

# Cost analysis
"Provide a cost breakdown for this architecture at [scale]."

# Phased implementation
"Break this into phases. What's the MVP vs full implementation?"

# Risk assessment
"What are the risks of this approach? How do we mitigate them?"

# Comparison request
"Compare this with [alternative approach] in terms of [criteria]."
```
