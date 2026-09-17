import streamlit as st

import lagring
from hjelper import les_deltakere


def vis(fane, arrangement_id: int | None = None):
    form_key_prefix = f"arr_{arrangement_id or 'global'}"
    with fane:
        # Vis toast fra forrige rerun
        toast_key = f"toast_registrering_{form_key_prefix}"
        if toast_key in st.session_state:
            melding, ikon = st.session_state.pop(toast_key)
            st.toast(melding, icon=ikon)

        with st.form(f"Registrering_{form_key_prefix}", clear_on_submit=True, border=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                deltaker_navn = st.text_input(label="Navn:", key=f"{form_key_prefix}_navn_id")
            with col2:
                deltaker_id = st.text_input(label="Id:", key=f"{form_key_prefix}_deltaker_id")
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                registrering_knapp = st.form_submit_button("Registrer deltaker")

            if registrering_knapp:
                eksisterende = les_deltakere(arrangement_id)
                if deltaker_id in eksisterende:
                    st.session_state[toast_key] = (
                        f"Id '{deltaker_id}' er allerede registrert ({eksisterende[deltaker_id]})", "❌",
                    )
                elif not deltaker_id or not deltaker_navn:
                    st.session_state[toast_key] = (
                        "Både navn og id må fylles ut", "❌",
                    )
                else:
                    lagring.legg_til_deltaker(deltaker_id, deltaker_navn, arrangement_id=arrangement_id)
                    st.session_state[toast_key] = (
                        f"{deltaker_navn} ({deltaker_id}) registrert!", "✅",
                    )
                st.rerun()

        st.header("Registrerte deltakere")
        alle_deltakere = lagring.les_deltakere(arrangement_id)
        if alle_deltakere:
            rader = [
                {"Startnummer": d.get("startnummer", i), "Navn": d["navn"]}
                for i, d in enumerate(alle_deltakere, start=1)
            ]
            st.dataframe(rader, hide_index=True, use_container_width=True,
                         height=(len(rader) + 1) * 35 + 3,
                         column_config={
                "Startnummer": st.column_config.NumberColumn(width="small"),
                "Navn": st.column_config.TextColumn(width="large"),
            })
        else:
            st.write("Ingen deltakere registrert ennå.")


