import os
import streamlit as st
from supabase import create_client, Client


def _hent_secret(nøkkel: str) -> str:
    """Les fra st.secrets (lokalt) eller miljøvariabler (NAIS)."""
    try:
        return st.secrets[nøkkel]
    except (KeyError, FileNotFoundError):
        return os.environ[nøkkel]


_url: str = _hent_secret("SUPABASE_URL")
_key: str = _hent_secret("SUPABASE_KEY")
_supabase: Client = create_client(_url, _key)


def les_deltakere() -> list[dict]:
    """Returnerer liste med dicts: {'id': ..., 'navn': ..., 'startnummer': ...}"""
    resp = _supabase.table("deltakere").select("*").order("startnummer").execute()
    return resp.data


def neste_startnummer() -> int:
    """Returnerer neste ledige startnummer."""
    resp = _supabase.table("deltakere").select("startnummer").order("startnummer", desc=True).limit(1).execute()
    if resp.data and resp.data[0]["startnummer"] is not None:
        return resp.data[0]["startnummer"] + 1
    return 1


def legg_til_deltaker(deltaker_id: str, navn: str) -> None:
    nr = neste_startnummer()
    _supabase.table("deltakere").insert({"id": deltaker_id, "navn": navn, "startnummer": nr}).execute()


def les_rundetider() -> list[dict]:
    """Returnerer liste med dicts: {'id': ..., 'deltaker_id': ..., 'runde': ..., 'tid_sekunder': ...}"""
    resp = _supabase.table("rundetider").select("*").execute()
    return resp.data


def legg_til_rundetid(deltaker_id: str, runde: int, tid_sekunder: int) -> None:
    _supabase.table("rundetider").insert({
        "deltaker_id": deltaker_id,
        "runde": runde,
        "tid_sekunder": tid_sekunder,
    }).execute()


def finnes_rundetid(deltaker_id: str, runde: int) -> bool:
    resp = (
        _supabase.table("rundetider")
        .select("id")
        .eq("deltaker_id", deltaker_id)
        .eq("runde", runde)
        .execute()
    )
    return len(resp.data) > 0
