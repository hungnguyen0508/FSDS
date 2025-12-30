import streamlit as st 
import pandas as pd
import requests 


Base_URL = "http://0.0.0.0:8080"


#/season
st.header("Data availability for Season statistics")
response = requests.get(f"{Base_URL}/season")
if response.status_code == 200: 
    st.write(response.json()["message"])

# season stat
st.header("Season Stat")
season_num = st.text_input("Season (format: yyyy-yy)", key = "input_ss_stat")
if st.button("Search", key="season_stat_search"): 
    response = requests.get(f"{Base_URL}/season/{season_num}")
    if response.status_code == 200: 
        st.dataframe(pd.DataFrame([response.json()]).T)
    elif response.status_code == 404: 
        st.warning("Season not found")
    else: 
        st.error(f"Error: {response.status_code}")

# Create season stat
st.header("Create new Season Stat")
season = st.text_input("Season (format: yyyy-yy)", key = "new_season")
spectator = st.number_input("Average spectator per match:", key = "average_spectator") 
goals_per_match = st.number_input("Average goals per match", key = "goals_per_match")
tot_yc = st.number_input("Total yellow cards", key = "total_yc")
tot_rc = st.number_input("Total red cards", key = "total_rx")
yc_per_match = st.number_input("Average yellow cards per match", key = "avg_yc")
rc_per_match = st.number_input("Average red cards per match", key = "avg_rc")
post_obj = {
    "season" : season, 
    "spectator":spectator, 
    "goals_per_match" : goals_per_match, 
    "tot_yc" : tot_yc, 
    "tot_rc" : tot_rc, 
    "yc_per_match" : yc_per_match, 
    "rc_per_match" : rc_per_match

}
if st.button("Create", key = "create_ss_stat"): 
    response = requests.post(f"{Base_URL}/Season", json = post_obj)
    if response.status_code == 201: 
        st.write(f"New season {season} is created")
    elif response.status_code == 404: 
        st.write(response.json()) 
    else: 
        st.error(f"Error:{response.status_code}")
        
    