{{ config(materialized="view") }}

select 
        {{ dbt_utils.surrogate_key(['country_code', 'ind_code', 'year', 'created_on']) }} as wbid,
        created_on,
        country_name, 
        country_code, 
        ind_name, 
        ind_code, 
        year, 
        value
from {{ source("staging",  "world_bank") }}
where country_name is not null
-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}

