import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

import lagring
from config import ARRANGEMENTER, TIDSSONE
from hjelper import parse_tidspunkt
from sider import registrering, runder, totaloversikt, leaderboard


def render_arrangement(arrangement_id: int, arrangement_navn: str):
    with st.container():
        arrangement = lagring.les_arrangement(arrangement_id)
        if arrangement is None:
            st.error(f"Fant ikke arrangement {arrangement_id}")
            return

        arrangement_start = parse_tidspunkt(arrangement["tidspunkt"])
        antall_runder = arrangement["antall_runder"]

        naa = datetime.now(TIDSSONE)
        col_title, col_cd = st.columns([3, 2])
        with col_title:
            st.title(f"Nav Backyard {arrangement_navn} 🤘🏻💥")
        with col_cd:
            if naa < arrangement_start:
                total_sek = max(int((arrangement_start - naa).total_seconds()), 0)
                dager = total_sek // 86400
                timer = (total_sek % 86400) // 3600
                minutter = (total_sek % 3600) // 60

                deler = []
                if dager > 0:
                    deler.append(f"{dager}d")
                if dager > 0 or timer > 0:
                    deler.append(f"{timer:02d}t")
                deler.append(f"{minutter:02d}m")

                countdown_tekst = f"### ⏱️ Starter om {' '.join(deler)}"
                if total_sek < 300:
                    st.error(countdown_tekst)
                else:
                    st.info(countdown_tekst)

        fane_navn = (
            ["Registrering"]
            + [f"Runde {i}" for i in range(1, antall_runder + 1)]
            + ["Totaloversikt", "Leaderboard"]
        )
        faner = st.tabs(fane_navn)

        registrering.vis(faner[0], arrangement_id=arrangement_id)
        runder.vis(faner, arrangement_id=arrangement_id,
                   antall_runder=antall_runder, arrangement_start=arrangement_start)
        totaloversikt.vis(faner[antall_runder + 1], arrangement_id=arrangement_id,
                          antall_runder=antall_runder, arrangement_start=arrangement_start)
        leaderboard.vis(faner[antall_runder + 2], arrangement_id=arrangement_id)


st.set_page_config(layout="wide", page_title="Nav Backyard 2026")
st_autorefresh(interval=60000, key="global_refresh")

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

arrangement_tabs = st.tabs(["Høst 2026", "Vår 2026"])
with arrangement_tabs[0]:
    render_arrangement(ARRANGEMENTER["Høst 2026"], "Høst 2026")
with arrangement_tabs[1]:
    render_arrangement(ARRANGEMENTER["Vår 2026"], "Vår 2026")
