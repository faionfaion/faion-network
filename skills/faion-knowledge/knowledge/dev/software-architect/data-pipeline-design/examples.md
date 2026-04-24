# Data Pipeline Examples

Real-world data pipeline architectures for common use cases.

---

## Example 1: E-Commerce Analytics Pipeline

### Use Case
Real-time and batch analytics for an e-commerce platform processing 10M+ daily orders.

### Requirements
- Real-time: Inventory updates, fraud detection (<1s latency)
- Near-real-time: Dashboards, recommendations (5-minute freshness)
- Batch: Daily reports, ML model training

### Architecture

```
                         Real-Time Path
                    +------------------------+
                    |                        v
+--------+    +-----+-----+    +-------+    +-------+    +-----------+
| Sources|    |   Kafka   |    | Flink |    | Redis |    | Real-time |
| (Apps) +--->| (Events)  +--->|(Stream)+-->|(Cache)+--->| Dashboard |
+--------+    +-----------+    +-------+    +-------+    +-----------+
                    |
                    |          Batch Path
                    v
              +-----------+    +-------+    +-----------+    +--------+
              |    S3     |    | Spark |    | Snowflake |    |  dbt   |
              |  (Raw)    +--->|(Batch)+--->| (Bronze)  +--->|(Models)|
              +-----------+    +-------+    +-----------+    +---+----+
                                                                 |
                    +-------------------+------------------------+
                    |                   |                        |
                    v                   v                        v
              +-----------+       +-----------+            +-----------+
              |   BI      |       |    ML     |            | Reverse   |
              | (Tableau) |       | (Training)|            | ETL       |
              +-----------+       +-----------+            +-----------+
```

### Technology Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Event streaming | Kafka | High throughput, exactly-once semantics |
| Stream processing | Flink | Low-latency fraud detection |
| Cache | Redis | Sub-ms inventory lookups |
| Data lake | S3 + Delta Lake | Cost-effective, ACID transactions |
| Warehouse | Snowflake | Scalable compute, separation of storage |
| Transformation | dbt | SQL-first, version controlled |
| Orchestration | Airflow | Mature, extensive integrations |
| Quality | Great Expectations + dbt tests | Multi-layer validation |

### Data Flow

1. **Order events** --> Kafka topic `orders.placed`
2. **Fraud service** consumes, scores in <100ms
3. **Flink** enriches with customer data, writes to Redis
4. **S3 sink** writes raw events to Bronze layer
5. **Spark job** (hourly) transforms to Silver
6. **dbt models** create Gold marts for BI
7. **Reverse ETL** syncs segments back to marketing tools

### Key Patterns Used
- Lambda architecture (real-time + batch)
- CDC for database replication
- Medallion architecture (Bronze/Silver/Gold)
- Event sourcing for order lifecycle

---

## Example 2: Real-Time Fraud Detection

### Use Case
Detect fraudulent transactions within 200ms for a fintech company processing 50K transactions/second.

### Requirements
- p99 latency: <200ms
- Availability: 99.99%
- ML model inference at scale
- Historical analysis for model training

### Architecture

```
+------------+    +-----------+    +----------------+    +----------+
| Payment    |    |   Kafka   |    |  Flink + ML    |    | Decision |
| Gateway    +--->|  (txns)   +--->|  (Inference)   +--->| Service  |
+------------+    +-----+-----+    +-------+--------+    +----+-----+
                        |                  |                  |
                        v                  v                  v
                  +-----------+      +----------+       +-----------+
                  | Feature   |      | Feature  |       | Alert     |
                  | Store     |      | Store    |       | Service   |
                  | (Redis)   |<---->| (Update) |       | (PagerDuty)|
                  +-----------+      +----------+       +-----------+
                        ^
                        |
              +---------+---------+
              |                   |
        +-----+-----+       +-----+-----+
        | Batch     |       | Model     |
        | Features  |       | Training  |
        | (Spark)   |       | (MLflow)  |
        +-----------+       +-----------+
```

### Technology Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Streaming | Kafka | Guaranteed delivery, replay |
| Processing | Flink | Low-latency, stateful processing |
| Feature store | Redis + Feast | Real-time + batch features |
| ML serving | Seldon/KServe | Kubernetes-native, auto-scaling |
| Training | Spark + MLflow | Distributed training, versioning |
| Monitoring | Prometheus + Grafana | Custom fraud metrics |

### Key Features

**Real-time Features:**
- Transaction amount deviation from 30-day average
- Geographic velocity (distance/time since last transaction)
- Device fingerprint risk score
- Merchant category risk

**Batch Features:**
- Customer lifetime value
- Historical chargeback rate
- Network graph embeddings (fraud rings)

### Streaming Logic (Flink)

