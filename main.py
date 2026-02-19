import streamlit as st

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Runde:
    user_id: str
    runde_nummer: int
    start_tid: datetime
    slutt_tid: datetime = field(init=False)
    tid_brukt: int =  field(init=False)


    def beregn(self):
        self.slutt_tid = datetime.now()
        self.tid_brukt =  self.slutt_tid - self.start_tid


    def lagre(self):
        pass



@dataclass
class Deltaker:
    id: str
    navn: str
    runder: list[Runde] = field(default_factory=list, init=False)


    def legg_til_runde(self, runde: Runde) -> None:
        self.runder.append(runde)

    def lagre(self):
        pass




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
            deltaker.lagre()




    st.header("Registrerte deltakere")
    st.table()


with oversikt:
    st.header("Scan kortet ditt")
    st.table()