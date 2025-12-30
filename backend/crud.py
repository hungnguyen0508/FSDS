from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import Session
from models import SeasonStat, team_recent_form,team,match_result
from helper_stat import latest_season
import re 

# Create a stat in season stat talbe 
def create_season(db:Session,season:str, spectator:float, goals_per_match: float, tot_yc:int, tot_rc:int, yc_per_match:float, rc_per_match:float):
    last_season = latest_season(db)
    if re.match(r"\d{4}-\d{2}", season) and last_season < season: # only create new season
        new_season = SeasonStat(season = season, average_spectator = spectator, average_goals_per_match = goals_per_match, total_yellow_cards = tot_yc, total_red_cards = tot_rc, yellow_cards_per_match = yc_per_match, red_cards_per_match = rc_per_match)
        db.add(new_season)
        db.commit()
        db.refresh(SeasonStat)
        return True
    else: 

        return {last_season}


# read operation to get the stat of a particular season
def get_season(db:Session, season:str): 
    return db.query(SeasonStat).filter(SeasonStat.season == season).first()

# read operation to get the team recent performance
def get_team_recent_form(db:Session, team:int): 
    return db.query(team_recent_form).filter(team_recent_form.team == team).first()

def get_team(db:Session): 
    return db.query(team).all()

def get_head_to_head(db:Session, team1:int, team2:int): 
    return (
        db.query(match_result)
        .filter(
            and_(
                or_(
                    match_result.home_team_id == team1,
                    match_result.home_team_id == team2
                ),
                or_(
                    match_result.away_team_id == team1,
                    match_result.away_team_id == team2
                )
            )
        )
        .order_by(desc(match_result.match_date))
        .all()
)
