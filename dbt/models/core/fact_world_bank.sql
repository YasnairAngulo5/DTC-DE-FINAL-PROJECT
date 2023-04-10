{{ config(materialized="table") }}
select
    wb.wbid,
    wb.created_on,
    countries.region,
    wb.country_name,
    wb.country_code,
    wb.ind_name,
    wb.ind_code,
    wb.year,
    wb.value
from (
    select 
        *,
        ROW_NUMBER() OVER (PARTITION BY country_code, ind_code, year ORDER BY created_on DESC) as rn
    from {{ ref("stg_world_bank") }}
    where country_name is not null
) as wb
inner join
    {{ ref("countries") }} as countries on wb.country_code = countries.country_code
where wb.year between ( select max(year) - 10 from {{ ref("stg_world_bank") }} ) and ( select max(year) from {{ ref("stg_world_bank") }})
  and countries.region is not null
  and wb.rn = 1



