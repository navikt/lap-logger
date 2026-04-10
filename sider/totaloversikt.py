import streamlit as st
from datetime import datetime

from config import ANTALL_RUNDER, RUNDE_START_TIME, TIDSSONE
from hjelper import (
    les_deltakere, les_rundetider,
    total_sekunder, formater_tid, runde_starttid,
)


def vis(fane):
    deltaker_map = les_deltakere()
    alle_tider = les_rundetider()

    with fane:
        st.header("Totaloversikt")

        # Countdown til neste runde
        naa = datetime.now(TIDSSONE)
        neste_runde = None
        for rn in range(1, ANTALL_RUNDER + 1):
            start = runde_starttid(rn)
            if naa < start:
                neste_runde = rn
                break

        if neste_runde is not None:
            tid_igjen = runde_starttid(neste_runde) - naa
            total_sek_igjen = max(int(tid_igjen.total_seconds()), 0)
            minutter_igjen = total_sek_igjen // 60
            sekunder_igjen = total_sek_igjen % 60
            klokkeslett = f"kl {RUNDE_START_TIME + neste_runde - 1}:00"

            countdown_tekst = (
                f"⏱️ **Runde {neste_runde}** ({klokkeslett}) starter om\n"
                f"## {minutter_igjen:02d}m {sekunder_igjen:02d}s"
            )
            if total_sek_igjen < 300:
                st.error(countdown_tekst)
            else:
                st.info(countdown_tekst)
        elif naa >= runde_starttid(ANTALL_RUNDER):
            st.success("✅ **Alle runder er i gang eller fullført!**")
        else:
            st.info("🏁 **Runde 1 pågår!**")

        if alle_tider:
            # Bygg en rad per deltaker med tid per runde + total
            per_deltaker: dict[str, dict[int, int]] = {}
            for t in alle_tider:
                per_deltaker.setdefault(t["id"], {})[t["runde"]] = total_sekunder(
                    t["minutter"], t["sekunder"]
                )

            # Beregn rangering per runde for medaljer
            medaljer = {1: "🥇", 2: "🥈", 3: "🥉"}
            runde_rangeringer: dict[int, dict[str, int]] = {}
            for rn in range(1, ANTALL_RUNDER + 1):
                tider_i_runde = [
                    (did, runder[rn])
                    for did, runder in per_deltaker.items()
                    if rn in runder
                ]
                tider_i_runde.sort(key=lambda x: x[1])
                runde_rangeringer[rn] = {
                    did: plass + 1 for plass, (did, _) in enumerate(tider_i_runde)
                }

            tabell = []
            for did, runder in per_deltaker.items():
                navn = deltaker_map.get(did, did)

                # Rad 1: Akkumulert totaltid etter hver runde
                rad_total: dict[str, str] = {"Deltaker": navn}
                akkumulert = 0
                for rn in range(1, ANTALL_RUNDER + 1):
                    if rn in runder:
                        akkumulert += runder[rn]
                    if rn < ANTALL_RUNDER:
                        if rn in runder:
                            rad_total[f"Runde {rn}"] = formater_tid(akkumulert)
                        else:
                            rad_total[f"Runde {rn}"] = "—"
                rad_total["Total"] = formater_tid(akkumulert)

                # Rad 2: Rundetid per runde med medaljer
                rad_runde: dict[str, str] = {"Deltaker": ""}
                for rn in range(1, ANTALL_RUNDER):
                    if rn in runder:
                        plass = runde_rangeringer[rn].get(did, 0)
                        medalje = medaljer.get(plass, "")
                        rad_runde[f"Runde {rn}"] = (
                            f"{medalje} {formater_tid(runder[rn])}"
                            if medalje
                            else formater_tid(runder[rn])
                        )
                    else:
                        rad_runde[f"Runde {rn}"] = "—"
                if ANTALL_RUNDER in runder:
                    plass = runde_rangeringer[ANTALL_RUNDER].get(did, 0)
                    medalje = medaljer.get(plass, "")
                    rad_runde["Total"] = (
                        f"{medalje} {formater_tid(runder[ANTALL_RUNDER])}"
                        if medalje
                        else formater_tid(runder[ANTALL_RUNDER])
                    )
                else:
                    rad_runde["Total"] = "—"

                tabell.append(rad_total)
                tabell.append(rad_runde)

            st.dataframe(tabell, hide_index=True, height=(len(tabell) + 1) * 35 + 3)
        else:
            st.write("Ingen tider registrert ennå.")

