import streamlit as st
import pandas as pd
from datetime import datetime

from config import TIDSSONE
from hjelper import les_deltakere, les_rundetider, formater_tid, runde_starttid


def vis(fane, arrangement_id: int, antall_runder: int, arrangement_start):
    deltaker_map = les_deltakere(arrangement_id)
    alle_tider = les_rundetider(arrangement_id)

    with fane:
        st.header("Totaloversikt")

        naa = datetime.now(TIDSSONE)
        neste_runde = None
        for rn in range(1, antall_runder + 1):
            start = runde_starttid(rn, arrangement_start)
            if naa < start:
                neste_runde = rn
                break

        if neste_runde is not None:
            neste_starttid = runde_starttid(neste_runde, arrangement_start)
            tid_igjen = neste_starttid - naa
            total_sek_igjen = max(int(tid_igjen.total_seconds()), 0)
            klokkeslett = f"kl {neste_starttid.strftime('%H:%M')}"

            dager = total_sek_igjen // 86400
            timer = (total_sek_igjen % 86400) // 3600
            minutter = (total_sek_igjen % 3600) // 60

            deler = []
            if dager > 0:
                deler.append(f"{dager}d")
            if dager > 0 or timer > 0:
                deler.append(f"{timer:02d}t")
            deler.append(f"{minutter:02d}m")

            tid_str = ' '.join(deler)
            if total_sek_igjen < 300:
                st.error(f"⏱️ Runde {neste_runde} ({klokkeslett}) starter om  **{tid_str}**")
            else:
                st.info(f"⏱️ Runde {neste_runde} ({klokkeslett}) starter om  **{tid_str}**")
        elif naa >= runde_starttid(antall_runder, arrangement_start):
            st.success("✅ **Alle runder er i gang eller fullført!**")
        else:
            st.info("🏁 **Runde 1 pågår!**")

        if alle_tider:
            per_deltaker: dict[str, dict[int, int]] = {}
            for t in alle_tider:
                per_deltaker.setdefault(t["id"], {})[t["runde"]] = t["tid_sekunder"]

            medaljer = {1: "🥇", 2: "🥈", 3: "🥉"}
            runde_rangeringer: dict[int, dict[str, int]] = {}
            for rn in range(1, antall_runder + 1):
                tider_i_runde = [
                    (did, runder_dict[rn])
                    for did, runder_dict in per_deltaker.items()
                    if rn in runder_dict
                ]
                tider_i_runde.sort(key=lambda x: x[1])
                runde_rangeringer[rn] = {
                    did: plass + 1 for plass, (did, _) in enumerate(tider_i_runde)
                }

            tabell = []
            sortert_deltakere = sorted(
                per_deltaker.items(),
                key=lambda x: (-len(x[1]), sum(x[1].values())),
            )
            for did, runder_dict in sortert_deltakere:
                navn = deltaker_map.get(did, did)
                rad_total: dict[str, str] = {"Deltaker": navn}
                akkumulert = 0
                for rn in range(1, antall_runder + 1):
                    if rn in runder_dict:
                        akkumulert += runder_dict[rn]
                    if rn < antall_runder:
                        if rn in runder_dict:
                            rad_total[f"Runde {rn}"] = formater_tid(akkumulert)
                        else:
                            rad_total[f"Runde {rn}"] = "—"
                rad_total["Total"] = formater_tid(akkumulert)

                rad_runde: dict[str, str] = {"Deltaker": ""}
                for rn in range(1, antall_runder):
                    if rn in runder_dict:
                        plass = runde_rangeringer[rn].get(did, 0)
                        medalje = medaljer.get(plass, "")
                        rad_runde[f"Runde {rn}"] = (
                            f"{medalje} {formater_tid(runder_dict[rn])}"
                            if medalje
                            else formater_tid(runder_dict[rn])
                        )
                    else:
                        rad_runde[f"Runde {rn}"] = "—"
                if antall_runder in runder_dict:
                    plass = runde_rangeringer[antall_runder].get(did, 0)
                    medalje = medaljer.get(plass, "")
                    rad_runde["Total"] = (
                        f"{medalje} {formater_tid(runder_dict[antall_runder])}"
                        if medalje
                        else formater_tid(runder_dict[antall_runder])
                    )
                else:
                    rad_runde["Total"] = "—"

                tabell.append(rad_total)
                tabell.append(rad_runde)

            df = pd.DataFrame(tabell)

            def fargelegg_par(row):
                person_nr = row.name // 2
                if person_nr % 2 == 1:
                    return ["background-color: rgba(128,128,128,0.1)"] * len(row)
                return [""] * len(row)

            styled = df.style.apply(fargelegg_par, axis=1)
            st.dataframe(styled, hide_index=True, height=(len(tabell) + 1) * 35 + 3)
        else:
            st.write("Ingen tider registrert ennå.")

