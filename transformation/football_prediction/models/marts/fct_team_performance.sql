{{ config(materialized='view')}}


select 
    t.team,
    r.season,
    avg(r.full_time_goals) as avg_goals_per_match, 
    sum(r.full_time_goals) as total_goals, 
    avg(r.full_times_goals_conceded) as avg_goals_conceded_per_match, 
    sum(r.full_times_goals_conceded) as total_goals_conceded, 
    sum(r.match_point) as points_collected, 
    avg(r.half_time_goals) as avg_goals_half_time, 
    sum(r.half_time_goals) as total_half_time_goals,
    avg(r.half_time_goals_conceded) as avg_goals_conceded_half_time, 
    sum(r.half_time_goals_conceded) as total_goals_conceded_half_time, 
    avg(r.shots) as avg_shots_per_match, 
    avg(r.shots_on_target) as avg_shots_on_target_per_match, 
    avg(r.hit_woodwork) as avg_hit_ww_per_match, 
    avg(r.corners_taken) as avg_corner_taken_per_match, 
    sum(r.corners_taken) as total_corners_taken, 
    avg(r.fouls_committed) as avg_fouls_committed_per_match, 
    sum(r.fouls_committed) as total_fouls_committed, 
    avg(r.yellow_cards) as YC_per_match,
    sum(r.yellow_cards) as total_YC, 
    avg(r.red_cards) as RC_per_match,
    sum(r.red_cards) as total_RC
from {{ref('int_fct_team_result')}} r 
join {{ref('int_dim_teams')}} t
on r.team = t.id
group by t.team, r.season