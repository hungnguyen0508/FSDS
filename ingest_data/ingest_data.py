from sqlalchemy import create_engine, Float, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.dialects.postgresql import insert
from datetime import date
import os
import re
import pandas as pd


DB_URL = "postgresql://postgres:meomeomeo123@localhost:5432/football_db"

# check if the database exists before creating
if not database_exists(DB_URL):
    create_database(DB_URL)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Div: Mapped[str] = mapped_column(String)
    Date: Mapped[date] = mapped_column(nullable=False)
    HomeTeam: Mapped[str] = mapped_column(nullable=False)
    AwayTeam: Mapped[str] = mapped_column(nullable=False)
    FTHG: Mapped[int] = mapped_column(Integer,nullable=False)
    FTAG: Mapped[int] = mapped_column(Integer,nullable=False)
    FTR: Mapped[str] = mapped_column(String(1),nullable=False)
    HTHG: Mapped[int] = mapped_column(Integer,nullable=False)
    HTAG: Mapped[int] = mapped_column(Integer,nullable=False)
    HTR: Mapped[str] = mapped_column(String(1),nullable=True)
    Attendance: Mapped[float] = mapped_column(Float,nullable=True)
    Referee: Mapped[str] = mapped_column(String,nullable=True)
    HS: Mapped[int] = mapped_column(Integer,nullable=True)
    AS: Mapped[int] = mapped_column(Integer,nullable=True)
    HST: Mapped[int] = mapped_column(Integer,nullable=True)
    AST: Mapped[int] = mapped_column(Integer,nullable=True)
    HHW: Mapped[int] = mapped_column(Integer,nullable=True)
    AHW: Mapped[int] = mapped_column(Integer,nullable=True)
    HC: Mapped[int] = mapped_column(Integer,nullable=True)
    AC: Mapped[int] = mapped_column(Integer,nullable=True)
    HF: Mapped[int] = mapped_column(Integer,nullable=True)
    AF: Mapped[int] = mapped_column(Integer,nullable=True)
    HY: Mapped[int] = mapped_column(Integer,nullable=True)
    AY: Mapped[int] = mapped_column(Integer,nullable=True)
    HR: Mapped[int] = mapped_column(Integer,nullable=True)
    AR: Mapped[int] = mapped_column(Integer,nullable=True)

    __table_args__ = (
        UniqueConstraint("Date", "HomeTeam", "AwayTeam", "Div"),)
Base.metadata.create_all(engine)

def date_adjusted(date_column: str) -> date:
    d, m, y = date_column.split("/")
    if len(y) == 2:
        y = int(y) + 2000
    return date(int(y), int(m), int(d))

# load each csv file into postgres 
def data_ingestion(dir: str):
    session = SessionLocal()

    for file in os.listdir(dir):
        if re.match(r"\d{4}-\d{2}\.csv", file): # check condition for each csv. 
            df = pd.read_csv(f"{dir}/{file}") 

            df["Date"] = df["Date"].apply(date_adjusted)

            for _, row in df.iterrows():
                # prepare to insert column
                stmt = insert(Match).values(
                    Div=row.get("Div"),
                    Date=row["Date"],
                    HomeTeam=row["HomeTeam"],
                    AwayTeam=row["AwayTeam"],
                    FTHG=row.get("FTHG"),
                    FTAG=row.get("FTAG"),
                    FTR=row.get("FTR"),
                    HTHG=row.get("HTHG"),
                    HTAG=row.get("HTAG"),
                    HTR=row.get("HTR"),
                    Attendance=row.get("Attendance"),
                    Referee=row.get("Referee"),
                    HS=row.get("HS"),
                    AS=row.get("AS"),
                    HST=row.get("HST"),
                    AST=row.get("AST"),
                    HHW=row.get("HHW"),
                    AHW=row.get("AHW"),
                    HC=row.get("HC"),
                    AC=row.get("AC"),
                    HF=row.get("HF"),
                    AF=row.get("AF"),
                    HY=row.get("HY"),
                    AY=row.get("AY"),
                    HR=row.get("HR"),
                    AR=row.get("AR"),
                )

                # Upsert data. 
                stmt = stmt.on_conflict_do_update(
                    index_elements=["Date", "HomeTeam", "AwayTeam", "Div"],
                    set_={
                        "FTHG": stmt.excluded.FTHG,
                        "FTAG": stmt.excluded.FTAG,
                        "FTR": stmt.excluded.FTR,
                        "HTHG": stmt.excluded.HTHG,
                        "HTAG": stmt.excluded.HTAG,
                        "HTR": stmt.excluded.HTR,
                        "Attendance": stmt.excluded.Attendance,
                        "Referee": stmt.excluded.Referee,
                        "HS": stmt.excluded.HS,
                        "AS": stmt.excluded.AS,
                        "HST": stmt.excluded.HST,
                        "AST": stmt.excluded.AST,
                        "HY": stmt.excluded.HY,
                        "AY": stmt.excluded.AY,
                        "HR": stmt.excluded.HR,
                        "AR": stmt.excluded.AR,
                    }
                )
                session.execute(stmt)


    session.commit()

    session.close()


if __name__ == "__main__":
    data_ingestion("/home/hung-nguyen/Downloads/final_project/raw_data")