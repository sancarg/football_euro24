import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.title("⚽Euro 2024 Shot Map")
st.subheader("Select any team/player to see all their shots on the pitch!")

# Loading the dataset
df = pd.read_csv('euros_2024_shot_map.csv')
df['location'] = df['location'].apply(json.loads)

team = st.selectbox('Select a team', df['team'].sort_values().unique(), index=None)
player = st.selectbox('Select a player', df[df['team'] == team]['player'].sort_values().unique(), index=None)

def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    
    return df

filtered_df = filter_data(df, team, player)

pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))
