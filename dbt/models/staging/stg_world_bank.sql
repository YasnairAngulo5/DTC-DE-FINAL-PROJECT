{{ config(materialized="view") }}

select 
        country_code || '-' || ind_code || '-' || year as wbid,
        country_name, 
        country_code, 
        ind_name, 
        ind_code, 
        year, 
        value
from {{ source("staging",  "world_bank") }}
-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}

