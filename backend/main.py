from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from schema import Matchresult, MatchIdentity
from crud import get_season, get_team_recent_form, get_team, get_head_to_head, create_match, delete_match
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


# Update historic match result
@app.post("/match_result/",status_code = 201)
async def match_result(post_obj:Matchresult, db:Session = Depends(get_db)): 
        logger.info(f"Match result created for date {post_obj.match_date}")
        success, result = create_match(db, post_obj)
        if success: 
            logger.info(f"Match was created successfully between {post_obj.home_team} vs {post_obj.away_team} on {post_obj.match_date}")
            return {
                "message": result, 
            }   
        raise HTTPException(status_code = 400, detail = result)     


# Delete historic match result
@app.delete("/match_result/",status_code = 204)
async def del_match(del_obj : MatchIdentity, db:Session = Depends(get_db)): 
    logger.info(f"Delete match on {del_obj.match_date} between {del_obj.home_team} vs {del_obj.away_team}")
    success, result = delete_match(db, del_obj)
    if success: 
        logger.info(f"Successfully deleted match on {del_obj.match_date} between {del_obj.home_team} vs {del_obj.away_team}")
        return {"message": result}
    raise HTTPException(status_code=400, detail = result)


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