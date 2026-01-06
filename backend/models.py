from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import date

# create SeasonStat class aka table based on Base. 
class SeasonStat(Base): 
    __tablename__ = "fct_season_stats"
    __table_args__ = {"schema":"public_gold"}
    season:Mapped[str]=mapped_column(String, primary_key=True)
    average_spectator:Mapped[float]=mapped_column(Float)
    average_goals_per_match:Mapped[str]=mapped_column(Float)
    total_yellow_cards:Mapped[int]=mapped_column(Integer)
    total_red_cards:Mapped[int]=mapped_column(Integer)
    yellow_cards_per_match:Mapped[float]=mapped_column(Float)
    red_cards_per_match:Mapped[str]=mapped_column(Float)

# create team_recent_form class aka table based on Base. 
class team_recent_form(Base): 
    __tablename__ = "fct_team_recent_form"
    __table_args__ = {"schema":"public_gold"}
    team:Mapped[str] = mapped_column(String, primary_key=True)
    latest_match_date: Mapped[date] = mapped_column(nullable=False)
    goals_for_last_5:Mapped[int] = mapped_column(Integer)
    goals_against_last_5:Mapped[int] = mapped_column(Integer)
    wins_last_5:Mapped[int] = mapped_column(Integer)
    draws_last_5:Mapped[int] = mapped_column(Integer)
    losses_last_5:Mapped[int] = mapped_column(Integer)
    number:Mapped[int] = mapped_column(Integer)

# team information
class team(Base): 
    __tablename__ = "int_dim_teams"
    __table_args__ = {"schema":"public_silver"}
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    team:Mapped[str]=mapped_column(String)
    city:Mapped[str]=mapped_column(String)
    stadium:Mapped[str]=mapped_column(String)
    founded:Mapped[str]=mapped_column(String)




# source
class src_match_result(Base): 
    __tablename__ = "matches"
    __table_args__ = {"schema":"public"}
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season: Mapped[str] = mapped_column(String, nullable = False)
    div: Mapped[str] = mapped_column(String, nullable = True)
    match_date: Mapped[date] = mapped_column(Date, nullable=False)
    hometeam: Mapped[str] = mapped_column(String, nullable=False)
    awayteam: Mapped[str] = mapped_column(String, nullable=False)
    fthg: Mapped[str] = mapped_column(String, nullable=False)
    ftag: Mapped[str] = mapped_column(String, nullable=False)
    ftr: Mapped[str] = mapped_column(String(1), nullable=False)
    hthg: Mapped[int] = mapped_column(Integer, nullable=False)
    htag: Mapped[int] = mapped_column(Integer, nullable=False)
    htr: Mapped[str] = mapped_column(String(1), nullable=True)
    attendance: Mapped[float] = mapped_column(Float, nullable=True)
    referee: Mapped[str] = mapped_column(String, nullable=True)
    hsh: Mapped[int] = mapped_column(Integer, nullable=True)
    ash: Mapped[int] = mapped_column(Integer, nullable=True)  
    hst: Mapped[int] = mapped_column(Integer, nullable=True)
    ast: Mapped[int] = mapped_column(Integer, nullable=True)
    hhw: Mapped[int] = mapped_column(Integer, nullable=True)
    ahw: Mapped[int] = mapped_column(Integer, nullable=True)
    hc: Mapped[int] = mapped_column(Integer, nullable=True)
    ac: Mapped[int] = mapped_column(Integer, nullable=True)
    hf: Mapped[int] = mapped_column(Integer, nullable=True)
    af: Mapped[int] = mapped_column(Integer, nullable=True)
    hy: Mapped[int] = mapped_column(Integer, nullable=True)
    ay: Mapped[int] = mapped_column(Integer, nullable=True)
    hr: Mapped[int] = mapped_column(Integer, nullable=True)
    ar: Mapped[int] = mapped_column(Integer, nullable=True)


# head to head 
class match_result(Base): 
    __tablename__ = "int_fct_match_result"
    __table_args__ = {"schema":"public_silver"}
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season: Mapped[str] = mapped_column(String)
    division: Mapped[str] = mapped_column(String)
    match_date: Mapped[date] = mapped_column(nullable=False)
    home_team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    away_team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    full_time_home_goals: Mapped[int] = mapped_column(Integer, nullable=False)
    full_time_away_goals: Mapped[int] = mapped_column(Integer, nullable=False)
    full_time_result: Mapped[str] = mapped_column(String(1), nullable=False)
    half_time_home_goals: Mapped[int] = mapped_column(Integer, nullable=False)
    half_time_away_goals: Mapped[int] = mapped_column(Integer, nullable=False)
    half_time_result: Mapped[str] = mapped_column(String(1), nullable=True)
    attendance: Mapped[float] = mapped_column(Float, nullable=True)
    referee_id: Mapped[int] = mapped_column(Integer, nullable=True)
    home_team_shots: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_shots: Mapped[int] = mapped_column(Integer, nullable=True)  # 'as' là từ khóa SQL
    home_team_shots_on_target: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_shots_on_target: Mapped[int] = mapped_column(Integer, nullable=True)
    home_team_hit_woodwork: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_hit_woodwork: Mapped[int] = mapped_column(Integer, nullable=True)
    home_team_corners: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_corners: Mapped[int] = mapped_column(Integer, nullable=True)
    home_team_fouls_committed: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_fouls_committed: Mapped[int] = mapped_column(Integer, nullable=True)
    home_team_yellow_cards: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_yellow_cards: Mapped[int] = mapped_column(Integer, nullable=True)
    home_team_red_cards: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_red_cards: Mapped[int] = mapped_column(Integer, nullable=True)




