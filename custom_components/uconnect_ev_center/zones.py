"""Zone di ricarica: logica pura (validazione, distanza, opzioni filtro).

Separata dal coordinator per poterla testare senza Home Assistant.
"""
from __future__ import annotations

from math import asin, cos, radians, sin, sqrt
from typing import Any, Callable, Iterable

from .const import ZONE_FUORI, ZONE_GPS_RADIUS_M, ZONE_MAX_LEN, ZONE_SLOTS, ZONE_TIPI


def _f(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def norm_zones(raw: Iterable[Any] | None) -> list[dict[str, Any]]:
    """Zone salvate, ripulite: {nome, prezzo, lat?, lon?}."""
    out: list[dict[str, Any]] = []
    for z in list(raw or [])[:ZONE_SLOTS]:
        if not isinstance(z, dict):
            continue
        nome = str(z.get("nome") or "").strip()[:ZONE_MAX_LEN]
        if not nome:
            continue
        row: dict[str, Any] = {"nome": nome, "prezzo": max(_f(z.get("prezzo")), 0.0)}
        for k in ("lat", "lon"):
            if z.get(k) is not None:
                row[k] = _f(z.get(k))
        out.append(row)
    return out


def validate_zones(raw: Iterable[Any] | None,
                   previous: Iterable[Any] | None = None) -> list[dict[str, Any]]:
    """Valida le zone in ingresso: nome unico, prezzo >= 0, coordinate preservate."""
    vecchie = {z["nome"].lower(): z for z in norm_zones(previous)}
    visti: set[str] = set()
    out: list[dict[str, Any]] = []
    for z in list(raw or [])[:ZONE_SLOTS]:
        if not isinstance(z, dict):
            continue
        nome = str(z.get("nome") or "").strip()[:ZONE_MAX_LEN]
        chiave = nome.lower()
        if not nome or chiave in visti:
            continue
        row: dict[str, Any] = {"nome": nome,
                               "prezzo": round(max(_f(z.get("prezzo")), 0.0), 4)}
        old = vecchie.get(chiave) or {}
        for k in ("lat", "lon"):
            val = z.get(k, old.get(k))
            if val is not None:
                row[k] = round(_f(val), 5)
        visti.add(chiave)
        out.append(row)
    return out


def default_zone(zones: list[dict[str, Any]]) -> str:
    return zones[0]["nome"] if zones else ZONE_TIPI[0]


def dist_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distanza in metri (haversine), sufficiente per un raggio di poche centinaia."""
    r = 6371000.0
    p1, p2 = radians(lat1), radians(lat2)
    dp, dl = p2 - p1, radians(lon2 - lon1)
    a = sin(dp / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * r * asin(min(1.0, sqrt(a)))


def nearest_zone(zones: list[dict[str, Any]], lat: float, lon: float,
                 radius_m: float = ZONE_GPS_RADIUS_M) -> str | None:
    """Zona piu' vicina entro il raggio, None se nessuna ha coordinate vicine."""
    best: str | None = None
    bestd: float | None = None
    for z in zones:
        if z.get("lat") is None or z.get("lon") is None:
            continue
        d = dist_m(float(lat), float(lon), float(z["lat"]), float(z["lon"]))
        if d <= radius_m and (bestd is None or d < bestd):
            best, bestd = z["nome"], d
    return best


def zone_for_session(zones: list[dict[str, Any]], lat: float | None, lon: float | None,
                     location: str) -> str:
    """Zona della ricarica che inizia: GPS > a casa (default) > Fuori."""
    if lat is not None and lon is not None:
        found = nearest_zone(zones, float(lat), float(lon))
        if found:
            return found
    if str(location or "").lower() == "home":
        return default_zone(zones)
    return ZONE_FUORI


def zone_price(zones: list[dict[str, Any]], nome: str, fallback: float) -> float:
    n = str(nome or "").strip().lower()
    for z in zones:
        if z["nome"].lower() == n:
            return z["prezzo"]
    return fallback


def filter_options(zone_names: Iterable[str]) -> list[str]:
    """Opzioni filtro: Tutte + tipi noti + zone configurate e presenti nei dati."""
    visti = {t.lower() for t in ZONE_TIPI}
    extra: list[str] = []
    for nome in list(zone_names):
        n = str(nome or "").strip()
        if not n or n.lower() in visti:
            continue
        visti.add(n.lower())
        extra.append(n)
    return ["Tutte", *ZONE_TIPI, *sorted(extra, key=str.lower)]


def zone_of(rec: dict[str, Any], default: str) -> str:
    """Zona di una ricarica; i record vecchi (senza campo) ricadono sul default."""
    return str(rec.get("zona_tariffa") or default)
