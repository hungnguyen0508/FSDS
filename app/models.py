from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


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
    table_args__ = {"schema":"public_gold"}
    team:Mapped[int] = mapped_column(Integer, primary_key=True)
    match_date:Mapped[str] = mapped_column(String)
    goals_for_last_5:Mapped[int] = mapped_column(Integer)
    goals_against_last_5:Mapped[int] = mapped_column(Integer)
    wins_last_5:Mapped[int] = mapped_column(Integer)
    draws_last_5:Mapped[int] = mapped_column(Integer)
    losses_last_5:Mapped[int] = mapped_column(Integer)
    number:Mapped[int] = mapped_column(Integer)
