{{ config(materialized='view')}}

select 
    season,
    avg(attendance) as average_spectator, 
    avg(full_time_home_goals) + avg(full_time_away_goals) as average_goals_per_match,
    sum(home_team_yellow_cards) + sum(away_team_yellow_cards) as total_yellow_cards,
    sum(home_team_red_cards) + sum(away_team_red_cards) as total_red_cards,
    avg(home_team_yellow_cards) + avg(away_team_yellow_cards) as yellow_cards_per_match,
    avg(home_team_red_cards) + avg(away_team_red_cards) as red_cards_per_match
from {{ ref('int_fct_match_result')}} 
group by season