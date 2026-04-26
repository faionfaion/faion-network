-- models/marts/growth/cohort_retention_weekly.sql
-- dbt incremental model: weekly cohort retention
-- Compatible with BigQuery (DATE_DIFF) and Snowflake/Redshift (DATEDIFF) — pick per engine
-- Partition: cohort_week | Cluster: user_id | Unique key: cohort_week + day_offset + user_id

{{ config(
    materialized='incremental',
    unique_key=['cohort_week', 'day_offset', 'user_id'],
    partition_by={'field': 'cohort_week', 'data_type': 'date'},
    cluster_by=['user_id']
) }}

WITH users AS (
  SELECT user_id,
         CAST(DATE_TRUNC(DATE(signup_ts_utc), WEEK(MONDAY)) AS DATE) AS cohort_week,
         signup_ts_utc
    FROM {{ ref('stg_users') }}
    {% if is_incremental() %}
      WHERE signup_ts_utc >= (SELECT MAX(signup_ts_utc) FROM {{ this }}) - INTERVAL 90 DAY
    {% endif %}
),
events AS (
  SELECT user_id, event_ts_utc
    FROM {{ ref('stg_events') }}
   WHERE event_type = 'login'   -- replace with your retention metric; document here
)
SELECT u.cohort_week,
       u.user_id,
       -- BigQuery syntax; for Snowflake/Redshift: DATEDIFF(day, DATE(u.signup_ts_utc), DATE(e.event_ts_utc))
       DATE_DIFF(DATE(e.event_ts_utc), DATE(u.signup_ts_utc), DAY) AS day_offset
  FROM users u
  JOIN events e USING (user_id)
 WHERE e.event_ts_utc >= u.signup_ts_utc
   AND DATE_DIFF(DATE(e.event_ts_utc), DATE(u.signup_ts_utc), DAY) IN (1, 7, 14, 30, 60, 90)