```java
// Simplified fraud detection pipeline
DataStream<Transaction> transactions = env
    .addSource(new FlinkKafkaConsumer<>("transactions", schema, props));

DataStream<ScoredTransaction> scored = transactions
    .keyBy(Transaction::getCustomerId)
    .process(new FraudScoringFunction())  // ML inference
    .filter(tx -> tx.getScore() > THRESHOLD);

scored
    .addSink(new FlinkKafkaProducer<>("fraud-alerts", alertSchema, props));
```

### Error Handling
- Circuit breaker on ML service (fallback to rules)
- Dead letter queue for failed scoring
- Automatic replay from Kafka on recovery

---

## Example 3: Modern Data Stack for SaaS Analytics

### Use Case
Product analytics and customer health scoring for a B2B SaaS platform with 500+ data sources.

### Requirements
- Ingest from 500+ SaaS tools and databases
- Daily refresh for most data, hourly for critical metrics
- Self-serve analytics for business teams
- ML-powered customer health scores

### Architecture

```
+------------------+
| Sources (500+)   |
| - Salesforce     |
| - Stripe         |
| - PostgreSQL     |
| - Segment        |
+--------+---------+
         |
         v
+------------------+    +------------------+    +------------------+
|     Airbyte      |    |     Fivetran     |    |   Kafka + CDC    |
| (Open Source)    |    | (SaaS critical)  |    | (Real-time DB)   |
+--------+---------+    +--------+---------+    +--------+---------+
         |                       |                       |
         +-------------------+---+-----------------------+
                             |
                             v
                    +------------------+
                    |    Snowflake     |
                    |    (Bronze)      |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |       dbt        |
                    | (Silver + Gold)  |
                    +--------+---------+
                             |
         +-------------------+-------------------+
         |                   |                   |
         v                   v                   v
+------------------+ +------------------+ +------------------+
|   dbt Semantic   | |    Hightouch     | |    Databricks    |
|     Layer        | |  (Reverse ETL)   | |  (ML Training)   |
+--------+---------+ +--------+---------+ +--------+---------+
         |                   |                   |
         v                   v                   v
+------------------+ +------------------+ +------------------+
|     Looker       | |   Salesforce     | |  Health Score    |
|    (BI/Viz)      | |   (Enrichment)   | |    API           |
+------------------+ +------------------+ +------------------+
```

### Technology Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Ingestion (OSS) | Airbyte | 600+ connectors, cost-effective |
| Ingestion (managed) | Fivetran | Reliable for critical sources |
| CDC | Debezium --> Kafka | Real-time database changes |
| Warehouse | Snowflake | Auto-scaling, data sharing |
| Transformation | dbt Cloud | Managed, CI/CD built-in |
| Semantic layer | dbt Semantic Layer | Consistent metrics |
| Orchestration | Dagster Cloud | Asset-centric, modern |
| Reverse ETL | Hightouch | Activate data in tools |
| Quality | Soda Cloud | Continuous monitoring |
| Catalog | Atlan | Metadata, lineage, governance |

### dbt Project Structure

```
models/
├── staging/
│   ├── salesforce/
│   │   ├── _salesforce__sources.yml
│   │   ├── stg_salesforce__accounts.sql
│   │   └── stg_salesforce__opportunities.sql
│   ├── stripe/
│   │   ├── _stripe__sources.yml
│   │   ├── stg_stripe__customers.sql
│   │   └── stg_stripe__subscriptions.sql
│   └── product/
│       ├── _product__sources.yml
│       └── stg_product__events.sql
│
├── intermediate/
│   ├── finance/
│   │   └── int_mrr_by_customer.sql
│   └── product/
│       └── int_usage_aggregated_daily.sql
│
└── marts/
    ├── finance/
    │   ├── fct_mrr_movements.sql
    │   └── dim_subscriptions.sql
    ├── sales/
    │   ├── fct_opportunities.sql
    │   └── dim_accounts.sql
    └── product/
        ├── fct_daily_active_users.sql
        └── dim_features.sql
```

### Key Patterns
- ELT with medallion architecture
- Semantic layer for metric consistency
- Reverse ETL for data activation
- Data mesh with domain ownership

---

## Example 4: IoT Telemetry Pipeline

### Use Case
Process sensor data from 100K IoT devices, storing 1B+ events/day for predictive maintenance.

### Requirements
- Handle 100K concurrent device connections
- Sub-second ingestion latency
- 90-day hot storage, 7-year cold archive
- Real-time anomaly detection
- Time-series analytics

### Architecture

