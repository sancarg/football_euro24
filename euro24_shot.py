import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.title("⚽Euro 2024 Shot Map")
st.subheader("Select any team/player to see all their shots on the pitch!")

# Loading the dataset
df = pd.read_csv('euros_2024_shot_map.csv')
st.table(df)
