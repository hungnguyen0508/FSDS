{{ config(materialized='view') }}


select 
    id,
    "season" as season,
    "Div" as division,
    "Date" as match_date,
    trim("HomeTeam") as home_team,
    trim("AwayTeam") as away_team,
    "FTHG" as full_time_home_goals,
    "FTAG" as full_time_away_goals,
    "FTR" as full_time_result,
    "HTHG" as half_time_home_goals,
    "HTAG" as half_time_away_goals,
    "HTR" as half_time_result,
    "Attendance"::float as attendance,
    "Referee",
    "HS" as home_team_shots,
    "AS" as away_team_shots,
    "HST" as home_team_shots_on_target,
    "AST" as away_team_shots_on_target,
    "HHW" as home_team_hit_woodwork,
    "AHW" as away_team_hit_woodwork,
    "HC" as home_team_corners,
    "AC" as away_team_corners,
    "HF" as home_team_fouls_committed,
    "AF" as away_team_fouls_committed,
    "HY" as home_team_yellow_cards,
    "AY" as away_team_yellow_cards,
    "HR" as home_team_red_cards,
    "AR" as away_team_red_cards
from {{ source('football_db', 'matches') }}
