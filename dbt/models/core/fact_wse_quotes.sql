{{ config(materialized='table') }}

with stg_shares_data as (
  select * from {{ ref('stg_wse_shares') }}
),

dim_securities as (

    select * from {{ ref('dim_securities') }}
)


select 
    stg_shares_data.date,
    dim_securities.symbol,
    stg_shares_data.open_price,
    stg_shares_data.max_price,
    stg_shares_data.min_price,
    stg_shares_data.close_price,
    stg_shares_data.change,
    stg_shares_data.volume
from stg_shares_data inner join dim_securities on stg_shares_data.isin = dim_securities.isin