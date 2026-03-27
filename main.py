import streamlit as st

from config import ANTALL_RUNDER
from sider import registrering, runder, totaloversikt, leaderboard


st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.5rem; }
        [data-testid="stStatusWidget"] { display: none !important; }
        header [data-testid="stStatusWidget"] { display: none !important; }
        .stAppRunningIcon { display: none !important; }
        #stStatusWidget { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Nav Backyard 2026 🤘🏻💥")

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
