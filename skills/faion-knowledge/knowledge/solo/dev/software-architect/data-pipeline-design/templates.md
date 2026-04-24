# Data Pipeline Templates

Copy-paste configurations for common data pipeline components.

---

## Table of Contents

1. [Apache Airflow DAGs](#apache-airflow-dags)
2. [Apache Kafka Configuration](#apache-kafka-configuration)
3. [Apache Spark Jobs](#apache-spark-jobs)
4. [dbt Models and Tests](#dbt-models-and-tests)
5. [Data Quality (Great Expectations)](#data-quality-great-expectations)
6. [Data Quality (Soda)](#data-quality-soda)
7. [Dagster Assets](#dagster-assets)
8. [Prefect Flows](#prefect-flows)
9. [Docker Compose Stacks](#docker-compose-stacks)

---

## Apache Airflow DAGs

### Basic ETL DAG

```python
# dags/etl_pipeline.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.s3_to_sql import S3ToSqlOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(hours=1),
}

with DAG(
    dag_id='etl_sales_pipeline',
    default_args=default_args,
    description='Daily sales data ETL pipeline',
    schedule_interval='0 6 * * *',  # 6 AM daily
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'sales', 'production'],
) as dag:

    def extract_data(**context):
        """Extract data from source systems."""
        execution_date = context['ds']
        # Extract logic here
        return {'records_extracted': 1000}

    def transform_data(**context):
        """Transform extracted data."""
        ti = context['ti']
        extract_result = ti.xcom_pull(task_ids='extract')
        # Transform logic here
        return {'records_transformed': 950}

    def load_data(**context):
        """Load data to destination."""
        ti = context['ti']
        transform_result = ti.xcom_pull(task_ids='transform')
        # Load logic here
        return {'records_loaded': 950}

    def validate_data(**context):
        """Validate loaded data."""
        # Great Expectations validation
        pass

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )

    validate = PythonOperator(
        task_id='validate',
        python_callable=validate_data,
    )

    extract >> transform >> load >> validate
```

### dbt Integration DAG

```python
# dags/dbt_pipeline.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    'owner': 'analytics-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

DBT_PROJECT_DIR = '/opt/airflow/dbt'
DBT_PROFILES_DIR = '/opt/airflow/dbt/profiles'

with DAG(
    dag_id='dbt_transform_pipeline',
    default_args=default_args,
    schedule_interval='0 7 * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['dbt', 'transformation'],
) as dag:

    dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt deps --profiles-dir {DBT_PROFILES_DIR}',
    )

    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt seed --profiles-dir {DBT_PROFILES_DIR}',
    )

    dbt_run_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select staging --profiles-dir {DBT_PROFILES_DIR}',
    )

    dbt_test_staging = BashOperator(
        task_id='dbt_test_staging',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --select staging --profiles-dir {DBT_PROFILES_DIR}',
    )

    dbt_run_marts = BashOperator(
        task_id='dbt_run_marts',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select marts --profiles-dir {DBT_PROFILES_DIR}',
    )

    dbt_test_marts = BashOperator(
        task_id='dbt_test_marts',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --select marts --profiles-dir {DBT_PROFILES_DIR}',
    )

    dbt_docs_generate = BashOperator(
        task_id='dbt_docs_generate',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt docs generate --profiles-dir {DBT_PROFILES_DIR}',
        trigger_rule=TriggerRule.ALL_DONE,
    )

    dbt_deps >> dbt_seed >> dbt_run_staging >> dbt_test_staging
    dbt_test_staging >> dbt_run_marts >> dbt_test_marts >> dbt_docs_generate
```

### Sensor-based DAG with Branching

```python
# dags/sensor_pipeline.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.s3_key_sensor import S3KeySensor
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    'owner': 'data-team',
    'retries': 1,
}

def check_data_quality(**context):
    """Check if data passes quality threshold."""
    # Implement quality check logic
    quality_score = 0.95  # Example
    if quality_score >= 0.9:
        return 'process_full_data'
    elif quality_score >= 0.7:
        return 'process_with_warnings'
    else:
        return 'quarantine_data'

with DAG(
    dag_id='sensor_branching_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Triggered by sensor
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['sensor', 'quality-gate'],
) as dag:

    wait_for_file = S3KeySensor(
        task_id='wait_for_file',
        bucket_name='data-lake',
        bucket_key='incoming/{{ ds }}/data.parquet',
        aws_conn_id='aws_default',
        poke_interval=300,  # 5 minutes
        timeout=3600,  # 1 hour
        mode='reschedule',  # Don't block worker slot
    )

    quality_check = BranchPythonOperator(
        task_id='quality_check',
        python_callable=check_data_quality,
    )

    process_full = PythonOperator(
        task_id='process_full_data',
        python_callable=lambda: print("Processing full data"),
    )

    process_warnings = PythonOperator(
        task_id='process_with_warnings',
        python_callable=lambda: print("Processing with warnings"),
    )

    quarantine = PythonOperator(
        task_id='quarantine_data',
        python_callable=lambda: print("Quarantining data"),
    )

    notify = PythonOperator(
        task_id='notify_completion',
        python_callable=lambda: print("Pipeline complete"),
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    wait_for_file >> quality_check
    quality_check >> [process_full, process_warnings, quarantine]
    [process_full, process_warnings, quarantine] >> notify
```

---

## Apache Kafka Configuration

### Producer Configuration (Python)

```python
# kafka_producer.py
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import json

# Schema Registry configuration
schema_registry_conf = {
    'url': 'http://schema-registry:8081'
}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Avro schema
order_schema = """
{
  "type": "record",
  "name": "Order",
  "namespace": "com.example.orders",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "currency", "type": "string", "default": "USD"},
    {"name": "created_at", "type": "long", "logicalType": "timestamp-millis"},
    {"name": "items", "type": {"type": "array", "items": "string"}}
  ]
}
"""

avro_serializer = AvroSerializer(
    schema_registry_client,
    order_schema,
    lambda obj, ctx: obj  # to_dict function
)

# Producer configuration
producer_conf = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'order-service',
    'acks': 'all',
    'retries': 3,
    'retry.backoff.ms': 100,
    'enable.idempotence': True,
    'max.in.flight.requests.per.connection': 5,
    'compression.type': 'snappy',
    'linger.ms': 5,
    'batch.size': 16384,
}

producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_order(order: dict):
    producer.produce(
        topic='orders.placed',
        key=order['order_id'],
        value=avro_serializer(
            order,
            SerializationContext('orders.placed', MessageField.VALUE)
        ),
        on_delivery=delivery_report,
    )
    producer.poll(0)

# Example usage
order = {
    'order_id': 'ORD-12345',
    'customer_id': 'CUST-001',
    'amount': 99.99,
    'currency': 'USD',
    'created_at': 1706180400000,
    'items': ['SKU-001', 'SKU-002']
}
produce_order(order)
producer.flush()
```

### Consumer Configuration (Python)

```python
# kafka_consumer.py
from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
import signal
import sys

# Schema Registry
schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_deserializer = AvroDeserializer(
    schema_registry_client,
    lambda obj, ctx: obj  # from_dict function
)

# Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'order-processor',
    'client.id': 'order-processor-1',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Manual commit for exactly-once
    'max.poll.interval.ms': 300000,
    'session.timeout.ms': 45000,
    'heartbeat.interval.ms': 3000,
    'fetch.min.bytes': 1,
    'fetch.max.wait.ms': 500,
}

consumer = Consumer(consumer_conf)

running = True

def shutdown_handler(signum, frame):
    global running
    running = False

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

def process_message(message):
    """Process a single message."""
    order = avro_deserializer(
        message.value(),
        SerializationContext(message.topic(), MessageField.VALUE)
    )
    print(f"Processing order: {order['order_id']}")
    # Add processing logic here
    return True

def consume_loop():
    consumer.subscribe(['orders.placed'])

    try:
        while running:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())

            try:
                if process_message(msg):
                    consumer.commit(message=msg)
            except Exception as e:
                print(f"Error processing message: {e}")
                # Send to DLQ or retry topic
    finally:
        consumer.close()

if __name__ == '__main__':
    consume_loop()
```

### Kafka Connect Configuration

```json
{
  "name": "postgres-cdc-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${env:POSTGRES_PASSWORD}",
    "database.dbname": "app_db",
    "database.server.name": "app",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.name": "dbz_publication",
    "table.include.list": "public.orders,public.customers",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "key.converter.schema.registry.url": "http://schema-registry:8081",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://schema-registry:8081",
    "topic.prefix": "cdc",
    "heartbeat.interval.ms": "10000",
    "snapshot.mode": "initial"
  }
}
```

---

## Apache Spark Jobs

### Batch ETL Job (PySpark)

```python
# spark_batch_etl.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, lit, to_date, current_timestamp,
    sum as spark_sum, count, avg
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from delta import DeltaTable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_spark_session():
    return (SparkSession.builder
        .appName("SalesETL")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate())

def extract(spark, source_path: str, date: str):
    """Extract data from source."""
    logger.info(f"Extracting data from {source_path} for date {date}")

    df = (spark.read
        .format("parquet")
        .load(f"{source_path}/date={date}")
    )

    logger.info(f"Extracted {df.count()} records")
    return df

def transform(df):
    """Apply business transformations."""
    logger.info("Applying transformations")

    transformed = (df
        # Clean nulls
        .fillna({'discount': 0.0, 'tax': 0.0})
        # Calculate derived fields
        .withColumn('net_amount', col('amount') - col('discount') + col('tax'))
        .withColumn('profit_margin', (col('amount') - col('cost')) / col('amount'))
        # Categorize
        .withColumn('customer_tier',
            when(col('total_purchases') > 10000, 'platinum')
            .when(col('total_purchases') > 5000, 'gold')
            .when(col('total_purchases') > 1000, 'silver')
            .otherwise('bronze')
        )
        # Add metadata
        .withColumn('processed_at', current_timestamp())
    )

    return transformed

def load(df, target_path: str, partition_cols: list = None):
    """Load data to Delta Lake with merge."""
    logger.info(f"Loading data to {target_path}")

    if DeltaTable.isDeltaTable(spark, target_path):
        # Merge (upsert)
        delta_table = DeltaTable.forPath(spark, target_path)

        (delta_table.alias("target")
            .merge(
                df.alias("source"),
                "target.order_id = source.order_id"
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )
        logger.info("Merge completed")
    else:
        # Initial load
        writer = df.write.format("delta").mode("overwrite")
        if partition_cols:
            writer = writer.partitionBy(*partition_cols)
        writer.save(target_path)
        logger.info("Initial load completed")

def create_aggregations(spark, source_path: str, target_path: str):
    """Create aggregated tables for analytics."""
    df = spark.read.format("delta").load(source_path)

    # Daily aggregations
    daily_agg = (df
        .groupBy(to_date('order_date').alias('date'), 'product_category')
        .agg(
            count('*').alias('order_count'),
            spark_sum('net_amount').alias('total_revenue'),
            avg('net_amount').alias('avg_order_value'),
            spark_sum('quantity').alias('units_sold')
        )
    )

    (daily_agg.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("date")
        .save(f"{target_path}/daily_sales")
    )

def main(date: str):
    spark = create_spark_session()

    try:
        # Bronze -> Silver
        bronze_df = extract(spark, "s3://data-lake/bronze/sales", date)
        silver_df = transform(bronze_df)
        load(silver_df, "s3://data-lake/silver/sales", ['order_date'])

        # Silver -> Gold (aggregations)
        create_aggregations(
            spark,
            "s3://data-lake/silver/sales",
            "s3://data-lake/gold"
        )

        logger.info("ETL completed successfully")
    except Exception as e:
        logger.error(f"ETL failed: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else "2025-01-25"
    main(date)
```

### Structured Streaming Job

```python
# spark_streaming.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, sum as spark_sum, count,
    to_timestamp, current_timestamp
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

def create_spark_session():
    return (SparkSession.builder
        .appName("OrdersStreamProcessor")
        .config("spark.sql.streaming.checkpointLocation", "/checkpoints/orders")
        .config("spark.sql.streaming.stateStore.stateSchemaCheck", "false")
        .getOrCreate())

# Define schema for incoming events
order_schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("amount", DoubleType(), False),
    StructField("currency", StringType(), True),
    StructField("created_at", LongType(), False),
    StructField("category", StringType(), True),
])

def main():
    spark = create_spark_session()

    # Read from Kafka
    raw_stream = (spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "orders.placed")
        .option("startingOffsets", "latest")
        .option("failOnDataLoss", "false")
        .load()
    )

    # Parse JSON and transform
    orders = (raw_stream
        .select(from_json(col("value").cast("string"), order_schema).alias("data"))
        .select("data.*")
        .withColumn("event_time", to_timestamp(col("created_at") / 1000))
    )

    # Windowed aggregation
    windowed_counts = (orders
        .withWatermark("event_time", "10 minutes")
        .groupBy(
            window(col("event_time"), "5 minutes", "1 minute"),
            col("category")
        )
        .agg(
            count("*").alias("order_count"),
            spark_sum("amount").alias("total_amount")
        )
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("category"),
            col("order_count"),
            col("total_amount")
        )
    )

    # Write to Delta Lake
    query = (windowed_counts
        .writeStream
        .format("delta")
        .outputMode("update")
        .option("checkpointLocation", "/checkpoints/orders_agg")
        .trigger(processingTime="30 seconds")
        .start("s3://data-lake/silver/orders_5min_agg")
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
```

---

## dbt Models and Tests

### Project Structure

```yaml
# dbt_project.yml
name: 'analytics'
version: '1.0.0'
config-version: 2

profile: 'analytics'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

vars:
  start_date: '2020-01-01'
  currency: 'USD'

models:
  analytics:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +schema: analytics
      finance:
        +tags: ['finance', 'daily']
      product:
        +tags: ['product', 'daily']
```

### Staging Model

```sql
-- models/staging/stripe/stg_stripe__payments.sql

with source as (
    select * from {{ source('stripe', 'payments') }}
),

renamed as (
    select
        -- ids
        id as payment_id,
        customer as customer_id,
        invoice as invoice_id,

        -- amounts (convert from cents to dollars)
        amount / 100.0 as amount,
        amount_received / 100.0 as amount_received,

        -- status and metadata
        status as payment_status,
        currency,
        payment_method_types[1] as payment_method,

        -- timestamps
        to_timestamp(created) as created_at,
        to_timestamp({{ dbt_utils.safe_cast('metadata:processed_at', 'bigint') }}) as processed_at,

        -- deduplication
        row_number() over (
            partition by id
            order by created desc
        ) as row_num

    from source
)

select * from renamed
where row_num = 1
```

### Intermediate Model

```sql
-- models/intermediate/finance/int_payments_enriched.sql

with payments as (
    select * from {{ ref('stg_stripe__payments') }}
),

customers as (
    select * from {{ ref('stg_stripe__customers') }}
),

subscriptions as (
    select * from {{ ref('stg_stripe__subscriptions') }}
),

enriched as (
    select
        p.payment_id,
        p.customer_id,
        c.email as customer_email,
        c.name as customer_name,
        s.subscription_id,
        s.plan_name,
        s.plan_interval,
        p.amount,
        p.amount_received,
        p.payment_status,
        p.currency,
        p.payment_method,
        p.created_at,

        -- derived fields
        case
            when p.amount_received = p.amount then 'full'
            when p.amount_received > 0 then 'partial'
            else 'none'
        end as collection_status,

        -- window functions for customer metrics
        sum(p.amount) over (
            partition by p.customer_id
            order by p.created_at
            rows between unbounded preceding and current row
        ) as customer_ltv

    from payments p
    left join customers c on p.customer_id = c.customer_id
    left join subscriptions s on c.customer_id = s.customer_id
        and p.created_at between s.started_at and coalesce(s.ended_at, current_timestamp())
)

select * from enriched
```

### Mart Model with Incremental

```sql
-- models/marts/finance/fct_monthly_revenue.sql

{{
    config(
        materialized='incremental',
        unique_key='month_key',
        incremental_strategy='merge',
        partition_by={
            "field": "revenue_month",
            "data_type": "date",
            "granularity": "month"
        }
    )
}}

with payments as (
    select * from {{ ref('int_payments_enriched') }}
    {% if is_incremental() %}
    where created_at >= (select max(revenue_month) from {{ this }})
    {% endif %}
),

monthly as (
    select
        date_trunc('month', created_at)::date as revenue_month,
        plan_name,
        plan_interval,
        currency,

        -- metrics
        count(distinct payment_id) as payment_count,
        count(distinct customer_id) as paying_customers,
        sum(amount_received) as gross_revenue,
        sum(case when collection_status = 'full' then amount_received else 0 end) as collected_revenue,

        -- create surrogate key
        {{ dbt_utils.generate_surrogate_key([
            'revenue_month',
            'plan_name',
            'plan_interval',
            'currency'
        ]) }} as month_key

    from payments
    where payment_status = 'succeeded'
    group by 1, 2, 3, 4
)

select * from monthly
```

### Schema Tests

```yaml
# models/staging/stripe/_stripe__sources.yml
version: 2

sources:
  - name: stripe
    database: raw
    schema: stripe
    tables:
      - name: payments
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
        loaded_at_field: _loaded_at
        columns:
          - name: id
            tests:
              - unique
              - not_null

---
# models/marts/finance/_finance__models.yml
version: 2

models:
  - name: fct_monthly_revenue
    description: "Monthly revenue aggregated by plan and currency"
    columns:
      - name: month_key
        description: "Surrogate key for the record"
        tests:
          - unique
          - not_null

      - name: revenue_month
        description: "First day of the revenue month"
        tests:
          - not_null

      - name: gross_revenue
        description: "Total amount charged"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0

      - name: paying_customers
        description: "Count of unique paying customers"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0

  - name: fct_daily_active_users
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - date
            - platform
```

---

## Data Quality (Great Expectations)

### Expectation Suite

```python
# great_expectations/expectations/orders_suite.py
import great_expectations as gx

context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite(expectation_suite_name="orders_quality")

# Schema expectations
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(column="customer_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(column="amount")
)

# Completeness expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="created_at")
)

# Uniqueness expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
)

# Format expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        column="order_id",
        regex=r"^ORD-[A-Z0-9]{8}$"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchStrftimeFormat(
        column="created_at",
        strftime_format="%Y-%m-%d %H:%M:%S"
    )
)

# Range expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount",
        min_value=0,
        max_value=1000000
    )
)

# Categorical expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["pending", "processing", "completed", "cancelled", "refunded"]
    )
)

# Referential integrity (custom expectation)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        column_A="total_amount",
        column_B="discount",
        or_equal=True
    )
)

# Statistical expectations
suite.add_expectation(
    gx.expectations.ExpectColumnMeanToBeBetween(
        column="amount",
        min_value=50,
        max_value=500
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnDistinctValuesToBeInSet(
        column="currency",
        value_set=["USD", "EUR", "GBP"]
    )
)

# Save suite
context.save_expectation_suite(suite)
```

### Validation in Pipeline

```python
# validate_data.py
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint

def validate_orders(file_path: str) -> bool:
    """Validate orders data and return success status."""
    context = gx.get_context()

    # Create batch request
    batch_request = {
        "datasource_name": "my_datasource",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": "orders",
        "batch_spec_passthrough": {
            "path": file_path
        }
    }

    # Run checkpoint
    checkpoint_config = {
        "name": "orders_checkpoint",
        "config_version": 1.0,
        "class_name": "Checkpoint",
        "run_name_template": "%Y%m%d-%H%M%S-orders-validation",
        "validations": [
            {
                "batch_request": batch_request,
                "expectation_suite_name": "orders_quality",
                "action_list": [
                    {
                        "name": "store_validation_result",
                        "action": {
                            "class_name": "StoreValidationResultAction"
                        }
                    },
                    {
                        "name": "update_data_docs",
                        "action": {
                            "class_name": "UpdateDataDocsAction"
                        }
                    },
                    {
                        "name": "send_slack_notification",
                        "action": {
                            "class_name": "SlackNotificationAction",
                            "slack_webhook": "${SLACK_WEBHOOK}",
                            "notify_on": "failure"
                        }
                    }
                ]
            }
        ]
    }

    checkpoint = Checkpoint(**checkpoint_config, data_context=context)
    result = checkpoint.run()

    return result.success
```

---

## Data Quality (Soda)

### SodaCL Checks

```yaml
# checks/orders_checks.yml
# Soda Checks for orders table

checks for orders:
  # Row count checks
  - row_count > 0
  - row_count:
      warn: when < 1000
      fail: when < 100

  # Freshness check
  - freshness(created_at) < 1d

  # Schema checks
  - schema:
      warn:
        when required column missing: [order_id, customer_id, amount]
      fail:
        when forbidden column present: [ssn, password]

  # Completeness checks
  - missing_count(order_id) = 0
  - missing_count(customer_id) = 0
  - missing_percent(email) < 5%

  # Uniqueness checks
  - duplicate_count(order_id) = 0

  # Validity checks
  - invalid_count(amount) = 0:
      valid min: 0
      valid max: 1000000

  - invalid_count(status) = 0:
      valid values: [pending, processing, completed, cancelled]

  - invalid_count(email) = 0:
      valid regex: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

  # Referential integrity
  - values in (customer_id) must exist in dim_customers (customer_id)

  # Anomaly detection
  - anomaly detection for row_count:
      warn: when > 2 stdev
      fail: when > 3 stdev

  - anomaly detection for avg(amount):
      training_days: 30
      warn: when > 2 stdev

  # Cross-check
  - row_count same as orders_staging

  # Custom SQL
  - failed rows:
      name: Orders with negative amounts
      fail query: |
        SELECT order_id, amount
        FROM orders
        WHERE amount < 0

---
# checks/daily_metrics.yml
checks for daily_metrics:
  # Distribution checks
  - avg(revenue) between 10000 and 1000000
  - stddev(revenue) < 50000

  # Trend checks
  - change for row_count < 50%
  - change avg last 7 for revenue between -20% and 20%

  # Reference checks
  - sum(revenue) = sum(payments.amount):
      filter: date = ${DATE}
```

### Soda Configuration

```yaml
# configuration.yml
data_source my_warehouse:
  type: snowflake
  account: ${SNOWFLAKE_ACCOUNT}
  username: ${SNOWFLAKE_USER}
  password: ${SNOWFLAKE_PASSWORD}
  database: ANALYTICS
  warehouse: COMPUTE_WH
  schema: PUBLIC
  role: SODA_ROLE

soda_cloud:
  host: cloud.soda.io
  api_key_id: ${SODA_API_KEY_ID}
  api_key_secret: ${SODA_API_KEY_SECRET}
```

---

## Dagster Assets

### Asset Definitions

```python
# assets/sales_pipeline.py
from dagster import (
    asset, AssetIn, AssetOut, Output, MetadataValue,
    FreshnessPolicy, AutoMaterializePolicy, DailyPartitionsDefinition
)
import pandas as pd

daily_partitions = DailyPartitionsDefinition(start_date="2025-01-01")

@asset(
    description="Raw sales data from source system",
    group_name="bronze",
    partitions_def=daily_partitions,
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=60),
)
def raw_sales(context) -> Output[pd.DataFrame]:
    """Extract raw sales data from source."""
    partition_date = context.partition_key

    # Extract logic
    df = pd.read_parquet(f"s3://source/sales/{partition_date}.parquet")

    return Output(
        df,
        metadata={
            "row_count": MetadataValue.int(len(df)),
            "columns": MetadataValue.json(list(df.columns)),
            "partition": MetadataValue.text(partition_date),
        }
    )


@asset(
    description="Cleaned and validated sales data",
    group_name="silver",
    ins={"raw_sales": AssetIn()},
    partitions_def=daily_partitions,
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
def clean_sales(context, raw_sales: pd.DataFrame) -> Output[pd.DataFrame]:
    """Clean and validate sales data."""

    # Data cleaning
    df = raw_sales.copy()
    df = df.dropna(subset=['order_id', 'customer_id'])
    df = df.drop_duplicates(subset=['order_id'])
    df['amount'] = df['amount'].clip(lower=0)

    # Validation
    assert len(df) > 0, "No data after cleaning"
    assert df['amount'].min() >= 0, "Negative amounts found"

    return Output(
        df,
        metadata={
            "row_count": MetadataValue.int(len(df)),
            "rows_dropped": MetadataValue.int(len(raw_sales) - len(df)),
            "null_rate": MetadataValue.float(df.isnull().mean().mean()),
        }
    )


@asset(
    description="Daily aggregated sales metrics",
    group_name="gold",
    ins={"clean_sales": AssetIn()},
    partitions_def=daily_partitions,
)
def daily_sales_metrics(context, clean_sales: pd.DataFrame) -> Output[pd.DataFrame]:
    """Aggregate sales by day."""

    df = clean_sales.groupby('product_category').agg({
        'order_id': 'count',
        'amount': ['sum', 'mean'],
        'customer_id': 'nunique',
    }).reset_index()

    df.columns = ['category', 'order_count', 'revenue', 'avg_order_value', 'unique_customers']
    df['date'] = context.partition_key

    return Output(
        df,
        metadata={
            "categories": MetadataValue.int(len(df)),
            "total_revenue": MetadataValue.float(df['revenue'].sum()),
        }
    )


@asset(
    description="Customer lifetime value calculations",
    group_name="gold",
    ins={"clean_sales": AssetIn()},
    non_partitioned_deps=["dim_customers"],
)
def customer_ltv(clean_sales: pd.DataFrame) -> pd.DataFrame:
    """Calculate customer lifetime value."""

    ltv = clean_sales.groupby('customer_id').agg({
        'amount': 'sum',
        'order_id': 'count',
        'order_date': ['min', 'max'],
    }).reset_index()

    ltv.columns = ['customer_id', 'total_spend', 'order_count', 'first_order', 'last_order']

    return ltv
```

### Dagster Jobs and Schedules

```python
# jobs/pipeline_jobs.py
from dagster import (
    define_asset_job, AssetSelection, ScheduleDefinition,
    DefaultScheduleStatus, RunRequest, schedule
)

# Define jobs
daily_etl_job = define_asset_job(
    name="daily_etl_job",
    selection=AssetSelection.groups("bronze", "silver", "gold"),
    description="Daily ETL pipeline for sales data",
)

hourly_metrics_job = define_asset_job(
    name="hourly_metrics_job",
    selection=AssetSelection.assets("daily_sales_metrics"),
    description="Hourly refresh of sales metrics",
)

# Define schedules
daily_schedule = ScheduleDefinition(
    job=daily_etl_job,
    cron_schedule="0 6 * * *",  # 6 AM daily
    default_status=DefaultScheduleStatus.RUNNING,
)

@schedule(cron_schedule="0 * * * *", job=hourly_metrics_job)
def hourly_schedule(context):
    """Hourly schedule with dynamic partitioning."""
    scheduled_date = context.scheduled_execution_time.strftime("%Y-%m-%d")
    return RunRequest(
        run_key=scheduled_date,
        partition_key=scheduled_date,
    )
```

---

## Prefect Flows

### Basic ETL Flow

```python
# flows/etl_flow.py
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd

@task(
    retries=3,
    retry_delay_seconds=60,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1),
)
def extract(source_path: str, date: str) -> pd.DataFrame:
    """Extract data from source."""
    df = pd.read_parquet(f"{source_path}/{date}.parquet")
    return df


@task(retries=2, retry_delay_seconds=30)
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform extracted data."""
    # Clean
    df = df.dropna(subset=['id'])
    df = df.drop_duplicates()

    # Enrich
    df['processed_at'] = pd.Timestamp.now()

    return df


@task(retries=3, retry_delay_seconds=120)
def load(df: pd.DataFrame, target_path: str) -> int:
    """Load data to destination."""
    df.to_parquet(target_path, index=False)
    return len(df)


@task
def validate(df: pd.DataFrame) -> bool:
    """Validate data quality."""
    assert len(df) > 0, "Empty dataframe"
    assert df['amount'].min() >= 0, "Negative amounts"
    return True


@flow(
    name="daily-etl",
    description="Daily ETL pipeline",
    retries=1,
    retry_delay_seconds=300,
)
def etl_pipeline(date: str, source_path: str, target_path: str):
    """Main ETL flow."""

    # Extract
    raw_data = extract(source_path, date)

    # Transform
    clean_data = transform(raw_data)

    # Validate
    is_valid = validate(clean_data)

    # Load only if valid
    if is_valid:
        rows_loaded = load(clean_data, f"{target_path}/{date}.parquet")
        return {"status": "success", "rows": rows_loaded}
    else:
        return {"status": "failed", "reason": "validation_failed"}


if __name__ == "__main__":
    etl_pipeline(
        date="2025-01-25",
        source_path="s3://data-lake/raw",
        target_path="s3://data-lake/processed"
    )
```

### Deployment Configuration

```python
# deployments/etl_deployment.py
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from flows.etl_flow import etl_pipeline

deployment = Deployment.build_from_flow(
    flow=etl_pipeline,
    name="daily-etl-prod",
    version="1.0.0",
    work_queue_name="default",
    parameters={
        "source_path": "s3://prod-data-lake/raw",
        "target_path": "s3://prod-data-lake/processed",
    },
    schedule=CronSchedule(cron="0 6 * * *", timezone="UTC"),
    tags=["production", "etl"],
)

if __name__ == "__main__":
    deployment.apply()
```

---

## Docker Compose Stacks

### Local Development Stack

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Kafka ecosystem
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'

  schema-registry:
    image: confluentinc/cp-schema-registry:7.5.0
    depends_on:
      - kafka
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka:29092

  kafka-connect:
    image: confluentinc/cp-kafka-connect:7.5.0
    depends_on:
      - kafka
      - schema-registry
    ports:
      - "8083:8083"
    environment:
      CONNECT_BOOTSTRAP_SERVERS: kafka:29092
      CONNECT_REST_PORT: 8083
      CONNECT_GROUP_ID: connect-cluster
      CONNECT_CONFIG_STORAGE_TOPIC: connect-configs
      CONNECT_OFFSET_STORAGE_TOPIC: connect-offsets
      CONNECT_STATUS_STORAGE_TOPIC: connect-status
      CONNECT_KEY_CONVERTER: io.confluent.connect.avro.AvroConverter
      CONNECT_KEY_CONVERTER_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      CONNECT_VALUE_CONVERTER: io.confluent.connect.avro.AvroConverter
      CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR: 1
      CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR: 1
      CONNECT_STATUS_STORAGE_REPLICATION_FACTOR: 1
    volumes:
      - ./connectors:/etc/kafka-connect/jars

  # Databases
  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: analytics
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Orchestration
  airflow-webserver:
    image: apache/airflow:2.8.0
    depends_on:
      - postgres
    ports:
      - "8080:8080"
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql://admin:admin@postgres/airflow
      AIRFLOW__CORE__FERNET_KEY: ${FERNET_KEY}
      AIRFLOW__WEBSERVER__SECRET_KEY: ${WEBSERVER_SECRET}
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.8.0
    depends_on:
      - airflow-webserver
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql://admin:admin@postgres/airflow
      AIRFLOW__CORE__FERNET_KEY: ${FERNET_KEY}
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: scheduler

  # MinIO (S3 compatible)
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

  # Monitoring
  prometheus:
    image: prom/prometheus:v2.47.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:10.2.0
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  postgres_data:
  redis_data:
  minio_data:
  prometheus_data:
  grafana_data:
```

---

## Quick Reference

| Component | Template Section |
|-----------|------------------|
| Airflow DAG | [Apache Airflow DAGs](#apache-airflow-dags) |
| Kafka Producer/Consumer | [Apache Kafka Configuration](#apache-kafka-configuration) |
| Spark ETL | [Apache Spark Jobs](#apache-spark-jobs) |
| dbt Models | [dbt Models and Tests](#dbt-models-and-tests) |
| Great Expectations | [Data Quality (Great Expectations)](#data-quality-great-expectations) |
| Soda Checks | [Data Quality (Soda)](#data-quality-soda) |
| Dagster Assets | [Dagster Assets](#dagster-assets) |
| Prefect Flows | [Prefect Flows](#prefect-flows) |
| Docker Compose | [Docker Compose Stacks](#docker-compose-stacks) |
