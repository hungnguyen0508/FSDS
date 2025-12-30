from pydantic import BaseModel


# validation for SeasonStat
class SeasonStat(BaseModel): 
    season:str
    average_spectator:float 
    average_goals_per_match:float
    otal_yellow_cards:int
    total_red_cards:int
    yellow_cards_per_match: float
    red_cards_per_match: float


