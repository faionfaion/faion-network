# Data Pipeline Design

Designing data ingestion, processing, transformation, and storage systems for batch and real-time workloads.

## Overview

Data pipelines are the backbone of modern data-driven organizations, enabling the flow of data from diverse sources through transformation and into destinations for analytics, ML/AI, and operational use. The global data pipeline market is projected to grow from $12.3 billion (2025) to $43.6 billion by 2032.

## Pipeline Types

| Type | Latency | Use Case | Tools |
|------|---------|----------|-------|
| **Batch** | Minutes to hours | ETL, reporting, ML training, historical analysis | Spark, Airflow, dbt |
| **Streaming** | Milliseconds to seconds | Real-time analytics, fraud detection, monitoring | Kafka, Flink, Spark Streaming |
| **Lambda** | Both | Combine batch accuracy + stream speed | Kafka + Spark batch |
| **Kappa** | Streaming-first | Simplified streaming-only architecture | Kafka + Flink |

## ETL vs ELT

### ETL (Extract-Transform-Load)

Transform data before loading into the destination.

```
Source --> Staging --> Transform --> Warehouse
```

**When to Use:**
- Strict compliance requirements (HIPAA, GDPR)
- Data anonymization/encryption before storage
- Legacy systems with limited compute
- Smaller data volumes with complex transformations

### ELT (Extract-Load-Transform)

Load raw data first, transform in the warehouse using its compute power.

```
Source --> Warehouse (raw) --> Transform --> Warehouse (clean)
```

**When to Use:**
- Cloud-native environments (BigQuery, Snowflake, Databricks)
- Large data volumes requiring distributed compute
- Exploratory analytics and ML workflows
- Need to preserve raw data for future use cases

### Medallion Architecture (2025 Standard)

68% of cloud-first enterprises use this ELT pattern:

| Layer | Purpose | Data State |
|-------|---------|------------|
| **Bronze** | Raw ingestion | Unprocessed, as-is from source |
| **Silver** | Cleaned | Standardized, deduplicated |
| **Gold** | Business-ready | Aggregated, enriched, optimized |

## Modern Data Stack Components

| Category | Tools | Purpose |
|----------|-------|---------|
| **Ingestion** | Airbyte, Fivetran, Stitch | Extract data from sources |
| **Storage** | S3, GCS, Azure Blob | Data lake storage |
| **Warehouse** | Snowflake, BigQuery, Databricks | Analytical processing |
| **Transformation** | dbt, Spark, Dataform | Data modeling and transformation |
| **Orchestration** | Airflow, Dagster, Prefect | Workflow scheduling and monitoring |
| **Quality** | Great Expectations, Soda, dbt tests | Data validation and testing |
| **Observability** | Monte Carlo, Datadog, Metaplane | Pipeline monitoring and alerting |
| **Catalog** | Alation, Atlan, Collibra | Metadata, lineage, governance |

## Orchestration Tools Comparison

### Apache Airflow

**Best for:** Large-scale production pipelines, enterprise environments, extensive integrations.

- Industry standard since 2015 (80,000+ organizations)
- Airflow 3.0 (2025): DAG versioning, multi-language support, event-driven scheduling
- Massive ecosystem with 600+ operators
- 30% use for MLOps, 10% for GenAI

**Considerations:** Steep learning curve, higher operational overhead.

### Dagster

**Best for:** Asset-centric pipelines, data quality focus, modern developer experience.

- Asset-first approach with built-in lineage
- Excellent local development and testing
- Fast onboarding compared to Airflow
- Type hints and pytest integration

**Considerations:** Smaller ecosystem, learning curve for asset-based thinking.

### Prefect

**Best for:** Small to mid-sized teams, rapid prototyping, dynamic workflows.

- Minimal Python interface with decorators
- Robust error handling and retries
- Cloud-friendly with hybrid execution
- Excellent developer experience

**Considerations:** Limited data lineage, smaller ecosystem than Airflow.

### Quick Selection Guide

```
Enterprise + many integrations --> Airflow
Asset-centric + observability --> Dagster
Small team + flexibility      --> Prefect
```

## Key Technologies

### Apache Kafka

Distributed event streaming platform for real-time data pipelines.

**Key Benefits:**
- High throughput: Millions of messages/second
- Fault tolerance: Replication across brokers
- Exactly-once semantics: Guaranteed processing
- Decoupling: Source/target independence

**Use Cases:** Event streaming, log aggregation, change data capture (CDC).

### Apache Spark

Unified analytics engine for batch and streaming processing.

**Processing Modes:**
- **Micro-batch** (default): ~100ms latency, exactly-once
- **Continuous** (Spark 2.3+): ~1ms latency, at-least-once
- **Real-time mode** (2025): Single-digit ms latency

