import streamlit as st
from datetime import datetime

import lagring
from config import ANTALL_RUNDER, RUNDE_START_TIME, TIDSSONE
from hjelper import les_deltakere, les_rundetider, formater_tid, runde_starttid


def vis(faner):
    deltaker_map = les_deltakere()
    alle_tider = les_rundetider()

    for runde_nr in range(1, ANTALL_RUNDER + 1):
        with faner[runde_nr]:
            starttid = runde_starttid(runde_nr)
            st.header(f"Runde {runde_nr}")
            st.info(f"🕐 Starttid: **kl {RUNDE_START_TIME + runde_nr - 1}:00**")

            # Vis toast fra forrige rerun
            toast_key = f"toast_runde_{runde_nr}"
            if toast_key in st.session_state:
                melding, ikon = st.session_state.pop(toast_key)
                st.toast(melding, icon=ikon)

            with st.form(f"runde_{runde_nr}_form", clear_on_submit=True, border=False):
                c1, c2 = st.columns([2, 1])
                with c1:
                    rid = st.text_input("Scan / skriv inn deltaker-Id:", key=f"rid_{runde_nr}")
                with c2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    lagre_runde = st.form_submit_button("Registrer tid")

                if lagre_runde and rid:
                    if lagring.finnes_rundetid(rid, runde_nr):
                        navn = deltaker_map.get(rid, rid)
                        st.session_state[toast_key] = (
                            f"{navn} er allerede registrert i runde {runde_nr}", "❌",
                        )
                    elif rid not in deltaker_map:
                        st.session_state[toast_key] = (
                            f"Id '{rid}' er ikke registrert som deltaker", "❌",
                        )
                    else:
                        naa = datetime.now(TIDSSONE)
                        delta = naa - starttid
                        tot_sek = max(int(delta.total_seconds()), 0)
                        lagring.legg_til_rundetid(rid, runde_nr, tot_sek)
                        navn = deltaker_map.get(rid, rid)
                        st.session_state[toast_key] = (
                            f"{navn} — {formater_tid(tot_sek)}", "✅",
                        )
                    st.rerun()

            # Vis resultattavle for denne runden, sortert på tid (stigende)
            runde_tider = [t for t in alle_tider if t["runde"] == runde_nr]
            if runde_tider:
                runde_tider.sort(key=lambda t: t["tid_sekunder"])
                medaljer = {1: "🥇", 2: "🥈", 3: "🥉"}
                tabell = []
                for plassering, t in enumerate(runde_tider, start=1):
                    navn = deltaker_map.get(t["id"], t["id"])
                    tabell.append({
                        "#": f"{medaljer.get(plassering, '')} {plassering}",
                        "Navn": navn,
                        "Rundetid": formater_tid(t["tid_sekunder"]),
                    })
                st.subheader("Resultater")
                st.dataframe(tabell, hide_index=True, use_container_width=True)
            else:
                st.write("Ingen tider registrert for denne runden ennå.")

