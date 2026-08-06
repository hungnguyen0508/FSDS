select id as match_id
from  {{ ref('stg_match_result') }}
where away_team_red_cards >= 4 or home_team_red_cards >= 4
