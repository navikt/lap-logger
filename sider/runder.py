import streamlit as st
import time
from datetime import datetime

from config import ANTALL_RUNDER, RUNDE_START_TIME, TIDSSONE
from hjelper import (
    les_deltakere, les_rundetider, rundetider_fil,
    total_sekunder, formater_tid, runde_starttid,
)


def vis(faner):
    deltaker_map = les_deltakere()
    alle_tider = les_rundetider()

    for runde_nr in range(1, ANTALL_RUNDER + 1):
        with faner[runde_nr]:
            starttid = runde_starttid(runde_nr)
            st.header(f"Runde {runde_nr}")
            st.info(f"🕐 Starttid: **kl {RUNDE_START_TIME + runde_nr - 1}:00**")

            # Vis feedback fra forrige registrering (vises i 5 sek)
            feedback_key = f"feedback_runde_{runde_nr}"
            if feedback_key in st.session_state:
                melding, tidsstempel, er_feil = st.session_state[feedback_key]
                if time.time() - tidsstempel < 5:
                    if er_feil:
                        st.error(melding)
                    else:
                        st.success(melding)
                else:
                    del st.session_state[feedback_key]

            with st.form(f"runde_{runde_nr}_form", clear_on_submit=True, border=False):
                c1, c2 = st.columns([2, 1])
                with c1:
                    rid = st.text_input("Scan / skriv inn deltaker-Id:", key=f"rid_{runde_nr}")
                with c2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    lagre_runde = st.form_submit_button("Registrer tid")

                if lagre_runde and rid:
                    allerede_registrert = any(
                        t["id"] == rid and t["runde"] == runde_nr for t in alle_tider
                    )
                    if allerede_registrert:
                        st.session_state[feedback_key] = (
                            f"❌ {deltaker_map.get(rid, rid)} er allerede registrert i runde {runde_nr}",
                            time.time(), True,
                        )
                    else:
                        naa = datetime.now(TIDSSONE)
                        delta = naa - starttid
                        tot_sek = max(int(delta.total_seconds()), 0)
                        rmin = tot_sek // 60
                        rsek = tot_sek % 60
                        rundetider_fil.skriv([rid, str(runde_nr), str(rmin), str(rsek)])
                        navn = deltaker_map.get(rid, rid)
                        st.session_state[feedback_key] = (
                            f"✅ {navn} — {formater_tid(tot_sek)}",
                            time.time(), False,
                        )
                    st.rerun()

            # Vis resultattavle for denne runden, sortert på tid (stigende)
            runde_tider = [t for t in alle_tider if t["runde"] == runde_nr]
            if runde_tider:
                runde_tider.sort(key=lambda t: total_sekunder(t["minutter"], t["sekunder"]))
                medaljer = {1: "🥇", 2: "🥈", 3: "🥉"}
                tabell = []
                for plassering, t in enumerate(runde_tider, start=1):
                    navn = deltaker_map.get(t["id"], t["id"])
                    tabell.append({
                        "#": f"{medaljer.get(plassering, '')} {plassering}",
                        "Navn": navn,
                        "Rundetid": formater_tid(total_sekunder(t["minutter"], t["sekunder"])),
                    })
                st.subheader("Resultater")
                st.dataframe(tabell, hide_index=True, use_container_width=True)
            else:
                st.write("Ingen tider registrert for denne runden ennå.")

