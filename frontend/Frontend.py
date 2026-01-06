import streamlit as st
from PIL import Image
from pathlib import Path

# ===== PAGE CONFIG (PHẢI ĐẶT ĐẦU TIÊN) =====
st.set_page_config(
    page_title="EPL Stats Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===== LOAD IMAGE =====
logo = Image.open(f"./relevant_resources/Premier-League-Logo.png")
rooney = Image.open("./relevant_resources/rooney.jpg")
aguero = Image.open("./relevant_resources/aguero.jpg")
arteta = Image.open("./relevant_resources/arteta.jpg")
gerard = Image.open("./relevant_resources/gerard.jpg")


# ===== HEADER =====
col1, col2 = st.columns([1, 4])

with col1:
    st.image(logo, width="stretch")

with col2:
    st.title("English Premier League Statistics")
    st.subheader("Season 2000 – 2020")
    st.markdown(
        """
        A data-driven app providing historical statistics, 
        team performance analysis, and head-to-head comparisons 
        across two decades of the English Premier League.
        """
    )

st.divider()

# ===== INTRO SECTION =====
st.header("About This Dashboard")

st.markdown(
    """
    This web application is designed to help users explore **English Premier League (EPL) statistics**
    from the **2000/01 season to the 2019/20 season**.

    The dashboard provides:
    - **Season-level statistics**
    - **Team performance analysis**
    - **Head-to-head comparisons**
    - **Clean, structured, and queryable data**
    
    All data is processed through a modern data pipeline and served via a FastAPI backend.
    """
)

# ===== FEATURES =====
st.header("Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Season Stats")
    st.markdown(
        """
        - Total matches
        - Goals scored
        - Home vs away performance
        - Seasonal summaries
        """
    )

with col2:
    st.markdown("### Team Analysis")
    st.markdown(
        """
        - Team performance by season
        - Points, wins, draws, losses
        - Ranking insights
        """
    )

with col3:
    st.markdown("### Head-to-Head")
    st.markdown(
        """
        - Matchups between teams
        - Historical comparison
        - Goal differences & results
        """
    )




st.divider()

# ===== IMAGE =====
col1, col2, col3, col4 = st.columns(4)
with col1: 
    st.image(rooney)
with col2: 
    st.image(aguero)
with col3: 
    st.image(arteta)
with col4: 
    st.image(gerard)



st.divider()

# ===== TECH STACK =====
st.header("Tech Stack")

st.markdown(
    """
    - **Backend**: FastAPI  
    - **Data Modeling**: dbt  
    - **Database**: SQL-based warehouse  
    - **Frontend**: Streamlit  
    - **Language**: Python  

    """
)

st.divider()


pg = st.navigation(["1_season.py","2_team.py","3_match.py"])
pg.run()




st.divider()

# ===== FOOTER =====
st.markdown(
    """
    *This project is built for data analysis, learning, and demonstration purposes.*  
    *Powered by historical EPL data (2000–2020).*
    """
)
