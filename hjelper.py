from datetime import datetime, timedelta

import lagring
from config import TIDSSONE


def les_deltakere(arrangement_id: int | None = None) -> dict[str, str]:
    """Returnerer dict id -> navn."""
    data = lagring.les_deltakere(arrangement_id)
    return {d["id"]: d["navn"] for d in data}


def les_rundetider(arrangement_id: int | None = None) -> list[dict]:
    """Returnerer liste med dicts: deltaker_id, runde, tid_sekunder."""
    data = lagring.les_rundetider(arrangement_id)
    return [
        {
            "id": d["deltaker_id"],
            "runde": d["runde"],
            "tid_sekunder": d["tid_sekunder"],
        }
        for d in data
    ]


def formater_tid(total_sek: float) -> str:
    total_sek = int(round(total_sek))
    t = total_sek // 3600
    m = (total_sek % 3600) // 60
    s = total_sek % 60
    if t > 0:
        return f"{t}t {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def parse_tidspunkt(tidspunkt) -> datetime:
    """Konverterer arrangementets tidspunkt (ISO-streng eller datetime) til lokal tidssone."""
    if isinstance(tidspunkt, str):
        dt = datetime.fromisoformat(tidspunkt)
    else:
        dt = tidspunkt
    return dt.astimezone(TIDSSONE)


def runde_starttid(runde_nr: int, arrangement_start: datetime) -> datetime:
    """Returnerer starttidspunkt for en gitt runde ut fra arrangementets starttidspunkt."""
    return arrangement_start + timedelta(hours=runde_nr - 1)

