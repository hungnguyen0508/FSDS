{{ config(materialized='table') }}

with distinct_refs as (
    select distinct "Referee"
from {{ ref('stg_match_result') }}
) 
select 
    row_number() over (order by "Referee") as id, 
    "Referee" as referee
    from distinct_refs