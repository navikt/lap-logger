import streamlit as st

from modeller import Deltaker
from hjelper import les_deltakere, deltakere_fil


def vis(fane):
    with fane:
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
                    st.error(f"❌ Id '{deltaker_id}' er allerede registrert ({eksisterende[deltaker_id]})")
                else:
                    deltaker = Deltaker(id=deltaker_id, navn=deltaker_navn)
                    deltakere_fil.skriv(rad=deltaker.rad())

        st.header("Registrerte deltakere")
        deltakere = deltakere_fil.les_hele_filen()
        if len(deltakere) > 1:
            rader = [{"Navn": (r := rad.strip().split(","))[1], "Id": r[0]} for rad in deltakere[1:]]
            st.dataframe(rader, hide_index=True)
        else:
            st.write("Ingen deltakere registrert ennå.")

