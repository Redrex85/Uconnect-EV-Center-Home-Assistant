# Contributing to Uconnect EV Center

Thanks for your interest! This document explains how to contribute.

## What this project is (and isn't)

- It is a HACS **integration** + Lovelace panel/card that **reads entities** produced
  by the [`hass-uconnect`](https://github.com/hass-uconnect/hass-uconnect) integration
  and turns them into a dashboard (charging, trips, costs, EU GSE/ARERA, maintenance, ...).
- It **does not** talk to Stellantis/Uconnect servers. Please do not add API/client
  code here — that belongs in `hass-uconnect`.
- Supported brands are only those `hass-uconnect` supports (Abarth, Alfa Romeo,
  Chrysler, Dodge, Fiat, Jeep, Lancia, Maserati, Ram). Other Stellantis brands
  (Peugeot, Citroën, Opel, DS) use different apps and are out of scope.

For large changes, please open an issue first to discuss the approach.

## Development setup

1. Have a working Home Assistant instance (HAOS or Core).
2. Copy `custom_components/uconnect_ev_center/` into your HA `config/custom_components/`.
3. Restart HA and add the integration from *Settings → Devices & Services*.
4. The panel and card are served from `custom_components/uconnect_ev_center/www/`.

No build step: the panel is a single ES module (`www/uconnect-ev-center-panel.js`).

## Checks before opening a PR

- Python syntax:
  - Linux/macOS: `python -m py_compile $(find custom_components -name "*.py")`
  - Windows: `py -3 -m py_compile (Get-ChildItem custom_components -Recurse -Filter *.py).FullName`
- Trip-engine self-check: `py -3 custom_components/uconnect_ev_center/trip_engine.py`
- Dev sanity helper: `py -3 tools/check_status.py`
- JSON valid: `strings.json` and every `translations/*.json`.

## Translations

- Edit `strings.json` **and** `translations/{it,en,fr,es,de}.json` together.
- Keep the key set identical across all files (the base is Italian).
- Panel UI strings live inline in `www/uconnect-ev-center-panel.js`
  (per-language dictionaries at the top of the file).

## Adding a car model

1. Add the model to `MODELS` in `const.py`, plus its entry in `MODEL_CAPACITY`
   (usable kWh) and `MODEL_POWERTRAIN` (`BEV`/`PHEV`).
2. Add `custom_components/uconnect_ev_center/images/<slug>.png`
   (transparent PNG, 800×450; slug = Home Assistant slugify of the model name).
3. Update the model list in `README.md` if relevant.

## Code style

- Python 3.12+, standard Home Assistant conventions.
- No new dependencies unless genuinely necessary.
- Do not add comments that merely restate the code.
- Avoid copying code from projects with incompatible licenses.

## Commits and pull requests

- Keep PRs small and focused on one thing.
- Describe **what** changed and **how you tested it**.
- Reference the related issue, if any.

## Reporting bugs

Include: Home Assistant version, integration version, car model and powertrain
(BEV/PHEV), what you expected vs what happened, and the relevant logs
(*Settings → System → Logs*).

## License

This project is released under the MIT License — see [LICENSE](LICENSE).
By contributing you agree that your work is released under the same license.
