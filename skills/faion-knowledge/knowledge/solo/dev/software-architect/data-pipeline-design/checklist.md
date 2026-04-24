# Data Pipeline Design Checklist

Step-by-step checklist for designing production-grade data pipelines.

---

## Phase 1: Requirements Analysis

### Business Requirements

- [ ] Define primary use case (analytics, ML, operational, compliance)
- [ ] Identify key stakeholders and consumers
- [ ] Document data freshness requirements (SLA)
- [ ] Specify data retention policies
- [ ] Clarify compliance requirements (GDPR, HIPAA, SOC2)
- [ ] Determine budget constraints
- [ ] Assess team skills and capacity

### Data Requirements

- [ ] Inventory all data sources
- [ ] Document source schemas and formats
- [ ] Estimate data volume (current and projected)
- [ ] Identify data velocity (records/second, events/day)
- [ ] Map data variety (structured, semi-structured, unstructured)
- [ ] Define critical data elements
- [ ] Identify sensitive/PII fields

### Performance Requirements

- [ ] Define latency requirements (real-time, near-real-time, batch)
- [ ] Specify throughput targets (records/second)
- [ ] Set availability SLA (99.9%, 99.99%)
- [ ] Define recovery time objective (RTO)
- [ ] Define recovery point objective (RPO)
- [ ] Establish query performance targets

---

## Phase 2: Architecture Selection

### Pipeline Type Selection

- [ ] **Batch Pipeline**
  - [ ] Latency tolerance: hours acceptable
  - [ ] Use cases: reporting, ML training, historical analysis
  - [ ] Tools: Spark, Airflow, dbt

- [ ] **Streaming Pipeline**
  - [ ] Latency requirement: seconds/milliseconds
  - [ ] Use cases: real-time analytics, monitoring, fraud detection
  - [ ] Tools: Kafka, Flink, Spark Streaming

- [ ] **Lambda Architecture**
  - [ ] Need both real-time and batch processing
  - [ ] Batch layer for accuracy, speed layer for freshness
  - [ ] Higher complexity acceptable

- [ ] **Kappa Architecture**
  - [ ] Streaming-first approach
  - [ ] Simplified operational model
  - [ ] Can replay events for reprocessing

### ETL vs ELT Decision

- [ ] **Choose ETL when:**
  - [ ] Strict compliance requires pre-load transformation
  - [ ] Complex transformations before storage
  - [ ] Legacy target systems with limited compute
  - [ ] Data anonymization/encryption required before storage

- [ ] **Choose ELT when:**
  - [ ] Cloud warehouse with scalable compute (Snowflake, BigQuery)
  - [ ] Large data volumes
  - [ ] Need raw data preservation
  - [ ] Flexible, iterative transformation requirements

- [ ] **Choose Hybrid when:**
  - [ ] Light cleansing at ingestion (dedup, type enforcement)
  - [ ] Full transformation in warehouse
  - [ ] Best of both approaches

### Storage Layer Selection

- [ ] Select data lake storage (S3, GCS, ADLS)
- [ ] Select data warehouse (Snowflake, BigQuery, Databricks, Redshift)
- [ ] Define table formats (Delta Lake, Apache Iceberg, Apache Hudi)
- [ ] Plan medallion architecture (Bronze/Silver/Gold)
- [ ] Design partitioning strategy
- [ ] Plan data lifecycle management

---

## Phase 3: Orchestration Design

### Tool Selection

- [ ] **Apache Airflow**
  - [ ] Large-scale production environment
  - [ ] Many existing integrations needed
  - [ ] Enterprise with dedicated platform team
  - [ ] Complex time-based scheduling

- [ ] **Dagster**
  - [ ] Asset-centric approach preferred
  - [ ] Strong testing requirements
  - [ ] Modern developer experience priority
  - [ ] Data lineage critical

- [ ] **Prefect**
  - [ ] Small to mid-sized team
  - [ ] Rapid development cycle
  - [ ] Dynamic, event-driven workflows
  - [ ] Minimal infrastructure overhead

### DAG Design

- [ ] Define task dependencies (DAG structure)
- [ ] Identify parallelization opportunities
- [ ] Plan task granularity (not too fine, not too coarse)
- [ ] Define scheduling frequency
- [ ] Plan backfill strategy
- [ ] Design idempotent tasks
- [ ] Implement task timeouts

