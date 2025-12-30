from sqlalchemy import func
from sqlalchemy.orm import Session
from models import SeasonStat
import re 

# calculate the latest season in the table 
def latest_season(db: Session): 
    last_season = db.query(func.max(SeasonStat.season)).scalar()
    return last_season
