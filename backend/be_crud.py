from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import Session
from backend.be_models import SeasonStat, TeamRecentForm, Team, BronzeMatchResult, SilverMatchResult
from backend.be_helper_stat import latest_date
from datetime import date, datetime as dt
from backend.be_schema import MatchIdentity, Matchresult
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
def delete_match(db: Session, data: MatchIdentity):
    db_match = (
        db.query(BronzeMatchResult)
        .filter(
            and_(
                BronzeMatchResult.match_date == data.match_date,
                BronzeMatchResult.hometeam == data.home_team,
                BronzeMatchResult.awayteam == data.away_team,
            )
        )
        .first()
    )
    if db_match is None:
        return False, f"Match not found"
    else:
        db.delete(db_match)
        db.commit()
        return True, f"Match deleted successfully"


# update match from source
def update_match(db: Session, data: Matchresult):
    db_match = (
        db.query(BronzeMatchResult)
        .filter(
            and_(
                BronzeMatchResult.match_date == data.match_date,
                BronzeMatchResult.hometeam == data.hometeam,
                BronzeMatchResult.awayteam == data.awayteam,
            )
        )
        .first()
    )
    if db_match is None:
        return False, f"Match not found to update"
    else:
        for key, value in data.model_dump().items():
            setattr(BronzeMatchResult, key, value)
        db.commit()
        return True, "Match updated successfully"


# create new match into source
def create_match(db: Session, data: Matchresult):
    last_date = latest_date(db, data.hometeam, data.awayteam)
    if last_date and last_date < data.match_date:
        new_match = BronzeMatchResult(
            season=data.season,
            div=data.division,
            match_date=data.match_date,
            hometeam=data.hometeam,
            awayteam=data.awayteam,
            fthg=data.fthg,
            ftag=data.ftag,
            ftr=data.ftr,
            hthg=data.hthg,
            htag=data.htag,
            htr=data.htr,
            attendance=data.attendance,
            referee=data.referee,
            hsh=data.hsh,
            ash=data.ash,
            hst=data.hst,
            ast=data.ast,
            hhw=data.hhw,
            ahw=data.ahw,
            hc=data.hc,
            ac=data.ac,
            hf=data.hf,
            af=data.af,
            hy=data.hy,
            ay=data.ay,
            hr=data.hr,
            ar=data.ar,
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return True, new_match
    else:
        return False, f"invalid date"


# read operation to get the stat of a particular season
def get_season(db: Session, season: str):
    return db.query(SeasonStat).filter(SeasonStat.season == season).first()


# read operation to get the team recent performance
def get_team_recent_form(db: Session, team: int):
    return db.query(TeamRecentForm).filter(TeamRecentForm.team == team).first()


def get_team(db: Session):
    return db.query(Team
                    ).all()


def get_head_to_head(db: Session, team1: int, team2: int):
    return (
        db.query(SilverMatchResult)
        .filter(
            and_(
                or_(
                    SilverMatchResult.home_team_id == team1,
                    SilverMatchResult.home_team_id == team2,
                ),
                or_(
                    SilverMatchResult.away_team_id == team1,
                    SilverMatchResult.away_team_id == team2,
                ),
            )
        )
        .order_by(desc(SilverMatchResult.match_date))
        .all()
    )
