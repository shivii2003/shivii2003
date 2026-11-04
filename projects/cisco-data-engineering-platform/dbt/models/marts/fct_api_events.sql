select
    event_id,
    source_system,
    payload:id::varchar as source_record_id,
    payload:userId::number as user_id,
    payload:title::varchar as event_title,
    ingested_at,
    current_timestamp() as transformed_at
from {{ ref('stg_api_events') }}
