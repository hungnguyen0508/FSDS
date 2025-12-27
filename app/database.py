from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#database url 
db_url = "postgresql://postgres:meomeomeo123@localhost:5432/football_db"

#engine and session
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind = engine, autoflush=False)

# base 
Base = declarative_base()