{{ config(materialized='table') }}

with stg_shares_data as (
    select *,
    'shares' as security_type
    from {{ ref('stg_wse_shares') }}
)

select * from stg_shares_data