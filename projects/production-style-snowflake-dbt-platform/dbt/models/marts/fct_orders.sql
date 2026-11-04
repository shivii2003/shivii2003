{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
) }}

select
    order_id,
    customer_id,
    order_status,
    order_timestamp,
    order_amount,
    ingested_at as source_ingested_at,
    loaded_at as warehouse_loaded_at,
    current_timestamp() as transformed_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
-- Use warehouse load time so late-arriving source updates are not skipped.
where loaded_at >= (
    select dateadd(
        minute, -30, coalesce(max(warehouse_loaded_at), '1900-01-01'::timestamp_tz)
    )
    from {{ this }}
)
{% endif %}
