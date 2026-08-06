select id as match_id
from  {{ ref('stg_match_result') }}
where match_date > current_date 