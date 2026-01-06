from pydantic import BaseModel, field_validator
import re 
from datetime import date, datetime as dt 

""" # validation for SeasonStat
class SeasonCreate(BaseModel): 
    season:str
    spectator:float 
    goals_per_match:float
    tot_yc:int # total yellow cards 
    tot_rc:int # total red cards
    yc_per_match: float # average yellow cards per match
    rc_per_match: float # average rec cards per match

    @classmethod
    def validate_season(cls, v): 
        if not re.match(r"\d{4}-\d{2}", v): 
            raise ValueError("Season must be in format yyyy-yy")
        return v  """



# Validate for match result: 
class Matchresult(BaseModel): 
                    season: str
                    division: str
                    match_date: str
                    home_team:str
                    away_team: str
                    fthg: int
                    ftag: int 
                    ftr: str 
                    hthg: int 
                    htag: int 
                    htr: str
                    attendance: float 
                    referee: str
                    hsh: int
                    ash: int 
                    hst: int 
                    ast: int 
                    hhw: int 
                    ahw: int 
                    hc: int 
                    ac: int 
                    hf: int 
                    af: int 
                    hy: int 
                    ay: int 
                    hr: int 
                    ar: int 
                    # Validate date column
                    @field_validator("match_date")
                    @classmethod
                    def validate_match_date(cls, v: str):
                        try:
                            d = dt.strptime(v, "%Y-%m-%d").date()
                        except ValueError:
                            raise ValueError("Date must be in format YYYY-MM-DD")

                        if d > date.today():
                            raise ValueError("Date cannot be in the future")

                        return d

# Validate for del object
class MatchIdentity(BaseModel): 
                    match_date: str
                    home_team: str 
                    away_team: str 
                    # Validate date column
                    @field_validator("match_date")
                    @classmethod
                    def validate_match_date(cls, v: str):
                        try:
                            d = dt.strptime(v, "%Y-%m-%d").date()
                        except ValueError:
                            raise ValueError("Date must be in format YYYY-MM-DD")

                        if d > date.today():
                            raise ValueError("Date cannot be in the future")

                        return d

                            


