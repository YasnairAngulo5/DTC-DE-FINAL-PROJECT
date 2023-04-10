{{ config(materialized="table") }}

select
    wb.wbid,
    case
        when countries.region is null then wb.country_name
        else countries.region
    end as region,
    wb.country_name,
    wb.country_code,
    wb.ind_name,
    wb.ind_code,
    wb.year,
    wb.value
from {{ ref("stg_world_bank") }} as wb
inner join
    {{ ref("countries") }} as countries on wb.country_code = countries.country_code
