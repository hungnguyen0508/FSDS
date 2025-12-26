{{ config(materialized='table') }}

with distinct_teams as (
    select distinct home_team
from {{ ref('stg_match_result') }}
) 
select 
    row_number() over (order by home_team) as id, 
    home_team as team
    from distinct_teams