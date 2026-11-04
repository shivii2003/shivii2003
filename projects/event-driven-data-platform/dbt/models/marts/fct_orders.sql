{{ config(
    materialized='incremental',
    unique_key='event_id',
    incremental_strategy='merge'
) }}

select
    event_id,
    order_id,
    customer_id,
    event_type,
    amount,
    currency,
    event_timestamp,
    ingested_at
from {{ ref('stg_order_events') }}

{% if is_incremental() %}
where ingested_at >= (
    select coalesce(dateadd(hour, -2, max(ingested_at)), '1900-01-01'::timestamp_tz)
    from {{ this }}
)
{% endif %}
