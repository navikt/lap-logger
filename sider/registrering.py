import streamlit as st
import time

from modeller import Deltaker
from hjelper import les_deltakere, deltakere_fil


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
                    deltaker = Deltaker(id=deltaker_id, navn=deltaker_navn)
                    deltakere_fil.skriv(rad=deltaker.rad())
                    st.session_state[feedback_key] = (
                        f"✅ {deltaker_navn} ({deltaker_id}) registrert!",
                        time.time(), False,
                    )
                st.rerun()

        st.header("Registrerte deltakere")
        deltakere = deltakere_fil.les_hele_filen()
        rader = [
            {"Startnummer": i, "Navn": r[1], "Id": r[0]}
            for i, rad in enumerate(deltakere[1:], start=1)
            if len(r := rad.strip().split(",")) >= 2
        ]
        if rader:
            st.dataframe(rader, hide_index=True, column_config={
                "Startnummer": st.column_config.NumberColumn(width="small"),
                "Navn": st.column_config.TextColumn(width="large"),
                "Id": st.column_config.TextColumn(width="large"),
            })
        else:
            st.write("Ingen deltakere registrert ennå.")


