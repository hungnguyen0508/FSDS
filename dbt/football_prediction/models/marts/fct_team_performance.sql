{{ config(materialized='view')}}


select 
    team,
    season,
    avg(full_time_goals) as avg_goals_per_match, 
    sum(full_time_goals) as total_goals, 
    avg(full_times_goals_conceded) as avg_goals_conceded_per_match, 
    sum(full_times_goals_conceded) as total_goals_conceded, 
    sum(match_point) as points_collected, 
    avg(half_time_goals) as avg_goals_half_time, 
    sum(half_time_goals) as total_half_time_goals,
    avg(half_time_goals_conceded) as avg_goals_conceded_half_time, 
    sum(half_time_goals_conceded) as total_goals_conceded_half_time, 
    avg(shots) as avg_shots_per_match, 
    avg(shots_on_target) as avg_shots_on_target_per_match, 
    avg(hit_woodwork) as avg_hit_ww_per_match, 
    avg(corners_taken) as avg_corner_taken_per_match, 
    sum(corners_taken) as total_corners_taken, 
    avg(fouls_committed) as avg_fouls_committed_per_match, 
    sum(fouls_committed) as total_fouls_committed, 
    avg(yellow_cards) as YC_per_match,
    sum(yellow_cards) as total_YC, 
    avg(red_cards) as RC_per_match,
    sum(red_cards) as total_RC
from {{ref('int_fct_team_result')}}
group by team, season