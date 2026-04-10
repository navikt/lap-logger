from datetime import datetime

from lagring import CSVFil
from config import ANTALL_RUNDER, RUNDE_START_TIME, EVENT_DATO, TIDSSONE


deltakere_fil = CSVFil("deltakere.csv", kolonner=["id", "navn"])
rundetider_fil = CSVFil("rundetider.csv", kolonner=["id", "runde", "minutter", "sekunder"])


def les_deltakere() -> dict[str, str]:
    """Returnerer dict id -> navn."""
    linjer = deltakere_fil.les_hele_filen()
    deltakere: dict[str, str] = {}
    for linje in linjer[1:]:
        deler = linje.strip().split(",")
        if len(deler) >= 2:
            deltakere[deler[0]] = deler[1]
    return deltakere


def les_rundetider() -> list[dict]:
    """Returnerer liste med dicts: id, runde, minutter, sekunder."""
    linjer = rundetider_fil.les_hele_filen()
    rader: list[dict] = []
    for linje in linjer[1:]:
        deler = linje.strip().split(",")
        if len(deler) >= 4:
            try:
                rader.append({
                    "id": deler[0],
                    "runde": int(deler[1]),
                    "minutter": int(deler[2]),
                    "sekunder": int(deler[3]),
                })
            except ValueError:
                continue
    return rader


def total_sekunder(m: int, s: int) -> int:
    return m * 60 + s


def formater_tid(total_sek: int) -> str:
    t = total_sek // 3600
    m = (total_sek % 3600) // 60
    s = total_sek % 60
    if t > 0:
        return f"{t}t {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def runde_starttid(runde_nr: int) -> datetime:
    """Returnerer starttidspunkt for en gitt runde på event-dagen."""
    t = RUNDE_START_TIME + (runde_nr - 1)
    return datetime(*EVENT_DATO, hour=t, minute=0, second=0, tzinfo=TIDSSONE)

