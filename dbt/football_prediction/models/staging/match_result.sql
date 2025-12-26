{{ config(materialized='view') }}


select 
from {{ source('football_db', 'matches') }}