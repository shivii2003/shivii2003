select
    customer_id,
    customer_name,
    customer_segment,
    customer_region,
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
    case when dbt_valid_to is null then true else false end as is_current
from {{ ref('snap_customers') }}
