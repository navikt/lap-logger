import streamlit as st
import time

import lagring
from hjelper import les_deltakere


def vis(fane):
    with fane:
        # Vis feedback fra forrige registrering (vises i 5 sek)
        feedback_key = "feedback_registrering"
        if feedback_key in st.session_state:
            melding, tidsstempel, er_feil = st.session_state[feedback_key]
            if time.time() - tidsstempel < 5:
                if er_feil:
                    st.error(melding)
                else:
                    st.success(melding)
            else:
                del st.session_state[feedback_key]

        with st.form("Registrering", clear_on_submit=True, border=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                deltaker_navn = st.text_input(label="Navn:", key="navn_id")
            with col2:
                deltaker_id = st.text_input(label="Id:", key="deltaker_id")
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                registrering_knapp = st.form_submit_button("Registrer deltaker")

            if registrering_knapp:
                eksisterende = les_deltakere()
                if deltaker_id in eksisterende:
                    st.session_state[feedback_key] = (
                        f"❌ Id '{deltaker_id}' er allerede registrert ({eksisterende[deltaker_id]})",
                        time.time(), True,
                    )
                elif not deltaker_id or not deltaker_navn:
                    st.session_state[feedback_key] = (
                        "❌ Både navn og id må fylles ut",
                        time.time(), True,
                    )
                else:
                    lagring.legg_til_deltaker(deltaker_id, deltaker_navn)
                    st.session_state[feedback_key] = (
                        f"✅ {deltaker_navn} ({deltaker_id}) registrert!",
                        time.time(), False,
                    )
                st.rerun()

        st.header("Registrerte deltakere")
        alle_deltakere = lagring.les_deltakere()
        if alle_deltakere:
            rader = [
                {"Startnummer": d.get("startnummer", i), "Navn": d["navn"], "Id": d["id"]}
                for i, d in enumerate(alle_deltakere, start=1)
            ]
            st.dataframe(rader, hide_index=True, column_config={
                "Startnummer": st.column_config.NumberColumn(width="small"),
                "Navn": st.column_config.TextColumn(width="large"),
                "Id": st.column_config.TextColumn(width="large"),
            })
        else:
            st.write("Ingen deltakere registrert ennå.")


