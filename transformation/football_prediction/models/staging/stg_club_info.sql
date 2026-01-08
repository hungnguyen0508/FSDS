{{ config(materialized="table")}}

select 
    team, 
    city,
    stadium,
    founded 
from {{source("football_db", "clubs")}}