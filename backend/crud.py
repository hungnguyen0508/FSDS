from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import Session
from models import SeasonStat, team_recent_form, team, src_match_result, match_result
from helper_stat import latest_date
from datetime import date, datetime as dt
import re 

""" # Create a stat in season stat talbe 
def create_season(db:Session,data:dict):
    last_season = latest_season(db)
    if last_season and last_season < data.season: # only create new season
        new_season = SeasonStat(season = data.season, 
                                average_spectator = data.spectator, 
                                average_goals_per_match = data.goals_per_match, 
                                total_yellow_cards = data.tot_yc, 
                                total_red_cards = data.tot_rc, 
                                yellow_cards_per_match = data.yc_per_match, 
                                red_cards_per_match = data.rc_per_match)
        db.add(new_season)
        db.commit()
        db.refresh(new_season)
        return True, new_season
    else: 

        return False """

# delete match result from source
def delete_match(db:Session, data:dict): 
    db_match = db.query(src_match_result).filter(
                                            and_(
                                            src_match_result.match_date == data.match_date,
                                            src_match_result.hometeam == data.home_team,
                                            src_match_result.awayteam == data.away_team
                                        )).first()
    if db_match is None: 
        return False, f"Match not found"
    else: 
        db.delete(db_match)
        db.commit()
        return True, f"Match deleted successfully"
    
# update match from source
def update_match(db:Session, data:dict): 
    db_match = db.query(src_match_result).filter(
                                            and_(
                                            src_match_result.match_date == data.match_date,
                                            src_match_result.hometeam == data.home_team,
                                            src_match_result.awayteam == data.away_team
                                        )).first()
    if db_match is None: 
        return False, f"Match not found to update"
    else: 
        db_match.fthg = data.fthg
        db_match.ftag = data.ftag
        db_match.ftr = data.ftr
        db_match.hthg = data.hthg
        db_match.htag = data.htag
        db_match.htr = data.htr
        db_match.attendance = data.attendance
        db_match.referee = data.referee
        db_match.hsh = data.hsh
        db_match.ash = data.ash
        db_match.hst = data.hst 
        db_match.ast = data.ast 
        db_match.hhw = data.hhw
        db_match.ahw = data.ahw
        db_match.hc = data.hc
        db_match.ac = data.ac
        db_match.hf = data.hf
        db_match.af = data.af
        db_match.hy = data.hy
        db_match.ay = data.ay
        db_match.hr = data.hr 
        db_match.ar = data.ar 
        db.commit()
        return True, "Match updated successfully"

# create new match into source
def create_match(db:Session, data:dict):
    last_date = latest_date(db, data.home_team, data.away_team)
    if last_date and last_date < data.match_date: 
        new_match = src_match_result(
            season = data.season,
            div = data.division,
            match_date =  data.match_date, 
            hometeam =  data.home_team,
            awayteam =  data.away_team,
            fthg =  data.fthg,
            ftag =  data.ftag,
            ftr = data.ftr,  
            hthg = data.hthg, 
            htag = data.htag, 
            htr = data.htr, 
            attendance = data.attendance,
            referee = data.referee, 
            hsh = data.hsh, 
            ash = data.ash, 
            hst = data.hst, 
            ast = data.ast, 
            hhw = data.hhw, 
            ahw = data.ahw, 
            hc = data.hc, 
            ac = data.ac, 
            hf = data.hf, 
            af = data.af, 
            hy = data.hy, 
            ay = data.ay, 
            hr = data.hr, 
            ar = data.ar         
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return True, new_match
    else: 
        return False, f"invalid date"




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