**Use Cases:** ETL, ML training, large-scale transformations.

### dbt (Data Build Tool)

SQL-first transformation layer with software engineering practices.

**Best Practices:**
- Follow `stg_<source>__<entity>s.sql` naming
- Use verbs for intermediate models: `int_orders_joined`
- Version control all transformations
- Modularize CTEs into separate models

**Materializations:**
| Type | Use Case |
|------|----------|
| View | Light transformations, always fresh |
| Table | Frequently accessed, performance-critical |
| Incremental | Large datasets, append-only updates |
| Ephemeral | Internal CTEs, not persisted |

### Data Quality Tools

| Tool | Approach | Best For |
|------|----------|----------|
| **Great Expectations** | Python-first, 300+ expectations | Complex validation, compliance |
| **Soda** | YAML-first (SodaCL), accessible | Continuous monitoring, alerts |
| **dbt tests** | SQL-first, integrated with dbt | Transformation-layer testing |

## Pipeline Patterns

### Fan-In (Aggregation)
```
Source A --+
Source B --+--> Aggregate --> Sink
Source C --+
```

### Fan-Out (Distribution)
```
              +--> Sink A
Source ---+--+--> Sink B
              +--> Sink C
```

### Enrichment
```
Main Stream -----------+--> Enriched Data
                       |
Reference Data --------+
```

### Change Data Capture (CDC)
```
Database --> Debezium --> Kafka --> Destination
```

## Error Handling

### Dead Letter Queue (DLQ)
```
Source --> Process --> Success --> Destination
               |
               +--> Failure --> DLQ --> Manual review
```

### Retry Strategies

| Strategy | Use Case |
|----------|----------|
| **Exponential backoff** | Transient failures (network, API limits) |
| **Fixed delay** | Known recovery time |
| **Circuit breaker** | Prevent cascade failures |

### Idempotency

Ensure same input produces same output (safe retries):

```python
def process(record):
    if already_processed(record.id):
        return  # Skip duplicate
    do_processing(record)
    mark_processed(record.id)
```

## Monitoring Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **Throughput** | Records/second | < expected baseline |
| **Latency** | Processing time | p99 > SLO target |
| **Error rate** | Failed records % | > 1% |
| **Queue depth** | Pending messages | Growing continuously |
| **Data freshness** | Time since last update | > SLA |
| **Consumer lag** | Kafka offset lag | Growing rapidly |

## 2025-2026 Trends

1. **AI-Powered Pipelines**: Intelligent agents for pipeline generation, anomaly detection, self-healing
2. **Lakehouse Architecture**: Unified batch + streaming on Delta Lake, Apache Iceberg
3. **Data Products**: Domain teams own data assets with quality, docs, access controls
4. **Decentralized Data Mesh**: Federated ownership with central governance
5. **Real-Time ML Features**: Sub-millisecond feature serving for online inference
6. **Semantic Layer**: Centralized metric definitions (dbt Semantic Layer, Cube)

## LLM Usage Tips

### When Designing Pipelines

1. **Provide context**: Volume, latency requirements, existing tech stack
2. **Specify constraints**: Budget, team skills, compliance requirements
3. **Ask for trade-offs**: Request pros/cons of different approaches
4. **Request diagrams**: Ask for ASCII/Mermaid architecture diagrams

### Effective Prompts

```
"Design a data pipeline for [use case] with [volume] daily records,
requiring [latency] latency. Consider [constraints]. What are the
trade-offs between different approaches?"
```

### Architecture Reviews

```
"Review this pipeline architecture for:
1. Scalability bottlenecks
2. Single points of failure
3. Data quality gaps
4. Cost optimization opportunities"
```

## External Links

### Official Documentation
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Great Expectations](https://greatexpectations.io/)
- [Dagster Documentation](https://docs.dagster.io/)
- [Prefect Documentation](https://docs.prefect.io/)

### Learning Resources
- [Confluent Developer: Data Pipelines with Kafka](https://developer.confluent.io/courses/data-pipelines/intro/)
- [dbt Learn](https://courses.getdbt.com/)
- [Databricks Academy](https://www.databricks.com/learn)

### Best Practices Guides
- [dbt Best Practices](https://docs.getdbt.com/best-practices)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Kafka Best Practices](https://www.instaclustr.com/education/apache-kafka/)

## Related Methodologies

- [event-driven-architecture/](../event-driven-architecture/) - Event patterns, Kafka, messaging
- [database-selection/](../database-selection/) - Storage options, CAP theorem
- [observability-architecture/](../observability-architecture/) - Monitoring, alerting, tracing
- [distributed-patterns/](../distributed-patterns/) - Saga, CQRS, Event Sourcing
