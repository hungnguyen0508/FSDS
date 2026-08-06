from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.be_database import SessionLocal, engine
from backend.be_models import Base
from backend.be_schema import Matchresult, MatchIdentity
from backend.be_crud import (
    get_season,
    get_team_recent_form,
    get_team,
    get_head_to_head,
    create_match,
    delete_match,
    update_match,
)
from datetime import datetime, timezone
import logging
from logging.config import dictConfig
import sys
import json
import uvicorn

RESERVED_ATTRS = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process"
}
# -------------------------------
# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        } 
        extra_fields = {
            key: value
            for key, value in record.__dict__.items()
            if key not in RESERVED_ATTRS
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


# Define the logging configuration
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": JsonFormatter}},
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
            "mode": "a",
        },
    },
    "loggers": {
        "app": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": False},
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
}
# Apply the configuration
dictConfig(log_config)

# create a logger instance
logger = logging.getLogger("app")
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
def root():
    logger.info("Root endpoint accessed")
    return {"message": f"Welcome to EPL stat"}


# Create historic match result
@app.post("/match_result/", status_code=201)
def post_result(post_obj: Matchresult, db: Session = Depends(get_db)):
    logger.info("Match result created for %s", post_obj.match_date)
    success, result = create_match(db, post_obj)
    if success:
        logger.info(
            "Match was created successfully between %s vs %s on %s",
            post_obj.home_team, 
            post_obj.away_team, 
            post_obj.match_date,
            ) 

        return {
            "message": result,
        }
    raise HTTPException(status_code=400, detail=result)


# Delete historic match result
@app.delete("/match_result/", status_code=204)
def del_match(del_obj: MatchIdentity, db: Session = Depends(get_db)):
    logger.info("Delete match on %s between %s vs %s", 
            del_obj.match_date, 
            del_obj.home_team, 
            del_obj.away_team,
            ) 
    success, result = delete_match(db, del_obj)
    if success:
        logger.info("Successfully deleted match on %s between %s vs %s", 
            del_obj.match_date, 
            del_obj.home_team, 
            del_obj.away_team,
            ) 
        return {"message": result}
    raise HTTPException(status_code=400, detail=result)


# Update historic match result
@app.put("/match_result/", status_code=201)
def put_match(put_obj: Matchresult, db: Session = Depends(get_db)):
    logger.info(
        "Update match on %s between %s vs %s",
            put_obj.match_date,
            put_obj.home_team,
            put_obj.away_team,
    )
    success, result = update_match(db, put_obj)
    if success:
        logger.info(
            "Successfully updated match on %s between %s vs %s",
                put_obj.match_date,
                put_obj.home_team,
                put_obj.away_team,
        )
        return {"message": result}
    raise HTTPException(status_code=400, detail=result)


# season stats
@app.get("/season/{season}")
def season_stat(season: str, db: Session = Depends(get_db)):
    logger.info("Season data requested for season %s", season)
    season_stat = get_season(db, season)
    if season_stat is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return season_stat


# routing to /team/recent_performance
@app.get("/team/recent_performance")
def season(db: Session = Depends(get_db)):
    logger.info("list all teams")
    return get_team(db)


# team recent performance
@app.get("/team/recent_performance/{team}")
def team_form(team: str, db: Session = Depends(get_db)):
    logger.info("Performance data requested for %s", team,)
    team_performance = get_team_recent_form(db, team)
    if team_performance is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_performance


# head to head
@app.get("/team/head_to_head")
def head_to_head(first_team: int, second_team: int, db: Session = Depends(get_db)):
    logger.info("Head to head data for %s", 
                 first_team,
                 second_team,)
    h2h = get_head_to_head(db, first_team, second_team)
    if h2h is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return h2h


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
