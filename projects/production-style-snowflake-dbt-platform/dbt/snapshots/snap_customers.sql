{% snapshot snap_customers %}

{{
    config(
      target_schema='SNAPSHOTS',
      unique_key='customer_id',
      strategy='check',
      check_cols=['customer_name', 'customer_segment', 'customer_region']
    )
}}

select
    customer_id,
    customer_name,
    customer_segment,
    customer_region
from {{ source('raw', 'customers') }}

{% endsnapshot %}
