import streamlit as st 
import requests
import pandas as pd

Base_URL = "http://0.0.0.0:8080"

#Streamlit app to interact with the FastAPI backend.
st.title("EPL Statistics App")


# first browse
st.header("Welcome to EPL Stat")
response = requests.get(f"{Base_URL}/")
if response.status_code == 200: 
    st.write(response.json()["message"])


#/season
st.header("Data availability for Season statistics")
response = requests.get(f"{Base_URL}/season")
if response.status_code == 200: 
    st.write(response.json()["message"])

# season stat
st.header("Season Stat")
season_num = st.text_input("Season (format: yyyy-yy)")
if st.button("Search", key="season_stat_search"): 
    response = requests.get(f"{Base_URL}/season/{season_num}")
    if response.status_code == 200: 
        st.dataframe(pd.DataFrame([response.json()]).T)
    elif response.status_code == 404: 
        st.warning("Season not found")
    else: 
        st.error(f"Error: {response.status_code}")



# information all team
st.header("Information of all teams")
response = requests.get(f"{Base_URL}/team/recent_performance")
if response.status_code == 200: 
    st.write("Information of all teams")
    st.dataframe(response.json())
else: 
    st.error(f"Error: {response.status_code}")



# team recent performance
st.header("Team performance of last 5 matches")
team = st.text_input("Team name (Capitalized first character)")
if st.button("Search",key="team_recent_performance"): 
    response = requests.get(f"{Base_URL}/team/recent_performance/{team}")
    if response.status_code == 200: 
        st.dataframe(pd.DataFrame([response.json()]))
    elif response.status_code == 404: 
        st.warning("Team not found")
    else: 
        st.error(f"Error: {response.status_code}")



# Head to head
st.header("Head to head")
team1 = st.number_input("Team 1",min_value = 1, step = 1)
team2 = st.number_input("Team 2", min_value = 1, step = 1)
if st.button("Search",key="head_to_head"): 
    response = requests.get(f"{Base_URL}/team/head_to_head?first_team={team1}&second_team={team2}")
    if response.status_code == 200: 
        st.dataframe(pd.DataFrame(response.json()))
    elif response.status_code == 404: 
        st.warning("Team not found")
    else: 
        st.error(f"Error: {response.status_code}")


