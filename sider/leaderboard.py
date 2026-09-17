import streamlit as st

from hjelper import les_deltakere, les_rundetider, formater_tid


def vis(fane, arrangement_id: int | None = None):
    deltaker_map = les_deltakere(arrangement_id)
    alle_tider = les_rundetider(arrangement_id)

    with fane:
        st.header("🏆 Leaderboard")
        if alle_tider:
            totaler: dict[str, int] = {}
            antall_runder_per: dict[str, int] = {}
            for t in alle_tider:
                totaler[t["id"]] = totaler.get(t["id"], 0) + t["tid_sekunder"]
                antall_runder_per[t["id"]] = antall_runder_per.get(t["id"], 0) + 1

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

            st.dataframe(tabell, hide_index=True, use_container_width=True, height=(len(tabell) + 1) * 35 + 3)
        else:
            st.write("Ingen tider registrert ennå.")

