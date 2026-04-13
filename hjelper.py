from datetime import datetime

import lagring
from config import RUNDE_START_TIME, EVENT_DATO, TIDSSONE


def les_deltakere() -> dict[str, str]:
    """Returnerer dict id -> navn."""
    data = lagring.les_deltakere()
    return {d["id"]: d["navn"] for d in data}


def les_rundetider() -> list[dict]:
    """Returnerer liste med dicts: deltaker_id, runde, tid_sekunder."""
    data = lagring.les_rundetider()
    return [
        {
            "id": d["deltaker_id"],
            "runde": d["runde"],
            "tid_sekunder": d["tid_sekunder"],
        }
        for d in data
    ]


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