### Error Handling

- [ ] Configure retry policies
  - [ ] Number of retries (typically 3)
  - [ ] Backoff strategy (exponential recommended)
  - [ ] Retry-able vs non-retry-able errors
- [ ] Implement Dead Letter Queues (DLQ)
- [ ] Design alerting thresholds
- [ ] Plan manual intervention procedures
- [ ] Document runbooks for common failures

---

## Phase 4: Data Ingestion

### Source Connectivity

- [ ] Inventory source connection types (API, DB, files, streams)
- [ ] Configure authentication and secrets management
- [ ] Implement connection pooling where applicable
- [ ] Plan rate limiting and throttling
- [ ] Set up CDC for database sources (Debezium, Fivetran)

### Ingestion Patterns

- [ ] **Full Load**
  - [ ] Initial data load
  - [ ] Small dimension tables
  - [ ] Data without reliable change tracking

- [ ] **Incremental Load**
  - [ ] Large fact tables
  - [ ] Event/transaction data
  - [ ] Define watermark/bookmark strategy

- [ ] **CDC (Change Data Capture)**
  - [ ] Near-real-time replication
  - [ ] Capture deletes and updates
  - [ ] Configure Debezium/Fivetran

- [ ] **Event Streaming**
  - [ ] Real-time event ingestion
  - [ ] Configure Kafka producers
  - [ ] Define topic partitioning strategy

### Schema Management

- [ ] Implement schema registry (Confluent Schema Registry)
- [ ] Define schema evolution strategy
- [ ] Handle schema drift gracefully
- [ ] Document breaking vs non-breaking changes
- [ ] Plan schema version compatibility

---

## Phase 5: Data Transformation

### dbt Project Setup

- [ ] Initialize dbt project structure
- [ ] Configure data warehouse connection
- [ ] Set up environment profiles (dev, staging, prod)
- [ ] Implement CI/CD for dbt

### Model Organization

- [ ] **Staging Models** (`stg_`)
  - [ ] One model per source table
  - [ ] Naming: `stg_<source>__<entity>.sql`
  - [ ] Light transformation only (rename, cast, dedupe)
  - [ ] Materialize as views or ephemeral

- [ ] **Intermediate Models** (`int_`)
  - [ ] Business logic groupings (billing, growth, etc.)
  - [ ] Use verbs: `int_orders_joined`, `int_users_aggregated`
  - [ ] Materialize as views or ephemeral

- [ ] **Mart Models** (`fct_`, `dim_`)
  - [ ] Fact tables: `fct_orders`, `fct_transactions`
  - [ ] Dimension tables: `dim_customers`, `dim_products`
  - [ ] Materialize as tables
  - [ ] Document business definitions

### Transformation Best Practices

- [ ] Define sources in `sources.yml`
- [ ] Never reference raw tables directly
- [ ] Modularize complex CTEs into separate models
- [ ] Use Jinja for DRY transformations
- [ ] Implement incremental models for large datasets
- [ ] Add model documentation and descriptions
- [ ] Test transformations that change grain

---

## Phase 6: Data Quality

### Validation Strategy

- [ ] **Schema Validation**
  - [ ] Column presence and types
  - [ ] Required fields not null
  - [ ] Enum/categorical value validation

- [ ] **Data Integrity**
  - [ ] Primary key uniqueness
  - [ ] Foreign key referential integrity
  - [ ] No orphan records

- [ ] **Business Rules**
  - [ ] Range checks (age >= 0, amount > 0)
  - [ ] Cross-field validation
  - [ ] Historical consistency

- [ ] **Freshness Checks**
  - [ ] Data age within SLA
  - [ ] Expected record counts
  - [ ] Anomaly detection

### Tool Implementation

- [ ] **dbt Tests** (transformation layer)
  - [ ] `unique` and `not_null` on keys
  - [ ] `accepted_values` for enums
  - [ ] `relationships` for foreign keys
  - [ ] Custom tests for business rules

- [ ] **Great Expectations** (ingestion/critical assets)
  - [ ] Define expectation suites
  - [ ] Configure data docs generation
  - [ ] Integrate with orchestrator

