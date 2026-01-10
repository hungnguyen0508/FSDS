import streamlit as st 
import requests 
import pandas as pd 
from datetime import datetime
from fe_helper_stat import check_match_goals, find_missing_fields
import os

Base_URL = f"http://{os.getenv('backend_env','0.0.0.0')}:8080"


# Post match
st.header("Post EPL football match")
season = st.text_input("Season", key="match_season", value = None, placeholder = "Format: YYYY-YY")
div = st.text_input("Division", key = "match_division",value = None,placeholder = "E0 for EPL (sole option)")
match_date = st.date_input("Match Date", format="YYYY-MM-DD", key = "Match Date",value = None)
match_date_js = match_date.strftime("%Y-%m-%d") if match_date else None
home_team = st.text_input("Home Team", key = "match_home_team",value = None)
away_team = st.text_input("Away Team", key = "match_away_team",value = None) 
fthg = st.number_input("Full Time home goals", min_value=0, max_value=100, key = "match_fthg",value = None)
ftag = st.number_input("Full Time away goals", min_value=0, max_value=100, key = "match_athg",value = None) 
ftr = st.selectbox(label = "Full Time result", options=("H","A","D"), key = "match_ft_result", index = None, placeholder="Specify full-time result") 
hthg = st.number_input("Half Time home goals", min_value=0, max_value=100, key="match_hthg",value = None)
htag = st.number_input("Half Time away goals", min_value=0, max_value=100, key="match_htag",value = None)
htr  = st.selectbox(label = "Half Time result", options = ("H","A","D"),key="match_htr", index = None,placeholder="Specify half-time result")
attendance = st.number_input("Attendance", min_value=0.0, key="match_attendance",value = None)
referee = st.text_input("Referee", key="match_referee",value = None)
hsh = st.number_input("Home shots", min_value=0, max_value=100, key="match_hsh",value = None)
ash = st.number_input("Away shots", min_value=0, max_value=100, key="match_ash",value = None)
hst = st.number_input("Home shots on target", min_value=0, max_value=100, key="match_hst",value = None)
ast = st.number_input("Away shots on target", min_value=0, max_value=100, key="match_ast",value = None)
hhw = st.number_input("Home hit woodwork", min_value=0, max_value=10, key="match_hhw",value = None)
ahw = st.number_input("Away hit woodwork", min_value=0, max_value=10, key="match_ahw",value = None)
hc = st.number_input("Home corners", min_value=0, max_value=50, key="match_hc",value = None)
ac = st.number_input("Away corners", min_value=0, max_value=50, key="match_ac",value = None)
hf = st.number_input("Home fouls", min_value=0, max_value=50, key="match_hf",value = None)
af = st.number_input("Away fouls", min_value=0, max_value=50, key="match_af",value = None)
hy = st.number_input("Home yellow cards", min_value=0, max_value=10, key="match_hy",value = None)
ay = st.number_input("Away yellow cards", min_value=0, max_value=10, key="match_ay",value = None)
hr = st.number_input("Home red cards", min_value=0, max_value=5, key="match_hr",value = None)
ar = st.number_input("Away red cards", min_value=0, max_value=5, key="match_ar",value = None)

if st.button("Create", key = "match_create"): 
    # raw for checking input
    raw_match_data = {
                "season" : season, 
                "division": div,
                "match_date": match_date_js,
                "home_team": home_team,
                "away_team": away_team,
                "fthg": fthg,
                "ftag": ftag,
                "ftr": ftr,
                "hthg": hthg,
                "htag": htag,
                "htr": htr,
                "attendance": attendance,
                "referee": referee,
                "hsh": hsh,
                "ash": ash,
                "hst": hst,
                "ast": ast,
                "hhw": hhw,
                "ahw": ahw,
                "hc": hc,
                "ac": ac,
                "hf": hf,
                "af": af,
                "hy": hy,
                "ay": ay,
                "hr": hr,
                "ar": ar
            }
    null_list = find_missing_fields(raw_match_data)
    # handle wrong input 
    if len(null_list) != 0: 
        st.warning(f"Try to fill in all inputs {null_list}")
    elif not (check_match_goals(fthg, ftag, ftr) and check_match_goals(hthg,htag,htr)): 
        st.warning(f"Conflict between goals and result for full time or half time")
    else: 
        # finally posted json data 
        match_data = {
        **raw_match_data,
        "home_team": home_team.strip(),
        "away_team": away_team.strip(),
        "referee": referee.strip(),
    }
        response = requests.post(f"{Base_URL}/match_result/", json = match_data)
        # handle request response
        if response.status_code == 201: 
            st.success("Match result was created successfully !")
        else:
            try: 
                st.error(f"Invalid input: {response.json().get('detail')}")
            except Exception:
                st.error("Server error")



