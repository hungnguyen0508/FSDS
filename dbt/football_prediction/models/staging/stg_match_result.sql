{{ config(materialized='incremental',unique_key = [""]) }}


select 
    id,
    "season" as season,
    "div" as division,
    "match_date" as match_date,
    trim("hometeam") as home_team,
    trim("awayteam") as away_team,
    "fthg" as full_time_home_goals,
    "ftag" as full_time_away_goals,
    "ftr" as full_time_result,
    "hthg" as half_time_home_goals,
    "htag" as half_time_away_goals,
    "htr" as half_time_result,
    "attendance"::float as attendance,
    "referee",
    "hsh" as home_team_shots,
    "ash" as away_team_shots,
    "hst" as home_team_shots_on_target,
    "ast" as away_team_shots_on_target,
    "hhw" as home_team_hit_woodwork,
    "ahw" as away_team_hit_woodwork,
    "hc" as home_team_corners,
    "ac" as away_team_corners,
    "hf" as home_team_fouls_committed,
    "af" as away_team_fouls_committed,
    "hy" as home_team_yellow_cards,
    "ay" as away_team_yellow_cards,
    "hr" as home_team_red_cards,
    "ar" as away_team_red_cards
from {{ source('football_db', 'matches') }}
