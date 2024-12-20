import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.title("⚽ Euro 2024 Shot Map")
st.subheader("Filter to any team then player to see all of their shots and goal-scoring shots!")

# Read and prepare the data
df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

# Print column names for debugging
st.write("Columns in the DataFrame:", df.columns.tolist())

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
selected_team = st.selectbox(
    'Select a team',
    df['team'].sort_values().unique(),
    on_change=update_team,
    key='team'
)

# Select player
if st.session_state.team:
    selected_player = st.selectbox(
        'Select a player',
        df[df['team'] == st.session_state.team]['player'].sort_values().unique(),
        on_change=update_player,
        key='player'
    )

# Function to filter data
def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

# Filter data for the selected player
filtered_df = filter_data(df, st.session_state.team, st.session_state.player)

# Create the pitch and plot shots
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

# Function to plot shots
def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if x['shot_outcome'] == 'Goal' else 1
        )

# Plot the filtered shots
plot_shots(filtered_df, ax, pitch)

# Display the pitch with shots
st.pyplot(fig)

