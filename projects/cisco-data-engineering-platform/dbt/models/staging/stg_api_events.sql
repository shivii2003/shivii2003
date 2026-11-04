with source_data as (
    select
        event_id,
        source_system,
        payload,
        ingested_at
    from {{ source('raw', 'api_events') }}
),
deduplicated as (
    select
        *,
        row_number() over (
            partition by event_id
            order by ingested_at desc
        ) as row_num
    from source_data
)
select
    event_id,
    source_system,
    payload,
    ingested_at
from deduplicated
where row_num = 1
