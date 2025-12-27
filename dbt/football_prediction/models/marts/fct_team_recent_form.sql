{{config(materialized='view')}}

with 
latest_year as (select max(season) as season from {{ref('int_fct_team_result')}}), 
rolling_form as (

    select
        team,
        season,
        match_date,

        count(*) over w as matches_last_5,
        sum(full_time_goals) over w as goals_for_last_5,
        sum(full_times_goals_conceded) over w as goals_against_last_5,

        sum(case when match_point = 3 then 1 else 0 end) over w as wins_last_5,
        sum(case when match_point = 1 then 1 else 0 end) over w as draws_last_5,
        sum(case when match_point = 0 then 1 else 0 end) over w as losses_last_5

    from {{ref('int_fct_team_result')}}
	where season = (select max(season) from latest_year)
    window w as (
        partition by team, season
        order by match_date asc
        rows between 4 preceding and current row
    )

), 
latest_form as (
select 	team,
	match_date,
	goals_for_last_5, 
	goals_against_last_5, 
	wins_last_5, 
	draws_last_5,
	losses_last_5,
	row_number() over (partition by team order by match_date desc) as number
from rolling_form
where matches_last_5 = 5
)
select * from latest_form
where number = 1