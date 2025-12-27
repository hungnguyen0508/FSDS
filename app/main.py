from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, SeasonStat
from crud import get_season, get_team_recent_form
import uvicorn

app = FastAPI()

# Dependency to get DB session
def get_db(): 
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()

@app.get("/") 
async def root(): 
    return f"Welcome to EPL stat"

@app.get("/season") 
async def season(): 
    return f"give me the season you want to get the statistics"

@app.get("/season/{season}")
async def get_season_stat(season:str, db:Session = Depends(get_db)): 
    season_stat = get_season(db, season)
    if season_stat is None: 
        raise HTTPException(status_code = 404, detail = "Season not found")
    return season_stat 

@app.get("/team/recent_performance") 
async def season(): 
    return f"give me the team you want to view recent performance"

@app.get("/team/recent_performance/{team}")
async def get_team_form(team:int, db:Session = Depends(get_db)): 
    team_performance = get_team_form(db, team)
    if team_performance is None: 
        raise HTTPException(status_code = 404, detail = "Team not found")
    return team_performance 
if __name__ == "__main__": 
    uvicorn.run(app, host = "0.0.0.0", port = 8080)