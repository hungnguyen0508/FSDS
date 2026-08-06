{{ config(materialized='table') }}

with distinct_refs as (
    select distinct "referee"
from {{ ref('stg_match_result') }}
) 
select 
    row_number() over (order by "referee") as id, 
    "referee" as referee
    from distinct_refs