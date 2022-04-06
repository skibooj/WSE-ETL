{{ config(materialized = 'table') }} 

WITH stg_shares_data AS (
       SELECT
              *
       FROM
              {{ ref ('stg_wse_shares') }}
),

dim_securities AS (
       SELECT
              *
       FROM
              {{ ref ('dim_securities') }}
)

SELECT
       stg_shares_data.date,
       dim_securities.stock_id,
       stg_shares_data.open_price,
       stg_shares_data.max_price,
       stg_shares_data.min_price,
       stg_shares_data.close_price,
       stg_shares_data.change,
       stg_shares_data.volume
FROM
       stg_shares_data
       INNER JOIN dim_securities ON stg_shares_data.isin = dim_securities.isin

       