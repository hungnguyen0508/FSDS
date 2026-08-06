{{config(materialized='table')}}


select 
    season, 
    match_date,
    home_team_id as team, 
    full_time_home_goals as full_time_goals,
    full_time_away_goals as full_times_goals_conceded, 
    case 
            when full_time_result = 'H' then 3
            when full_time_result = 'D' then 1
            else 0 end as match_point, 
    half_time_home_goals as half_time_goals, 
    half_time_away_goals as half_time_goals_conceded, 
    home_team_shots as shots, 
    home_team_shots_on_target shots_on_target, 
    home_team_hit_woodwork as hit_woodwork, 
    home_team_corners as corners_taken, 
    home_team_fouls_committed as fouls_committed, 
    home_team_yellow_cards as yellow_cards, 
    home_team_red_cards as red_cards       
from {{ ref('int_fct_match_result')}}
union
select 
    season, 
    match_date,
    away_team_id as team, 
    full_time_away_goals as full_time_goals,
    full_time_home_goals as full_times_goals_conceded, 
    case 
            when full_time_result = 'A' then 3
            when full_time_result = 'D' then 1
            else 0 end as match_point, 
    half_time_away_goals as half_time_goals, 
    half_time_home_goals as half_time_goals_conceded, 
    away_team_shots as shots, 
    away_team_shots_on_target shots_on_target, 
    away_team_hit_woodwork as hit_woodwork, 
    away_team_corners as corners_taken, 
    away_team_fouls_committed as fouls_committed, 
    away_team_yellow_cards as yellow_cards, 
    away_team_red_cards as red_cards       
from {{ ref('int_fct_match_result')}}