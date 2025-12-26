{{ config(materialized='table') }}
    
select 
                    m.id,
                    m.season, 
                    m.division,
                    m.match_date,
                    t.id as home_team_id, 
                    t2.id as away_team_id,
                    m.full_time_home_goals,
                    m.full_time_away_goals,
                    m.full_time_result,
                    m.half_time_home_goals,
                    m.half_time_away_goals,
                    m.half_time_result,
                    m.attendance::float,
                    r.id as referee_id,
                    home_team_shots,
                    away_team_shots,
                    home_team_shots_on_target,
                    away_team_shots_on_target,
                    home_team_hit_woodwork,
                    away_team_hit_woodwork,
                    home_team_corners,
                    away_team_corners,
                    home_team_fouls_committed,
                    away_team_fouls_committed,
                    home_team_yellow_cards,
                    away_team_yellow_cards,
                    home_team_red_cards,
                    away_team_red_cards


from {{ ref('stg_match_result') }} m 
join {{ ref('int_dim_referees')}} r on m."Referee" = r.referee
join {{ ref('int_dim_teams')}} t on m.home_team = t.team
join {{ ref('int_dim_teams')}} t2 on m.away_team = t2.team
 