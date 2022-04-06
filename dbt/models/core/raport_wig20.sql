{{ config(materialized = 'table') }} 

with fact_data as (
  select
    *
  from
    {{ ref('fact_wse_quotes') }}
),

dim_indexes as (
  select
    *
  from
    {{ ref('dim_indexes') }}
)



select
  dim_indexes.symbol,
  fact_data.date,
  fact_data.open_price,
  fact_data.close_price,
  fact_data.change
from
  fact_data
  inner join dim_indexes on dim_indexes.isin = fact_data.isin
where
  dim_indexes.stock_index = "WIG20"
  and fact_data.date = 
  (
    select date from fact_data order by date desc limit 1
  )