```
+------------------+
| IoT Devices      |
| (100K sensors)   |
+--------+---------+
         |
         v  (MQTT)
+------------------+    +------------------+
|   IoT Gateway    |    |  AWS IoT Core    |
|  (Edge compute)  +--->|  (MQTT Broker)   |
+------------------+    +--------+---------+
                                 |
                                 v
                        +------------------+
                        |  Kinesis/Kafka   |
                        |  (Buffering)     |
                        +--------+---------+
                                 |
             +-------------------+-------------------+
             |                                       |
             v                                       v
    +------------------+                    +------------------+
    |   Flink (Real)   |                    |   Lambda/Spark   |
    | Anomaly Detect   |                    |   (Batch agg)    |
    +--------+---------+                    +--------+---------+
             |                                       |
             v                                       v
    +------------------+                    +------------------+
    |  Alert Service   |                    |  TimescaleDB     |
    |  (PagerDuty)     |                    |  (Hot storage)   |
    +------------------+                    +--------+---------+
                                                     |
                                                     v
                                            +------------------+
                                            |  Grafana         |
                                            |  (Dashboards)    |
                                            +------------------+
                                                     |
                                        Archive      |
                                            +--------v---------+
                                            |  S3 + Parquet    |
                                            |  (Cold storage)  |
                                            +------------------+
```

### Technology Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Edge gateway | AWS IoT Greengrass | Local processing, filtering |
| MQTT broker | AWS IoT Core | Managed, auto-scaling |
| Streaming | Kinesis Data Streams | Integrated with AWS |
| Real-time processing | Apache Flink | Complex event processing |
| Hot storage | TimescaleDB | Time-series optimized |
| Cold storage | S3 + Parquet | Cost-effective archival |
| Visualization | Grafana | Time-series dashboards |
| Orchestration | Airflow | Batch job scheduling |

### Data Schema

```json
{
  "device_id": "sensor-12345",
  "timestamp": "2025-01-25T10:30:00Z",
  "metrics": {
    "temperature": 72.5,
    "humidity": 45.2,
    "vibration": 0.003,
    "power_consumption": 120.5
  },
  "metadata": {
    "firmware_version": "2.1.3",
    "location": "building-a-floor-3"
  }
}
```

### Anomaly Detection Rules

```sql
-- Flink SQL for anomaly detection
SELECT
  device_id,
  TUMBLE_START(event_time, INTERVAL '5' MINUTE) as window_start,
  AVG(temperature) as avg_temp,
  STDDEV(temperature) as std_temp
FROM sensor_readings
GROUP BY device_id, TUMBLE(event_time, INTERVAL '5' MINUTE)
HAVING AVG(temperature) > 3 * STDDEV(temperature) + LAG_AVG;
```

### Key Patterns
- Edge computing for filtering/aggregation
- Tiered storage (hot/warm/cold)
- Time-series database for queries
- Complex event processing (CEP)

---

## Example 5: ML Feature Pipeline

### Use Case
Unified feature store for real-time and batch ML features serving 50+ models.

### Requirements
- Consistent features for training and serving
- <10ms feature retrieval latency
- Point-in-time correct training data
- Feature versioning and lineage

### Architecture

```
+------------------+         +------------------+
| Batch Sources    |         | Stream Sources   |
| (Warehouse, S3)  |         | (Kafka, Events)  |
+--------+---------+         +--------+---------+
         |                            |
         v                            v
+------------------+         +------------------+
| Spark Batch      |         | Flink Stream     |
| (Feature Eng)    |         | (Feature Eng)    |
+--------+---------+         +--------+---------+
         |                            |
         v                            v
+--------------------------------------------------+
|                 Feature Store (Feast)            |
|  +-------------------+  +---------------------+  |
|  | Offline Store     |  | Online Store        |  |
|  | (S3/BigQuery)     |  | (Redis/DynamoDB)    |  |
|  +-------------------+  +---------------------+  |
+------------------------+-------------------------+
                         |
         +---------------+---------------+
         |                               |
         v                               v
+------------------+             +------------------+
|  Training        |             |  Online Serving  |
|  (get_training_  |             |  (get_online_    |
|   features())    |             |   features())    |
+--------+---------+             +--------+---------+
         |                                |
         v                                v
+------------------+             +------------------+
|  ML Training     |             |  Inference       |
|  (Spark/PyTorch) |             |  (KServe)        |
+------------------+             +------------------+
```

### Technology Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Feature store | Feast | Open source, K8s native |
| Offline store | BigQuery | Point-in-time queries |
| Online store | Redis | Sub-ms retrieval |
| Batch compute | Spark | Large-scale aggregations |
| Stream compute | Flink | Real-time features |
| Orchestration | Dagster | Asset-first, ML-focused |
| ML platform | MLflow + KServe | Training + serving |

### Feature Definition (Feast)

