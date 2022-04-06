{{ config(materialized = 'table') }} 

with stg_shares_data as (
    SELECT
        distinct isin,
        symbol,
        "shares" as security_type
    FROM
        {{ ref('stg_wse_shares') }}
    group by
        isin,
        symbol,
        security_type
),

update_symbol as (
    select distinct isin, max(date) from {{ ref('stg_wse_shares') }}
    group by isin
)


select
    ROW_NUMBER() OVER() AS stock_id,
    *
from
    stg_shares_data

