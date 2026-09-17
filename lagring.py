import os
import streamlit as st
from supabase import create_client, Client


def _hent_secret(nøkkel: str) -> str:
    """Les fra st.secrets (lokalt) eller miljøvariabler (NAIS)."""
    # Prøv miljøvariabler først (NAIS / Docker)
    verdi = os.environ.get(nøkkel)
    if verdi:
        return verdi
    # Prøv st.secrets (lokalt med secrets.toml)
    try:
        return st.secrets[nøkkel]
    except Exception:
        raise RuntimeError(f"Mangler secret '{nøkkel}' — sett som miljøvariabel eller i .streamlit/secrets.toml")


_url: str = _hent_secret("SUPABASE_URL")
_key: str = _hent_secret("SUPABASE_KEY")
_supabase: Client = create_client(_url, _key)


@st.cache_data(ttl=30, show_spinner=False)
def les_arrangement(arrangement_id: int) -> dict | None:
    """Returnerer dict: {'id', 'navn', 'tidspunkt', 'antall_runder'} for et arrangement."""
    try:
        resp = (
            _supabase.table("arrangementer")
            .select("*")
            .eq("id", arrangement_id)
            .limit(1)
            .execute()
        )
        if not resp.data:
            return None
        return resp.data[0]
    except Exception as e:
        st.error(f"Kunne ikke hente arrangement: {e}")
        return None


def _hent_arrangement_deltaker_id(arrangement_id: int, deltaker_id: str) -> int | None:
    resp = (
        _supabase.table("arrangement_deltakere")
        .select("id")
        .eq("arrangement_id", arrangement_id)
        .eq("deltaker_id", deltaker_id)
        .limit(1)
        .execute()
    )
    if not resp.data:
        return None
    return resp.data[0]["id"]


@st.cache_data(ttl=5, show_spinner=False)
def les_deltakere(arrangement_id: int | None = None) -> list[dict]:
    """Returnerer liste med dicts: {'id': ..., 'navn': ..., 'startnummer': ...}"""
    try:
        if arrangement_id is None:
            resp = _supabase.table("deltakere").select("*").order("navn").execute()
            return resp.data

        resp = (
            _supabase.table("arrangement_deltakere")
            .select("deltaker_id, startnummer, deltakere(navn)")
            .eq("arrangement_id", arrangement_id)
            .order("startnummer")
            .execute()
        )
        return [
            {
                "id": row["deltaker_id"],
                "navn": (row.get("deltakere") or {}).get("navn") or row["deltaker_id"],
                "startnummer": row.get("startnummer"),
            }
            for row in resp.data
        ]
    except Exception as e:
        st.error(f"Kunne ikke hente deltakere: {e}")
        return []


def neste_startnummer(arrangement_id: int) -> int:
    """Returnerer neste ledige startnummer for et arrangement."""
    resp = (
        _supabase.table("arrangement_deltakere")
        .select("startnummer")
        .eq("arrangement_id", arrangement_id)
        .order("startnummer", desc=True)
        .limit(1)
        .execute()
    )
    if resp.data and resp.data[0]["startnummer"] is not None:
        return resp.data[0]["startnummer"] + 1
    return 1


def _finnes_deltaker(deltaker_id: str) -> bool:
    resp = (
        _supabase.table("deltakere")
        .select("id")
        .eq("id", deltaker_id)
        .limit(1)
        .execute()
    )
    return bool(resp.data)


def legg_til_deltaker(deltaker_id: str, navn: str, arrangement_id: int) -> int:
    """Finn/opprett person, koble til arrangement, og returner arrangement_deltakere.id."""
    # 1-3: Finn person via RFID, opprett kun hvis den ikke finnes (aldri upsert).
    if not _finnes_deltaker(deltaker_id):
        _supabase.table("deltakere").insert({"id": deltaker_id, "navn": navn}).execute()

    # 4-5: Finn/opprett deltakelse i det aktive arrangementet.
    arrangement_deltaker_id = _hent_arrangement_deltaker_id(arrangement_id, deltaker_id)
    if arrangement_deltaker_id is None:
        nr = neste_startnummer(arrangement_id)
        resp = _supabase.table("arrangement_deltakere").insert({
            "arrangement_id": arrangement_id,
            "deltaker_id": deltaker_id,
            "startnummer": nr,
        }).execute()
        arrangement_deltaker_id = resp.data[0]["id"]

    les_deltakere.clear()
    return arrangement_deltaker_id



@st.cache_data(ttl=5, show_spinner=False)
def les_rundetider(arrangement_id: int | None = None) -> list[dict]:
    """Returnerer liste med dicts: {'deltaker_id': ..., 'runde': ..., 'tid_sekunder': ...}"""
    try:
        if arrangement_id is None:
            resp = _supabase.table("rundetider").select("*").execute()
            return resp.data

        deltaker_resp = (
            _supabase.table("arrangement_deltakere")
            .select("id, deltaker_id")
            .eq("arrangement_id", arrangement_id)
            .execute()
        )
        if not deltaker_resp.data:
            return []

        arrangement_deltaker_id_map = {
            row["id"]: row["deltaker_id"] for row in deltaker_resp.data
        }
        arrangement_deltaker_ids = list(arrangement_deltaker_id_map.keys())
        resp = (
            _supabase.table("rundetider")
            .select("*")
            .in_("arrangement_deltaker_id", arrangement_deltaker_ids)
            .execute()
        )
        return [
            {
                "deltaker_id": arrangement_deltaker_id_map.get(row["arrangement_deltaker_id"], row["arrangement_deltaker_id"]),
                "runde": row["runde"],
                "tid_sekunder": row["tid_sekunder"],
            }
            for row in resp.data
        ]
    except Exception as e:
        st.error(f"Kunne ikke hente rundetider: {e}")
        return []


def legg_til_rundetid(deltaker_id: str, runde: int, tid_sekunder: int, arrangement_id: int) -> None:
    arrangement_deltaker_id = _hent_arrangement_deltaker_id(arrangement_id, deltaker_id)
    if arrangement_deltaker_id is None:
        raise ValueError(f"Deltaker '{deltaker_id}' finnes ikke i arrangement {arrangement_id}")
    _supabase.table("rundetider").insert({
        "arrangement_deltaker_id": arrangement_deltaker_id,
        "runde": runde,
        "tid_sekunder": tid_sekunder,
    }).execute()
    les_rundetider.clear()


def finnes_rundetid(deltaker_id: str, runde: int, arrangement_id: int) -> bool:
    arrangement_deltaker_id = _hent_arrangement_deltaker_id(arrangement_id, deltaker_id)
    if arrangement_deltaker_id is None:
        return False
    resp = (
        _supabase.table("rundetider")
        .select("id")
        .eq("arrangement_deltaker_id", arrangement_deltaker_id)
        .eq("runde", runde)
        .execute()
    )
    return len(resp.data) > 0
