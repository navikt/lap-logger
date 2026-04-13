import streamlit as st

from hjelper import les_deltakere, les_rundetider, formater_tid


def vis(fane):
    deltaker_map = les_deltakere()
    alle_tider = les_rundetider()

    with fane:
        st.header("🏆 Leaderboard")
        if alle_tider:
            # Samle antall runder og totaltid per deltaker
            totaler: dict[str, int] = {}
            antall_runder_per: dict[str, int] = {}
            for t in alle_tider:
                totaler[t["id"]] = totaler.get(t["id"], 0) + t["tid_sekunder"]
                antall_runder_per[t["id"]] = antall_runder_per.get(t["id"], 0) + 1

            # Sorter: flest runder først, deretter lavest totaltid
            sortert = sorted(
                totaler.items(), key=lambda x: (-antall_runder_per[x[0]], x[1])
            )
            tabell = []
            medaljer = {1: "🥇", 2: "🥈", 3: "🥉"}
            for plassering, (did, total_sek) in enumerate(sortert, start=1):
                tabell.append({
                    "Plassering": f"{medaljer.get(plassering, '')} #{plassering}",
                    "Deltaker": deltaker_map.get(did, did),
                    "Runder": antall_runder_per[did],
                    "Total tid": formater_tid(total_sek),
                })

            st.dataframe(tabell, hide_index=True)
        else:
            st.write("Ingen tider registrert ennå.")

