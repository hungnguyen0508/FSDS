{{ config(materialized='table') }}

with distinct_teams as (
    select distinct home_team as team
from {{ ref('stg_match_result') }} 
) 
select 
    row_number() over (order by t.team) as id, 
    t.team as team,
    c.city,
    c.stadium,
    c.founded  
    from distinct_teams t 
    join {{ ref('stg_club_info') }} c
    on t.team = c.team
