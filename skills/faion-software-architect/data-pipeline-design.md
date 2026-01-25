# Data Pipeline Design

Designing data ingestion, processing, and storage systems.

## Pipeline Types

| Type | Latency | Use Case |
|------|---------|----------|
| Batch | Hours | ETL, reporting, ML training |
| Streaming | Seconds | Real-time analytics, monitoring |
| Lambda | Both | Combine batch accuracy + stream speed |

## Batch Processing

```
Source ─▶ Extract ─▶ Transform ─▶ Load ─▶ Destination
          (E)        (T)          (L)

Daily schedule:
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Raw Data │───▶│ Process  │───▶│ Data     │
│ (S3)     │    │ (Spark)  │    │ Warehouse│
└──────────┘    └──────────┘    └──────────┘
```

**Tools:**
- Apache Spark
- Apache Airflow (orchestration)
- dbt (transformations)
- AWS Glue, Dataflow

## Stream Processing

```
Events ─▶ Queue ─▶ Process ─▶ Sink
          │        (real-time)
          ▼
       Replay
       (if needed)
```

**Tools:**
- Apache Kafka (streaming platform)
- Apache Flink, Spark Streaming
- AWS Kinesis
- Kafka Streams

## ETL vs ELT

### ETL (Extract-Transform-Load)
Transform before loading.

```
Source ─▶ Staging ─▶ Transform ─▶ Warehouse
```

**Use when:** Complex transformations, legacy systems

### ELT (Extract-Load-Transform)
Load raw, transform in warehouse.

```
Source ─▶ Warehouse (raw) ─▶ Transform ─▶ Warehouse (clean)
```

**Use when:** Cloud warehouse (BigQuery, Snowflake), flexible transformations

## Data Pipeline Patterns

### Fan-In (Aggregation)
```
Source A ──┐
Source B ──┼──▶ Aggregate ─▶ Sink
Source C ──┘
```

### Fan-Out (Distribution)
```
              ┌──▶ Sink A
Source ──▶ ──┼──▶ Sink B
              └──▶ Sink C
```

### Enrichment
```
Main Stream ─────────────────┬──▶ Enriched Data
                             │
Reference Data ──────────────┘
```

## Data Quality

### Validation Checks

```python
# Schema validation
assert df.schema == expected_schema

# Null checks
assert df.filter(col("id").isNull()).count() == 0

# Range checks
assert df.filter(col("age") < 0).count() == 0

# Uniqueness
assert df.count() == df.select("id").distinct().count()

# Referential integrity
orphans = orders.join(customers, "customer_id", "left_anti")
assert orphans.count() == 0
```

### Data Contracts

Define expected schema and quality rules:

```yaml
# data_contract.yaml
name: orders
version: 1.0
schema:
  - name: order_id
    type: string
    required: true
    unique: true
  - name: amount
    type: decimal
    required: true
    min: 0
quality:
  - freshness: 1 hour
  - completeness: 99%
```

## Pipeline Orchestration

### DAG (Directed Acyclic Graph)

```
        ┌──▶ Transform A ──┐
Extract ┤                  ├──▶ Load
        └──▶ Transform B ──┘

Dependencies ensure correct order.
```

### Airflow Example

```python
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('etl_pipeline', schedule_interval='@daily') as dag:
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data
    )
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data
    )
    load = PythonOperator(
        task_id='load',
        python_callable=load_data
    )

    extract >> transform >> load
```

## Error Handling

### Dead Letter Queue (DLQ)
```
Source ─▶ Process ─▶ Success ─▶ Destination
              │
              └─▶ Failure ─▶ DLQ ─▶ Manual review
```

### Retry Strategy
```python
@retry(
    max_attempts=3,
    backoff=exponential(base=2),
    exceptions=[TransientError]
)
def process_record(record):
    ...
```

### Idempotency
Same input produces same output, safe to retry.

```python
def process(record):
    if already_processed(record.id):
        return  # Skip duplicate

    do_processing(record)
    mark_processed(record.id)
```

## Monitoring

**Key Metrics:**
- Throughput (records/second)
- Latency (processing time)
- Error rate
- Queue depth
- Data freshness

```python
# Prometheus metrics
records_processed = Counter('records_processed_total')
processing_latency = Histogram('processing_latency_seconds')
queue_depth = Gauge('queue_depth')
```

## Architecture Example

```
┌─────────────────────────────────────────────────────┐
│                    Data Platform                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Sources          Ingestion        Processing       │
│  ┌─────┐         ┌─────────┐      ┌─────────┐      │
│  │ App │────────▶│  Kafka  │─────▶│  Flink  │      │
│  │ DB  │         │         │      │ (stream)│      │
│  │ API │         │         │      └────┬────┘      │
│  └─────┘         └────┬────┘           │           │
│                       │                │           │
│                       ▼                ▼           │
│                  ┌─────────┐      ┌─────────┐      │
│                  │   S3    │─────▶│  Spark  │      │
│                  │ (raw)   │      │ (batch) │      │
│                  └─────────┘      └────┬────┘      │
│                                        │           │
│  Storage                               ▼           │
│  ┌───────────────────────────────────────────┐    │
│  │              Data Warehouse               │    │
│  │             (Snowflake/BQ)                │    │
│  └───────────────────────────────────────────┘    │
│                       │                           │
│  Consumption          ▼                           │
│  ┌─────┐         ┌─────────┐                     │
│  │ BI  │◀────────│   dbt   │                     │
│  │ ML  │         │ (models)│                     │
│  └─────┘         └─────────┘                     │
└─────────────────────────────────────────────────────┘
```

## Related

- [event-driven-architecture.md](event-driven-architecture.md) - Event patterns
- [database-selection.md](database-selection.md) - Storage options
