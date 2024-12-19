import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.title("Euro 2024 Shot Map")
st.subheader("Filter to any team then player to see all of their shots taken!")

df = pd.read_csv('euro24_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)


# Initialize session state 
if 'team' not in st.session_state: 
  st.session_state.team = None 
if 'player' not in st.session_state: 
  st.session_state.player = None

# Define callback functions 
def update_team(): 
  st.session_state.team 

def update_player(): 
  st.session_state.player

# Select team 
selected_team = st.selectbox('Select a team', df['team'].sort_values().unique(), on_change=update_team, key='team')

# select player
selected_player = st.selectbox('Select a player', [st.session_state.team]['player'].sort_values().unique(), on_change=update_player, key='player')


pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))
filtered_player = st.session_state.player
