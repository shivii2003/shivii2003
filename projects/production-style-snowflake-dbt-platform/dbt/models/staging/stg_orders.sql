with raw_events as (
    select
        payload:order_id::string as order_id,
        payload:customer_id::string as customer_id,
        payload:order_status::string as order_status,
        try_to_timestamp_tz(payload:order_timestamp::string) as order_timestamp,
        try_to_decimal(payload:order_amount::string, 18, 2) as order_amount,
        ingested_at,
        run_id,
        loaded_at
    from {{ source('raw', 'order_events') }}
),

latest_per_order as (
    select *
    from raw_events
    where order_id is not null
    qualify row_number() over (
        partition by order_id
        order by ingested_at desc, loaded_at desc
    ) = 1
)

select
    order_id,
    customer_id,
    upper(trim(order_status)) as order_status,
    order_timestamp,
    order_amount,
    ingested_at,
    run_id,
    loaded_at
from latest_per_order
