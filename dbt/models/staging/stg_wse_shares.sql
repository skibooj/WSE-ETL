{{ config(materialized='view') }}

with wse_data as 
(
  select *,

  from {{ source('staging','wse_shares_external_table') }}

)
select
    cast(Data as timestamp) as date,
    Nazwa as symbol,
    ISIN as isin,
    cast(Kurs_otwarcia as numeric) as open_price,
    cast(Kurs_max as numeric) as max_price,
    cast(Kurs_min as numeric) as min_price,
    cast(Kurs_zamkni_cia as numeric) as close_price,
    cast(Zmiana as numeric) as change,
    cast(Liczba_Transakcji as integer) as num_of_transactions,
    cast(Wolumen as integer) as quantity,
    cast(Obr_t * 1000 as numeric) as volume
  
from wse_data
