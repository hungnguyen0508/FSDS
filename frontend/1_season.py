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