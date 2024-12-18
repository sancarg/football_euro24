import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.title("⚽Euro 2024 Shot Map")
st.subheader("Select any team/player to see all their shots on the pitch!")

# Loading the dataset
df = pd.read_csv('euro24_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)
teams = df['team'].sort_values().unique()
#team = st.selectbox('Select a team', teams, index=None)