# Delete match
st.header("Delete Match")
match_date = st.date_input("Match Date", format="YYYY-MM-DD", key = "Del Match Date",value = None)
match_date_js = match_date.strftime("%Y-%m-%d") if match_date else None
home_team = st.text_input("Home Team", key = "del_match_home_team",value = None)
away_team = st.text_input("Away Team", key = "del_match_away_team",value = None) 
if st.button("Delete", key = "del"): 
    raw_del_data = {
            "match_date": match_date_js, 
            "home_team": home_team, 
            "away_team": away_team
        }
    null_list = find_missing_fields(raw_del_data)
    # handle wrong input 
    if len(null_list) != 0: 
        st.warning(f"Try to fill in blank value {null_list}")
    else: 
        del_data = {
            **raw_del_data, 
            "home_team": home_team.strip(), 
            "away_team": away_team.strip()
        }
        response = requests.delete(f"{Base_URL}/match_result/", json=del_data)
        # handle request response
        if response.status_code == 204: 
            st.success("Match deleted Successfully")
        else: 
            try: 
                st.error(f"Invalid input: {response.json().get('detail')}")
            except Exception:
                st.error("Server error")


# Update Match
st.header("Put EPL football match")
season = st.text_input("Season", key="up_match_season", value = None, placeholder = "Format: YYYY-YY")
div = st.text_input("Division", key = "up_match_division",value = None,placeholder = "E0 for EPL (sole option)")
match_date = st.date_input("Match Date", format="YYYY-MM-DD", key = "up_match_Date",value = None)
match_date_js = match_date.strftime("%Y-%m-%d") if match_date else None
home_team = st.text_input("Home Team", key = "up_match_home_team",value = None)
away_team = st.text_input("Away Team", key = "up_match_away_team",value = None) 
fthg = st.number_input("Full Time home goals", min_value=0, max_value=100, key = "up_match_fthg",value = None)
ftag = st.number_input("Full Time away goals", min_value=0, max_value=100, key = "up_match_athg",value = None) 
ftr = st.selectbox(label = "Full Time result", options=("H","A","D"), key = "up_match_ft_result", index = None, placeholder="Specify full-time result") 
hthg = st.number_input("Half Time home goals", min_value=0, max_value=100, key="up_match_hthg",value = None)
htag = st.number_input("Half Time away goals", min_value=0, max_value=100, key="up_match_htag",value = None)
htr  = st.selectbox(label = "Half Time result", options = ("H","A","D"),key="up_match_htr", index = None,placeholder="Specify half-time result")
attendance = st.number_input("Attendance", min_value=0.0, key="up_match_attendance",value = None)
referee = st.text_input("Referee", key="up_match_referee",value = None)
hsh = st.number_input("Home shots", min_value=0, max_value=100, key="up_match_hsh",value = None)
ash = st.number_input("Away shots", min_value=0, max_value=100, key="up_match_ash",value = None)
hst = st.number_input("Home shots on target", min_value=0, max_value=100, key="up_match_hst",value = None)
ast = st.number_input("Away shots on target", min_value=0, max_value=100, key="up_match_ast",value = None)
hhw = st.number_input("Home hit woodwork", min_value=0, max_value=10, key="up_match_hhw",value = None)
ahw = st.number_input("Away hit woodwork", min_value=0, max_value=10, key="up_match_ahw",value = None)
hc = st.number_input("Home corners", min_value=0, max_value=50, key="up_match_hc",value = None)
ac = st.number_input("Away corners", min_value=0, max_value=50, key="up_match_ac",value = None)
hf = st.number_input("Home fouls", min_value=0, max_value=50, key="up_match_hf",value = None)
af = st.number_input("Away fouls", min_value=0, max_value=50, key="up_match_af",value = None)
hy = st.number_input("Home yellow cards", min_value=0, max_value=10, key="up_match_hy",value = None)
ay = st.number_input("Away yellow cards", min_value=0, max_value=10, key="up_match_ay",value = None)
hr = st.number_input("Home red cards", min_value=0, max_value=5, key="up_match_hr",value = None)
ar = st.number_input("Away red cards", min_value=0, max_value=5, key="up_match_ar",value = None)

if st.button("Update", key = "match_update"): 
    # raw for checking input
    raw_upmatch_data = {
                "season" : season, 
                "division": div,
                "match_date": match_date_js,
                "home_team": home_team,
                "away_team": away_team,
                "fthg": fthg,
                "ftag": ftag,
                "ftr": ftr,
                "hthg": hthg,
                "htag": htag,
                "htr": htr,
                "attendance": attendance,
                "referee": referee,
                "hsh": hsh,
                "ash": ash,
                "hst": hst,
                "ast": ast,
                "hhw": hhw,
                "ahw": ahw,
                "hc": hc,
                "ac": ac,
                "hf": hf,
                "af": af,
                "hy": hy,
                "ay": ay,
                "hr": hr,
                "ar": ar
            }
    null_list = find_missing_fields(raw_upmatch_data)
    # handle wrong input 
    if len(null_list) != 0: 
        st.warning(f"Try to fill in all inputs {null_list}")
    elif not (check_match_goals(fthg, ftag, ftr) and check_match_goals(hthg,htag,htr)): 
        st.warning(f"Conflict between goals and result for full time or half time")
    else: 
        # finally posted json data 
        upmatch_data = {
        **raw_upmatch_data,
        "home_team": home_team.strip(),
        "away_team": away_team.strip(),
        "referee": referee.strip(),
    }
        response = requests.put(f"{Base_URL}/match_result/", json = upmatch_data)
        # handle request response
        if response.status_code == 201: 
            st.success("Match result was updated successfully !")
        else:
            try: 
                st.error(f"Invalid input: {response.json().get('detail')}")
            except Exception:
                st.error("Server error")