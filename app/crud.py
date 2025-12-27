from sqlalchemy.orm import Session
from models import SeasonStat, team_recent_form

# read operation to get the stat of a particular season
def get_season(db:Session, season:str): 
    return db.query(SeasonStat).filter(SeasonStat.season == season).first()

# read operation to get the team recent performance
def get_team_recent_form(db:Session, team:int): 
    return db.query(team_recent_form).filter(team_recent_form.team == team).first()
