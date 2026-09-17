import streamlit as st
from datetime import datetime

import lagring
from config import TIDSSONE
from hjelper import les_deltakere, les_rundetider, formater_tid, runde_starttid


def vis(faner, arrangement_id: int, antall_runder: int, arrangement_start):
    deltaker_map = les_deltakere(arrangement_id)
    alle_tider = les_rundetider(arrangement_id)

    for runde_nr in range(1, antall_runder + 1):
        with faner[runde_nr]:
            starttid = runde_starttid(runde_nr, arrangement_start)
            st.header(f"Runde {runde_nr}")
            st.info(f"🕐 Starttid: **kl {starttid.strftime('%H:%M')}**")

            toast_key = f"toast_runde_{arrangement_id}_{runde_nr}"
            if toast_key in st.session_state:
                melding, ikon = st.session_state.pop(toast_key)
                st.toast(melding, icon=ikon)

            with st.form(f"runde_{arrangement_id}_{runde_nr}_form", clear_on_submit=True, border=False):
                c1, c2 = st.columns([2, 1])
                with c1:
                    rid = st.text_input("Scan / skriv inn deltaker-Id:", key=f"rid_{arrangement_id}_{runde_nr}")
                with c2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    lagre_runde = st.form_submit_button("Registrer tid")

                if lagre_runde and rid:
                    naa = datetime.now(TIDSSONE)
                    delta = naa - starttid
                    tot_sek = max(int(delta.total_seconds()), 0)
                    if tot_sek > 3600:
                        st.session_state[toast_key] = (
                            f"Registrering stengt — mer enn 1 time siden runde {runde_nr} startet", "❌",
                        )
                    elif lagring.finnes_rundetid(rid, runde_nr, arrangement_id=arrangement_id):
                        navn = deltaker_map.get(rid, rid)
                        st.session_state[toast_key] = (
                            f"{navn} er allerede registrert i runde {runde_nr}", "❌",
                        )
                    elif rid not in deltaker_map:
                        st.session_state[toast_key] = (
                            f"Id '{rid}' er ikke registrert som deltaker", "❌",
                        )
                    else:
                        lagring.legg_til_rundetid(rid, runde_nr, tot_sek, arrangement_id=arrangement_id)
                        navn = deltaker_map.get(rid, rid)
                        st.session_state[toast_key] = (
                            f"{navn} — {formater_tid(tot_sek)}", "✅",
                        )
                    st.rerun()

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
                st.dataframe(tabell, hide_index=True, use_container_width=True, height=(len(tabell) + 1) * 35 + 3)
            else:
                st.write("Ingen tider registrert for denne runden ennå.")

