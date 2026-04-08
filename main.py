import streamlit as st

from config import ANTALL_RUNDER, EVENT_DATO, RUNDE_START_TIME
from sider import registrering, runder, totaloversikt, leaderboard
from datetime import datetime


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

# Overskrift med countdown til arrangementet
event_start = datetime(*EVENT_DATO, hour=RUNDE_START_TIME)
naa = datetime.now()
col_title, col_cd = st.columns([3, 2])
with col_title:
    st.title("Nav Backyard 2026 🤘🏻💥")
with col_cd:
    if naa < event_start:
        tid_igjen = event_start - naa
        total_sek = max(int(tid_igjen.total_seconds()), 0)
        dager = total_sek // 86400
        rest = total_sek % 86400
        timer = rest // 3600
        rest = rest % 3600
        minutter = rest // 60
        sekunder = rest % 60

        deler = []
        if dager > 0:
            deler.append(f"{dager}d")
        if dager > 0 or timer > 0:
            deler.append(f"{timer:02d}t")
        deler.append(f"{minutter:02d}m {sekunder:02d}s")

        countdown_tekst = f"### ⏱️ Starter om {' '.join(deler)}"
        if total_sek < 300:
            st.error(countdown_tekst)
        else:
            st.info(countdown_tekst)

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
