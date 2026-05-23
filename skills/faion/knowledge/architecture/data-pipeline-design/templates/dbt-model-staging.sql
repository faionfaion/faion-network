-- Canonical staging model template: stg_<source>__<entity>.sql
-- Purpose: light transform only — rename, cast, deduplicate.
-- Never reference raw source tables directly from intermediate or mart models.
-- Materialise as view (default) or ephemeral.

{{
  config(
    materialized='view',
    schema='staging',
    tags=['staging', 'orders'],
  )
}}

with source as (

  -- Always reference via source() macro, never raw schema directly.
  -- This creates lineage metadata and lets dbt detect source freshness.
  select * from {{ source('ecommerce', 'orders') }}

),

renamed as (

  select
    -- Primary key: cast to consistent type across all staging models
    cast(id          as bigint)                    as order_id,

    -- Foreign keys
    cast(customer_id as bigint)                    as customer_id,

    -- Business fields: rename to snake_case, apply consistent types
    cast(status      as varchar(50))               as order_status,
    cast(total_cents as integer)                   as amount_cents,
    cast(currency    as char(3))                   as currency_code,

    -- Timestamps: always cast to UTC timestamp
    cast(created_at  as timestamp with time zone)  as created_at,
    cast(updated_at  as timestamp with time zone)  as updated_at,

    -- Source metadata: preserve for lineage and debugging
    _fivetran_synced                               as _ingested_at

  from source

),

-- Deduplication: keep the most recent record per primary key.
-- Required when source produces duplicate rows (CDC, at-least-once delivery).
-- If source guarantees uniqueness, remove this CTE and reference renamed directly.
deduplicated as (

  select
    *,
    row_number() over (
      partition by order_id
      order by updated_at desc, _ingested_at desc
    ) as _row_num

  from renamed

)

select
  -- Exclude deduplication helper column
  order_id,
  customer_id,
  order_status,
  amount_cents,
  currency_code,
  created_at,
  updated_at,
  _ingested_at

from deduplicated
where _row_num = 1

-- Add dbt tests in schema.yml:
-- - not_null: order_id
-- - unique: order_id
-- - accepted_values: order_status in ['pending', 'paid', 'cancelled', 'refunded']
-- - not_null: customer_id
-- - relationships: customer_id references stg_ecommerce__customers.customer_id
