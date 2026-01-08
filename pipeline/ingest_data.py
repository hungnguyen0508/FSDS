from sqlalchemy import create_engine, Float, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.dialects.postgresql import insert
from datetime import date
import os
import re
import pandas as pd


DB_URL = os.getenv("Database_URL","postgresql://postgres:meomeomeo123@localhost:5432/football_db")

# check if the database exists before creating
if not database_exists(DB_URL):
    create_database(DB_URL)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season: Mapped[str] = mapped_column(String)
    div: Mapped[str] = mapped_column(String)
    match_date: Mapped[date] = mapped_column(nullable=False)
    hometeam: Mapped[str] = mapped_column(String, nullable=False)
    awayteam: Mapped[str] = mapped_column(String, nullable=False)
    fthg: Mapped[int] = mapped_column(Integer, nullable=False)
    ftag: Mapped[int] = mapped_column(Integer, nullable=False)
    ftr: Mapped[str] = mapped_column(String(1), nullable=False)
    hthg: Mapped[int] = mapped_column(Integer, nullable=False)
    htag: Mapped[int] = mapped_column(Integer, nullable=False)
    htr: Mapped[str] = mapped_column(String(1), nullable=True)
    attendance: Mapped[float] = mapped_column(Float, nullable=True)
    referee: Mapped[str] = mapped_column(String, nullable=True)
    hsh: Mapped[int] = mapped_column(Integer, nullable=True)
    ash: Mapped[int] = mapped_column(Integer, nullable=True)  # 'as' is SQL keyword
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

    __table_args__ = (
        UniqueConstraint("match_date", "hometeam", "awayteam", "div"),
    )

Base.metadata.create_all(engine)


# helper function to change date type of date column
def date_adjusted(date_column: str):
    d, m, y = date_column.split("/")
    if len(y) == 2:
        y = int(y) + 2000
    return date(int(y), int(m), int(d))


# load each csv file into postgres 
def data_ingestion(dir: str):
    session = SessionLocal()
    files = os.listdir(dir)
    files.sort()
    for file in files:
        if re.match(r"\d{4}-\d{2}\.csv", file):
            df = pd.read_csv(f"{dir}/{file}")
            ss = file.split(".")[0]  # get the season
            df["Date"] = df["Date"].apply(date_adjusted)

            for _, row in df.iterrows():
                stmt = insert(Match).values(
                    season=ss,
                    div=row.get("Div"),
                    match_date=row["Date"],
                    hometeam=row["HomeTeam"],
                    awayteam=row["AwayTeam"],
                    fthg=row.get("FTHG"),
                    ftag=row.get("FTAG"),
                    ftr=row.get("FTR"),
                    hthg=row.get("HTHG"),
                    htag=row.get("HTAG"),
                    htr=row.get("HTR"),
                    attendance=row.get("Attendance"),
                    referee=row.get("Referee"),
                    hsh=row.get("HS"),
                    ash=row.get("AS"),
                    hst=row.get("HST"),
                    ast=row.get("AST"),
                    hhw=row.get("HHW"),
                    ahw=row.get("AHW"),
                    hc=row.get("HC"),
                    ac=row.get("AC"),
                    hf=row.get("HF"),
                    af=row.get("AF"),
                    hy=row.get("HY"),
                    ay=row.get("AY"),
                    hr=row.get("HR"),
                    ar=row.get("AR"),
                )

                # Upsert data
                stmt = stmt.on_conflict_do_update(
                    index_elements=["match_date", "hometeam", "awayteam", "div"],
                    set_={
                        "fthg": stmt.excluded.fthg,
                        "ftag": stmt.excluded.ftag,
                        "ftr": stmt.excluded.ftr,
                        "hthg": stmt.excluded.hthg,
                        "htag": stmt.excluded.htag,
                        "htr": stmt.excluded.htr,
                        "attendance": stmt.excluded.attendance,
                        "referee": stmt.excluded.referee,
                        "hsh": stmt.excluded.hsh,
                        "ash": stmt.excluded.ash,
                        "hst": stmt.excluded.hst,
                        "ast": stmt.excluded.ast,
                        "hy": stmt.excluded.hy,
                        "ay": stmt.excluded.ay,
                        "hr": stmt.excluded.hr,
                        "ar": stmt.excluded.ar,
                    }
                )
                session.execute(stmt)

    session.commit()
    session.close()


if __name__ == "__main__":
    input_dir = str(input("Give me link nowwww: "))
    try:
        data_ingestion(input_dir)
        print("Yayyy successfully!")
    except Exception as e:
        raise ValueError(e)
