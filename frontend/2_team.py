import streamlit as st 
import pandas as pd
import requests 

Base_URL = "http://0.0.0.0:8080"


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
team = st.text_input("Team name (Capitalized first character)", key = "last_5_game")
if st.button("Search",key="team_recent_performance"): 
    if not team.strip(): 
        st.warning("Please enter a team name")
    else: 
        response = requests.get(f"{Base_URL}/team/recent_performance/{team}")
        if response.status_code == 200: 
            st.dataframe(pd.DataFrame([response.json()]))
        elif response.status_code == 404: 
            st.warning("Team not found")
        else: 
            st.error(f"Error: {response.status_code}")



# Head to head
st.header("Head to head")
st.write("Please use team ID above for input")
team1 = st.number_input("Team 1 (Team ID)",min_value = 1, step = 1, key = "team_1")
team2 = st.number_input("Team 2 (Team ID)", min_value = 1, step = 1, key = "team_2")
if st.button("Search",key="head_to_head"): 
    if not team1 or not team2:
        st.warning("Please enter the id of all teams")
    elif team1 == team2: 
        st.warning("Team IDs must not be equal")
    else:  
        response = requests.get(f"{Base_URL}/team/head_to_head?first_team={team1}&second_team={team2}")
        if response.status_code == 200: 
            st.dataframe(pd.DataFrame(response.json()))
        elif response.status_code == 404: 
            st.warning("Team not found")
        else: 
            st.error(f"Error: {response.status_code}")