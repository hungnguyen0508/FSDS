from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, SeasonStat
from crud import get_season, get_team_recent_form, get_team, get_head_to_head, create_season
from datetime import datetime 
import logging
from logging.config import dictConfig
import sys
import json 
import uvicorn

#-------------------------------
# Custom JSON formatter
class JsonFormatter(logging.Formatter): 
    def format(self, record): 
        log_record = {
            "timestamp": datetime.utcnow().isoformat(), 
            "level": record.levelname, 
            "logger": record.name, 
            "module": record.module, 
            "line": record.lineno, 
            "message": record.getMessage()
        }
        if record.exc_info: 
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)
# Define the logging configuration
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()":JsonFormatter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": "fastapi.log",
            "mode": "a"
        }
    },
    "loggers": {
        "app": {"handlers": ["console","file"], "level": "DEBUG", "propagate": False},
    },
    "root": {"handlers": ["console"], "level": "DEBUG"}
}

# create a logger instance
logger = logging.getLogger("app")

# Apply the configuration
dictConfig(log_config)
# ------------------------------

app = FastAPI()

# Dependency to get DB session
def get_db(): 
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()

# first browse
@app.get("/") 
async def root(): 
    logger.info("Root endpoint accessed")
    return {"message": f"Welcome to EPL stat"}


# updating season stats
@app.post("/season/", status_code=201)
async def create_stat(season:str, spectator:float, goals_per_match: float, tot_yc:int, tot_rc:int, yc_per_match:float, rc_per_match:float,db:Session = Depends(get_db)): 
    logger.info("Season data updated for season {season}")
    result =  create_season(db, season, spectator, goals_per_match, tot_yc, tot_rc, yc_per_match, rc_per_match)
    if result is True: 
        return True
    else: 
        raise HTTPException(status_code=404, detail = f"Wrong input for season {result}")

# season stats
@app.get("/season/{season}")
async def season_stat(season:str, db:Session = Depends(get_db)): 
    logger.info(f"Season data requested for season {season}")
    season_stat = get_season(db, season)
    if season_stat is None: 
        raise HTTPException(status_code = 404, detail = "Season not found")
    return season_stat 

# routing to /team/recent_performance
@app.get("/team/recent_performance") 
async def season(db:Session=Depends(get_db)): 
    logger.info("list all teams")
    return get_team(db)

# team recent performance
@app.get("/team/recent_performance/{team}")
async def team_form(team:str, db:Session = Depends(get_db)): 
    logger.info(f"Performance data requested for team {team}")
    team_performance = get_team_recent_form(db, team)
    if team_performance is None: 
        raise HTTPException(status_code = 404, detail = "Team not found")
    return team_performance 

# head to head
@app.get("/team/head_to_head")
async def head_to_head(first_team: int, second_team:int, db:Session = Depends(get_db)): 
    logger.info(f"Head to head data for {first_team} and {second_team}")
    h2h = get_head_to_head(db, first_team, second_team)
    if h2h is None: 
        raise HTTPException(status_code = 404, detail = "Team not found")
    return h2h

if __name__ == "__main__": 
    uvicorn.run(app, host = "0.0.0.0", port = 8080)