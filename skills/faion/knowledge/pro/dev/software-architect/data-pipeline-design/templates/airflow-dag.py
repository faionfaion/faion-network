"""
Airflow DAG skeleton with:
- Exponential backoff retry configuration
- SLA miss callback
- Idempotent task pattern (watermark-based incremental load)

Adjust SCHEDULE_INTERVAL, retries, and task logic for your pipeline.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

logger = logging.getLogger(__name__)

# --- Default args: applied to every task unless overridden ---
DEFAULT_ARGS = {
    "owner": "data-platform",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["data-alerts@company.com"],
    # Retry configuration: 3 retries, exponential backoff
    # Actual delays: 5min, 10min, 20min (5 * 2^n minutes)
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=60),
    # Timeout: kill task if it runs longer than 2h
    "execution_timeout": timedelta(hours=2),
}


def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Called when a task misses its SLA. Send alert to on-call."""
    logger.error(
        "sla_miss",
        extra={
            "dag_id": dag.dag_id,
            "tasks": [str(t) for t in task_list],
        },
    )
    # Integrate with your alerting system (PagerDuty, Slack, etc.)
    # pagerduty_alert(f"SLA miss: {dag.dag_id}")


with DAG(
    dag_id="incremental_orders_load",
    default_args=DEFAULT_ARGS,
    description="Incremental load of orders from source DB to warehouse",
    schedule_interval="0 * * * *",  # hourly
    start_date=days_ago(1),
    catchup=False,                  # do not run missed intervals on restart
    max_active_runs=1,              # prevent overlapping runs
    tags=["orders", "incremental"],
    sla_miss_callback=sla_miss_callback,
) as dag:

    def extract_incremental(**context) -> dict:
        """
        Idempotent extraction: load records updated since the last successful
        run watermark. Running twice with the same inputs produces the same output.

        The watermark is read from Airflow's XCom (or a dedicated state table).
        If no prior watermark exists, fall back to a safe default (e.g., 24h ago).
        """
        ti = context["ti"]

        # Read watermark from previous successful run
        previous_watermark = ti.xcom_pull(
            task_ids="extract", key="watermark", include_prior_dates=True
        )
        if previous_watermark is None:
            previous_watermark = (
                datetime.utcnow() - timedelta(hours=24)
            ).isoformat()

        logger.info("extract_start", extra={"since": previous_watermark})

        # --- Replace with your source query ---
        # records = source_db.execute(
        #     "SELECT * FROM orders WHERE updated_at > %s",
        #     (previous_watermark,)
        # )
        records = []  # placeholder

        new_watermark = datetime.utcnow().isoformat()
        logger.info("extract_done", extra={"records": len(records)})

        # Push watermark to XCom for the next run
        ti.xcom_push(key="watermark", value=new_watermark)
        return {"record_count": len(records), "watermark": new_watermark}

    def load_to_warehouse(**context) -> None:
        """
        Idempotent load: upsert records by primary key.
        Running this twice with the same payload must produce the same DB state.
        """
        ti = context["ti"]
        extract_result = ti.xcom_pull(task_ids="extract")
        record_count = extract_result.get("record_count", 0)

        logger.info("load_start", extra={"records": record_count})

        # --- Replace with your warehouse upsert ---
        # warehouse.execute(
        #     """
        #     INSERT INTO orders (order_id, ...) VALUES (...)
        #     ON CONFLICT (order_id) DO UPDATE SET ...
        #     """,
        #     records
        # )

        logger.info("load_done")

    def run_dbt_models(**context) -> None:
        """Run dbt models in the staging → intermediate → mart order."""
        import subprocess
        result = subprocess.run(
            ["dbt", "run", "--select", "stg_ecommerce__orders+"],
            capture_output=True,
            text=True,
            check=True,
        )
        logger.info("dbt_run_complete", extra={"stdout": result.stdout[-500:]})

    # --- Task definitions ---

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_incremental,
        sla=timedelta(minutes=30),  # alert if not done within 30min of schedule
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_to_warehouse,
        sla=timedelta(minutes=45),
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=run_dbt_models,
        sla=timedelta(minutes=55),
    )

    # Task dependency chain
    extract >> load >> transform
