import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.title("⚽Euro 2024 Shot Map")
st.subheader("Filter to any team then player to see all of their shots and goal-scoring shots!")

df = pd.read_csv('euros_2024_shot_map.csv')
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
if st.session_state.team:
 selected_player = st.selectbox('Select a player', df[df['team'] == st.session_state.team]['player'].sort_values().unique(), on_change=update_player, key='player')

# Create the pitch and plot shots 
pitch = VerticalPitch(pitch_type='statsbomb', half=True) 
fig, ax = pitch.draw(figsize=(10, 10)) 

# Filter data for the selected player 
if st.session_state.team and st.session_state.player:
  player_shots = df[(df['team'] == st.session_state.team) & (df['player'] == st.session_state.player)] 

for i, shot in player_shots.iterrows(): 
  pitch.scatter( x=float(shot['location'][0]), 
                y=float(shot['location'][1]), 
                ax=ax, 
                s=1000 * shot['shot_statsbomb_xg'], 
                color='green' if shot['shot_outcome'] == 'Goal' else 'white', 
                edgecolors='black', 
                alpha=1 if shot['type'] == 'goal' else 0.5, 
                zorder=2 if shot['type'] == 'goal' else 1 )

# Display the pitch with shots 
st.pyplot(fig)


