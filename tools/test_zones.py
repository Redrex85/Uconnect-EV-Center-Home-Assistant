"""Self-check della logica zone (eseguibile senza Home Assistant).

    py -3 tools/test_zones.py
"""
from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "custom_components" / "uconnect_ev_center"
PKG = "uconnect_ev_center"
# package fittizio: evita di eseguire __init__.py (che importa Home Assistant)
_mod = types.ModuleType(PKG)
_mod.__path__ = [str(ROOT)]
sys.modules[PKG] = _mod
Z = importlib.import_module(f"{PKG}.zones")  # noqa: E402

ROME = (41.9028, 12.4964)
HOME = {"nome": "Casa", "prezzo": 0.25, "lat": ROME[0], "lon": ROME[1]}
BANDB = {"nome": "B&B", "prezzo": 0.40, "lat": 41.9100, "lon": 12.5000}


def test_validate():
    got = Z.validate_zones([
        {"nome": "  Casa  ", "prezzo": 0.31},
        {"nome": "casa", "prezzo": 0.9},          # duplicato
        {"nome": "Pubblica", "prezzo": 0.5},      # nome di un tipo: ammesso
        {"nome": "", "prezzo": 1},                # vuoto
        {"nome": "B&B", "prezzo": -3},            # prezzo negativo
    ], [{"nome": "B&B", "prezzo": 0.2, "lat": 45.0, "lon": 9.0}])
    assert [z["nome"] for z in got] == ["Casa", "Pubblica", "B&B"], got
    assert got[0]["prezzo"] == 0.31
    assert got[1]["prezzo"] == 0.5
    assert got[2]["prezzo"] == 0.0
    assert got[2]["lat"] == 45.0 and got[2]["lon"] == 9.0   # coordinate preservate

    many = Z.validate_zones([{"nome": f"Z{i}", "prezzo": 0.1} for i in range(20)])
    assert len(many) == Z.ZONE_SLOTS


def test_gps_and_fallbacks():
    zone = [HOME, BANDB]
    # 50 m da casa: vince casa anche se B&B e' piu' "prezzata"
    assert Z.nearest_zone(zone, ROME[0] + 0.00045, ROME[1]) == "Casa"
    # vicino al B&B
    assert Z.nearest_zone(zone, 41.9102, 12.5001) == "B&B"
    # fuori dal raggio (in mezzo al mare)
    assert Z.nearest_zone(zone, 40.0, 5.0) is None
    # nessuna coordinata configurata: nessuna zona
    assert Z.nearest_zone([{"nome": "Casa", "prezzo": 0.25}], *ROME) is None


def test_zone_for_session():
    zone = [HOME]
    assert Z.zone_for_session(zone, *ROME, location="home") == "Casa"
    assert Z.zone_for_session(zone, None, None, "not_home") == "Fuori"
    assert Z.zone_for_session(zone, 41.9102, 12.5001, "not_home") == "Fuori"
    assert Z.zone_for_session(zone, 41.9102, 12.5001, "") == "Fuori"
    assert Z.zone_for_session([], None, None, "home") == Z.ZONE_TIPI[0]
    # tracker dice "home" ma il GPS e' lontano: non fidarsi
    assert Z.zone_for_session(zone, None, None, "home", home_far=True) == "Fuori"


def test_price_and_filter():
    zone = [HOME, BANDB]
    assert Z.zone_price(zone, "B&B", 0.99) == 0.40
    assert Z.zone_price(zone, "b&b", 0.99) == 0.40
    assert Z.zone_price(zone, "Fuori", 0.99) == 0.99
    assert Z.zone_price(zone, None, 0.77) == 0.77

    # "Fuori" compare solo se esistono ricariche fuori zona
    opts = Z.filter_options(["Casa", "Fuori", "Azienda", "azienda", ""])
    assert opts == ["Tutte", "Casa", "Fotovoltaico", "Pubblica", "Azienda", "Fuori"], opts
    assert Z.filter_options([]) == ["Tutte", *Z.ZONE_TIPI]


def test_zone_of_legacy():
    assert Z.zone_of({"zona_tariffa": "B&B"}, "Casa") == "B&B"
    assert Z.zone_of({}, "Casa") == "Casa"
    assert Z.zone_of({"zona_tariffa": ""}, "Casa") == "Casa"


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("OK  ", name)
    print("TUTTI I TEST ZONE OK")


if __name__ == "__main__":
    _run()
