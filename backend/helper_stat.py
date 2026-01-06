from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from models import src_match_result, match_result, team
import re 
from datetime import datetime as dt

# calculate the latest season in the table 
# def latest_season(db: Session): 
#    last_season = db.query(func.max(SeasonStat.season)).scalar()
#    return last_season

def latest_date(db:Session, home_team:str, away_team:str): 
    # find the latest game date of home team game
    last_ht_date = db.query(func.max(src_match_result.match_date)).filter(or_
                                                                      (src_match_result.hometeam == home_team,
                                                                       src_match_result.awayteam == home_team)
                                                                    ).first() 
    # find the latest game date of away team game
    last_at_date = db.query(func.max(src_match_result.match_date)).filter(or_
                                                                      (src_match_result.hometeam == away_team,
                                                                       src_match_result.awayteam == away_team)
                                                                    ).first()  
    return max(last_ht_date, last_at_date)[0]




