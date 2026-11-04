{{ config(materialized='view') }}

select
    event_id,
    order_id,
    customer_id,
    event_type,
    amount,
    upper(currency) as currency,
    event_timestamp,
    ingested_at
from {{ source('raw', 'order_events') }}
where event_id is not null
  and order_id is not null
