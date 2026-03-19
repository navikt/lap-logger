import streamlit as st

from config import ANTALL_RUNDER
from sider import registrering, runder, totaloversikt, leaderboard


st.set_page_config(layout="wide")

# --------------- faner ---------------

fane_navn = (
    ["Registrering"]
    + [f"Runde {i}" for i in range(1, ANTALL_RUNDER + 1)]
    + ["Totaloversikt", "Leaderboard"]
)

faner = st.tabs(fane_navn)

registrering.vis(faner[0])
runder.vis(faner)
totaloversikt.vis(faner[ANTALL_RUNDER + 1])
leaderboard.vis(faner[ANTALL_RUNDER + 2])