- [ ] **Soda** (continuous monitoring)
  - [ ] Define SodaCL checks
  - [ ] Configure anomaly detection
  - [ ] Set up alerting

### Data Contracts

- [ ] Define schema contracts between producers/consumers
- [ ] Version contracts semantically
- [ ] Automate contract validation in CI/CD
- [ ] Document SLAs for data quality metrics
- [ ] Establish data ownership

---

## Phase 7: Observability

### Monitoring Setup

- [ ] **Pipeline Metrics**
  - [ ] Task success/failure rates
  - [ ] Execution duration trends
  - [ ] Queue depths (Kafka lag)
  - [ ] Resource utilization

- [ ] **Data Metrics**
  - [ ] Record counts per batch
  - [ ] Data freshness
  - [ ] Quality score trends
  - [ ] Anomaly alerts

- [ ] **Infrastructure Metrics**
  - [ ] Cluster health
  - [ ] Storage capacity
  - [ ] Network throughput

### Alerting Configuration

- [ ] Define severity levels (P1-P4)
- [ ] Configure alerting channels (Slack, PagerDuty, email)
- [ ] Set up on-call rotation
- [ ] Create runbooks for each alert type
- [ ] Implement alert deduplication

### Logging and Tracing

- [ ] Implement structured logging
- [ ] Configure log aggregation (ELK, Loki)
- [ ] Set up distributed tracing (OpenTelemetry)
- [ ] Create dashboards (Grafana)
- [ ] Document troubleshooting procedures

---

## Phase 8: Security and Governance

### Access Control

- [ ] Implement role-based access control (RBAC)
- [ ] Configure service accounts with minimal permissions
- [ ] Set up secret management (Vault, AWS Secrets Manager)
- [ ] Enable audit logging
- [ ] Review access quarterly

### Data Protection

- [ ] Encrypt data at rest
- [ ] Encrypt data in transit (TLS)
- [ ] Implement column-level masking for PII
- [ ] Configure row-level security where needed
- [ ] Document data classification

### Governance

- [ ] Establish data ownership per domain
- [ ] Implement data catalog (Alation, Atlan)
- [ ] Enable automated lineage tracking
- [ ] Create data glossary
- [ ] Document data retention policies
- [ ] Configure compliance automation

---

## Phase 9: Deployment

### CI/CD Pipeline

- [ ] Set up version control (Git)
- [ ] Configure branch protection
- [ ] Implement pull request reviews
- [ ] Create staging environment
- [ ] Automate testing in CI
- [ ] Configure deployment automation

### Environment Strategy

- [ ] **Development**
  - [ ] Sample/subset data
  - [ ] Fast iteration
  - [ ] Individual developer environments

- [ ] **Staging**
  - [ ] Production-like data (anonymized)
  - [ ] Full pipeline testing
  - [ ] Performance validation

- [ ] **Production**
  - [ ] Blue-green or canary deployment
  - [ ] Rollback procedures documented
  - [ ] Change management process

### Documentation

- [ ] Architecture diagrams (C4 model)
- [ ] Runbooks for operations
- [ ] Data dictionary
- [ ] API documentation
- [ ] Onboarding guide for new team members

---

## Phase 10: Operations

### Day-2 Operations

- [ ] Establish daily health checks
- [ ] Monitor cost and optimize
- [ ] Review and tune performance
- [ ] Conduct incident post-mortems
- [ ] Maintain runbooks

### Disaster Recovery

- [ ] Document backup procedures
- [ ] Test restore procedures quarterly
- [ ] Define failover process
- [ ] Maintain DR runbook
- [ ] Conduct DR drills

### Continuous Improvement

- [ ] Collect pipeline performance metrics
- [ ] Review and reduce technical debt
- [ ] Gather user feedback
- [ ] Stay updated on tooling improvements
- [ ] Regular architecture reviews

---

## Quick Reference: Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| No idempotency | Design tasks to be rerunnable safely |
| Too many small topics | Consolidate related streams, use prefixes |
| Schema drift breaks pipelines | Use schema registry, handle evolution |
| No data quality checks | Implement validation at each layer |
| Missing monitoring | Add observability from day one |
| Hardcoded credentials | Use secret management systems |
| No backfill strategy | Design for historical reprocessing |
| Over-engineering | Start simple, evolve based on needs |
