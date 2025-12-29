from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import Session
from models import SeasonStat, team_recent_form,team,match_result

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
