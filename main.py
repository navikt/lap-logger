import streamlit as st

from dataclasses import dataclass, field
from datetime import datetime

from lagring import CSVFil

deltakere_fil = CSVFil("deltakere.csv", kolonner=["id", "navn"])

@dataclass
class Runde:
    user_id: str
    runde_nummer: int
    start_tid: datetime
    slutt_tid: datetime = field(init=False)
    tid_brukt_minutter:  int =  field(init=False)
    tid_brukt_sekunder: int = field(init=False)


    def beregn(self):
        self.slutt_tid = datetime.now()
        delta_tid  = self.slutt_tid - self.start_tid
        self.tid_brukt_minutter = delta_tid.seconds // 60
        self.tid_brukt_sekunder = delta_tid.seconds % 60


@dataclass
class Deltaker:
    id: str
    navn: str

    def rad(self):
        return [value for value in self.__dict__.values()]



registrering, oversikt = st.tabs(["Registrering", "Oversikt"])

with registrering:

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
            deltaker = Deltaker(id=deltaker_id, navn=deltaker_navn)
            deltakere_fil.skriv(rad=deltaker.rad())





    st.header("Registrerte deltakere")
    deltakere = deltakere_fil.les_hele_filen()
    if len(deltakere) > 1:
        # Lager en liste med dictionaries for å vise i tabellen, og hopper over headeren, r := tilordner resultatet av split til r
        rader = [{"Navn": (r := rad.split(","))[1], "Id": r[0]} for rad in deltakere[1:]]
        st.dataframe(rader, hide_index=True)
    else:
        st.write("Ingen deltakere registrert ennå.")


with oversikt:
    st.header("Scan kortet ditt")
    st.table()