```python
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from datetime import timedelta

# Entity definition
customer = Entity(
    name="customer_id",
    value_type=ValueType.STRING,
    description="Customer identifier"
)

# Batch feature view
customer_features = FeatureView(
    name="customer_features",
    entities=["customer_id"],
    ttl=timedelta(days=1),
    features=[
        Feature(name="total_purchases_30d", dtype=ValueType.FLOAT),
        Feature(name="avg_order_value", dtype=ValueType.FLOAT),
        Feature(name="days_since_last_purchase", dtype=ValueType.INT32),
        Feature(name="customer_segment", dtype=ValueType.STRING),
    ],
    online=True,
    batch_source=FileSource(
        path="s3://features/customer_features.parquet",
        timestamp_field="event_timestamp",
    ),
)

# Stream feature view (real-time)
customer_realtime = StreamFeatureView(
    name="customer_realtime_features",
    entities=["customer_id"],
    features=[
        Feature(name="session_page_views", dtype=ValueType.INT32),
        Feature(name="cart_value", dtype=ValueType.FLOAT),
    ],
    online=True,
    source=KafkaSource(
        name="customer_events",
        kafka_bootstrap_servers="kafka:9092",
        topic="customer.events",
        timestamp_field="event_timestamp",
    ),
)
```

### Key Patterns
- Feature store for consistency
- Point-in-time joins for training
- Dual store architecture (offline + online)
- Feature versioning and registry

---

## Example 6: Data Quality-First Pipeline

### Use Case
Compliance-critical data pipeline for healthcare with strict data quality requirements.

### Requirements
- HIPAA compliance
- 99.99% data accuracy
- Full audit trail
- Automated quality gates

### Architecture

```
+------------------+
| EHR Systems      |
| (HL7/FHIR)       |
+--------+---------+
         |
         v  (Encrypted)
+------------------+    +------------------+
| API Gateway      |    | Validation       |
| (Auth + Audit)   +--->| (Schema + PII)   |
+------------------+    +--------+---------+
                                 |
                        +--------v---------+
                        | Great Expectations|
                        | (Pre-load checks) |
                        +--------+---------+
                                 |
                   Pass?         |          Fail?
              +------------------+------------------+
              |                                     |
              v                                     v
     +------------------+                  +------------------+
     | Snowflake        |                  | Quarantine       |
     | (Bronze, masked) |                  | (S3 + Alert)     |
     +--------+---------+                  +------------------+
              |
              v
     +------------------+
     | dbt (Transform)  |
     | + dbt tests      |
     +--------+---------+
              |
              v
     +------------------+
     | Great Expectations|
     | (Post-transform) |
     +--------+---------+
              |
              v
     +------------------+
     | Silver Layer     |
     | (Quality scored) |
     +--------+---------+
              |
              v
     +------------------+
     | Soda Cloud       |
     | (Monitoring)     |
     +------------------+
```

### Quality Checks by Layer

**Ingestion Layer (Great Expectations):**
```python
expectation_suite = ExpectationSuite(name="patient_records")
expectation_suite.add_expectation(
    ExpectColumnValuesToNotBeNull(column="patient_id")
)
expectation_suite.add_expectation(
    ExpectColumnValuesToMatchRegex(
        column="ssn",
        regex=r"^\d{3}-\d{2}-\d{4}$"
    )
)
expectation_suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="age",
        min_value=0,
        max_value=150
    )
)
```

**Transformation Layer (dbt tests):**
```yaml
# schema.yml
version: 2
models:
  - name: fct_patient_visits
    columns:
      - name: patient_id
        tests:
          - unique
          - not_null
          - relationships:
              to: ref('dim_patients')
              field: patient_id
      - name: visit_date
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: "'2020-01-01'"
              max_value: "current_date"
```

**Continuous Monitoring (Soda):**
```yaml
# soda checks
checks for fct_patient_visits:
  - row_count > 0
  - freshness(visit_date) < 1d
  - duplicate_count(patient_id, visit_date) = 0
  - missing_percent(diagnosis_code) < 5%
  - anomaly detection for row_count
```

### Key Patterns
- Pre-load validation (fail fast)
- Quarantine pattern for bad data
- Multi-layer quality checks
- Quality scoring and metrics
- Continuous monitoring

---

## Quick Reference: Pattern Selection

| Scenario | Recommended Pattern |
|----------|---------------------|
| High volume, batch OK | ELT + Medallion |
| Real-time + batch | Lambda with Kafka + Spark |
| Streaming-only | Kappa with Kafka + Flink |
| Multi-source SaaS | Airbyte/Fivetran + dbt |
| ML features | Feature store (Feast) |
| IoT high-volume | Edge compute + time-series DB |
| Compliance-critical | Quality-first with quarantine |
