with dim_securities as (

    select * from {{ ref('dim_securities') }}
)


select
    symbol,
    isin,
    "WIG20" AS stock_index,
    from dim_securities
    where isin in
    (
        'PLSOFTB00016',
        'PLBRE0000012',
        'PLBZ00000044',
        'PLCCC0000016',
        'PLKGHM000017',
        'PLLOTOS00025',
        'PLLPP0000011',
        'PLOPTTC00011',
        'PLPEKAO00016',
        'PLPGNIG00014',
        'PLPKN0000018',
        'PLPKO0000016',
        'PLTLKPL00017',
        'PLCFRPT00013',
        'PLPGER000010',
        'PLPZU0000011',
        'PLJSW0000015',
        'PLDINPL00011',
        'LU2237380790',
        'NL0015000AU7'
    )