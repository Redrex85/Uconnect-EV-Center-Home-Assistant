"""Diagnostica redatta per Uconnect EV Center.

Espone lo stato dell'integrazione SENZA dati sensibili: mai host, IP, token o
testo di sistema. Gli errori di rete sono ridotti a un vocabolario fisso.
Home Assistant carica automaticamente questo modulo: nessuna registrazione.
"""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_BATTERY_LEVEL,
    CONF_CHARGING_ENTITY,
    CONF_LOCATION_ENTITY,
    CONF_ODOMETER,
    CONF_PLUG_ENTITY,
    CONF_RANGE,
    DOMAIN,
)

# chiavi di config mai esposte nel bundle
_SENSITIVE = ("token", "password", "secret", "api_key", "host", "url", "webhook")


def _redact(opts: dict[str, Any]) -> dict[str, Any]:
    """Rimuove le chiavi potenzialmente sensibili prima di esporre la config."""
    safe: dict[str, Any] = {}
    for key, val in opts.items():
        if any(s in str(key).lower() for s in _SENSITIVE):
            safe[key] = "**redacted**"
        elif val is None or isinstance(val, (str, int, float, bool)):
            safe[key] = val
        else:
            safe[key] = type(val).__name__
    return safe


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Bundle scaricabile da HA → Integrazione → ⋮ → Scarica diagnostica."""
    coord = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    opts = {**entry.data, **entry.options}

    sources: list[dict[str, str]] = []
    for key in (CONF_ODOMETER, CONF_BATTERY_LEVEL, CONF_RANGE,
                CONF_CHARGING_ENTITY, CONF_PLUG_ENTITY, CONF_LOCATION_ENTITY):
        eid = opts.get(key)
        if not eid:
            continue
        st = hass.states.get(eid)
        ok = bool(st and st.state not in ("unknown", "unavailable"))
        sources.append({"key": key, "state": "available" if ok else "unavailable"})

    return {
        "version": getattr(coord, "version", None),
        "update": {"last_ok": getattr(coord, "last_update_ok", None)},
        "sources": sources,
        "network": {"last_error": getattr(coord, "last_net_error", None)},
        "geocode": {
            "enabled": getattr(coord, "geocode_enabled", None),
            "last": getattr(coord, "geocode_last", None),
            "stats": getattr(coord, "geocode_stats", None),
        },
        "config_entry": {
            "data": _redact(dict(entry.data)),
            "options": _redact(dict(entry.options)),
        },
    }
