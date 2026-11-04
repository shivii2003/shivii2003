{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
) }}

select
    order_id,
    customer_id,
    product_id,
    order_status,
    order_ts,
    order_amount,
    _loaded_at as source_loaded_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
where _loaded_at > (
    select coalesce(max(source_loaded_at), '1900-01-01'::timestamp_ntz)
    from {{ this }}
)
{% endif %}
