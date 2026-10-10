# AUDIT_REPORT — Uconnect EV Center Home Assistant

- **Data:** 2026-10-10
- **Versione progetto:** 1.0.0 (`VERSION`, `manifest.json`, `CHANGELOG.md` allineati)
- **Commit HEAD:** `785d60e`
- **Ambito:** revisione statica completa del repository (nessuna modifica ai sorgenti in questa fase)
- **Esito complessivo:** **DA CORREGGERE** (nessun bug bloccante; presenti difetti non bloccanti e verifiche dipendenti da un'istanza HA reale)

> Nota metodologica: nessuna credenziale reale è stata usata; nessuna chiamata verso API del veicolo è
> stata effettuata; nessun comando è stato inviato all'auto; nessun push/commit eseguito. I test
> eseguibili offline sono stati lanciati; i controlli che richiedono un'istanza Home Assistant attiva
> sono dichiarati esplicitamente come NON ESEGUITI.

---

## 1. Sintesi esecutiva

L'integrazione è **ben strutturata e di qualità sopra la media**: nessun segreto nel codice, I/O di file
in executor, chiamate HTTP via `aiohttp` (helpers HA), attenzione a `0` vs "dato mancante",
`_unrecorded_attributes` per non gonfiare il database del recorder, gestione multi-entry con `entry_id`.

Non sono emersi **bug bloccanti** (l'integrazione compila e i 45+ invarianti del self-check interno
passano). Sono però emersi **alcuni difetti reali non bloccanti** e alcune **incoerenze di metadati/asset**
che rendono opportuno un intervento prima di dichiarare la 1.0.0 "pronta". I punti principali:

1. `REC_VER = "1.1.7"` nel pannello ≠ `VERSION 1.0.0` → reload spurio + badge versione errato.
2. Badge **PayPal** in README punta a un **terzo** (`paypal.me/lamortella`) → donazioni dirottate + traccia del progetto d'origine.
3. `async_unload_entry` **non rimuove 4 servizi** registrati.
4. Con **più auto**: i servizi (ricarica/manutenzione/…) agiscono su **tutte** le entry.
5. Screenshot README **mancanti** (`docs/screenshots/…`).
6. **Nomi entità HA non localizzati** (hardcoded italiano), mentre il pannello è in 5 lingue.
7. Copia **divergente** di `card.js` (root vs pacchetto) e blocchi di traduzione **morti**.

---

## 2. Stato generale del progetto

| Aspetto | Stato | Evidenza |
|---|---|---|
| Caricamento Python | OK | `py_compile` 17/17 file |
| JSON (strings + 5 traduzioni) | OK | parse 6/6 |
| Parità chiavi traduzioni | OK | 0 mancanti / 0 extra su it/en/fr/es/de |
| Coerenza versione | **KO** | `REC_VER 1.1.7` ≠ `VERSION 1.0.0` |
| Self-check interno (tools) | 45 OK / 2 ERR reali (+2 falsi) | `tools/check_status.py` |
| Sensori ↔ chiavi `coordinator.data` | OK a livello di chiave | grep incrociato |
| Semantica valori sensori | **DA VERIFICARE** | richiede runtime HA |
| Segreti nel codice | nessuno | grep `password/token/secret/key` = 0 |
| Asset README | **incompleti** | `docs/screenshots/` assente |
| Provenienza/licenze | OK (MIT) ma **link donazione terzo** | README badge PayPal |

Stato Git: `main...origin/main` allineati, **nessuna modifica locale preesistente** (working tree pulito).

---

## 3. Architettura analizzata

Integrazione **custom "companion passiva"**: non parla con il cloud del veicolo, ma **legge entità già
esposte** dall'integrazione esterna `hass-uconnect` e ne calcola statistiche (viaggi, ricariche, costi,
salute batteria, GSE/ARERA).

- **Config flow a 3 passi**: `user` (profilo base/pro/enterprise) → `settings` (unica schermata a sezioni
  collapsed: auto + comandi + wallbox + impostazioni) → crea entry. Options flow `init` con lo stesso
  schema + preservazione dei valori salvati.
- **Coordinator** (`DataUpdateCoordinator`) con motori interni: `TripEngine` (viaggi dall'odometro),
  `meters.py` (contatori periodo), `store.py` (persistenza `.storage`), `dashboard.py` (dashboard
  Lovelace + risorse card), geocoding Nominatim opzionale con cache.
- **Piattaforme**: `sensor`, `binary_sensor`, `button`, `number`, `select`, `switch`, `time`,
  `device_tracker`, `climate`.
- **Frontend**: pannello web unico (`www/uconnect-ev-center-panel.js`, ~5.900 righe, 5 lingue) + card
  compatta (`www/uconnect-ev-center-card.js`).
- **Servizi**: 19 registrati in `__init__.py`.

---

## 4. Elenco file verificati

Codice: `__init__.py`, `config_flow.py`, `coordinator.py`, `sensor.py`, `binary_sensor.py`, `button.py`,
`number.py`, `select.py`, `switch.py`, `time.py`, `device_tracker.py`, `climate.py`, `const.py`,
`meters.py`, `store.py`, `trip_engine.py`, `dashboard.py`.
Config/meta: `manifest.json`, `hacs.json`, `VERSION`, `services.yaml`, `strings.json`,
`translations/{it,en,fr,es,de}.json`.
Frontend: `www/uconnect-ev-center-panel.js`, `www/uconnect-ev-center-card.js` (root + pacchetto).
Doc/asset: `README.md`, `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`, `docs/*`, `dashboards/*`,
`themes/*`, `examples/*`, `.github/workflows/*`, `tools/check_status.py`.

---

## 5. Risultati dei test realmente eseguiti

| Comando | Risultato | Note |
|---|---|---|
| `py -3 -m py_compile` (tutti i .py) | **OK 17/17** | nessun errore di sintassi |
| parse `strings.json` + `translations/*.json` | **OK 6/6** | JSON valido |
| Confronto chiavi traduzioni vs base | **OK** | 0 mancanti/extra su 5 lingue |
| `py -3 custom_components/…/trip_engine.py` | **OK** | self-check PHEV/BEV + aggregate |
| `py -3 tools/check_status.py` (UTF-8) | **4 problemi di cui 2 reali** | vedi §9/§10 |
| grep segreti (`password|token|secret|key|bearer`) | **0 hit** | nessun segreto |
| grep rete/IO bloccante | OK | solo `aiohttp` + `open()` in executor |

**NON eseguiti** (con motivo) — vedi §14: caricamento su HA reale, config flow UI, creazione entità,
hassfest, HACS validation, build/lint JS (Node assente), test delle risposte API (nessun campione).

---

## 6. Tabella sensori

Legenda: **Implementato** = classe presente; **Dato collegato** = la chiave usata esiste in
`coordinator.data` (verificato per grep incrociato); **Visualizzato** = usato nel pannello/README;
**Tradotto** = nome entità HA localizzato (**NO** = hardcoded italiano); **Esito**.

> I nomi entità sono generati in codice come `f"{name} …"` (53 occorrenze, `_attr_translation_key` = 0):
> la localizzazione è **PARZIALE** (pannello sì, entità HA no). Semantica dei valori = **DA VERIFICARE**
> senza runtime.

| Sensore (classe) | Chiave data | Implementato | Dato collegato | Visualizzato | Tradotto | Esito |
|---|---|---|---|---|---|---|
| EffKmPerKwh | eff_km_per_kwh | Sì | OK | Sì | NO | OK (valore DA VERIFICARE) |
| EffKwh100 | eff_kwh_100km | Sì | OK | Sì | NO | OK |
| BatteryKwh | battery_kwh | Sì | OK | Sì | NO | OK |
| CostPerKm / CostPer100Km | cost / km | Sì | OK | Sì | NO | OK |
| PeriodKmSensor | km | Sì | OK | Sì | NO | OK |
| WbEnergySensor | wb_energy | Sì | OK | Sì | NO | OK |
| CostoRicaricaSensor | cost | Sì | OK | Sì | NO | OK |
| PctBatteriaOggi | pct_daily | Sì | OK | Sì | NO | OK |
| EnergiaBatteriaSensor | kwh_batt | Sì | OK | Sì | NO | OK |
| TempoRicarica / OraCompletamento | estimate | Sì | OK | Sì | NO | OK |
| CostoRicaricaCorrente | estimate | Sì | OK | Sì | NO | OK |
| TipoRicarica | tipo_ricarica | Sì | OK | Sì | NO | OK |
| TripAttivoInfo / TripKmCorrenti / TripDurata | trip | Sì | OK | Sì | NO | OK |
| UltimoTrip | last_trip | Sì | OK | Sì | NO | OK |
| TripsOggi / KmOggiTrip | trips_oggi / km_oggi_trip | Sì | OK | Sì | NO | OK |
| StatisticheViaggi | stats_all | Sì | OK | Sì | NO | OK |
| ViaggiRecenti | trips_recent | Sì | OK | Sì | NO | OK |
| StoricoGiornaliero | history_days | Sì | OK | Sì | NO | OK |
| UltimaRicarica / DeltaUltimaCarica | last_charge | Sì | OK | Sì | NO | OK |
| RicaricheContatore | charges_* | Sì | OK | Sì | NO | OK |
| RisparmioTermica / RisparmioExtra | savings | Sì | OK | Sì | NO | OK |
| WbPotenza / WbTempoSessione | wb_power_kw / wb_session_time | Sì | OK | Sì | NO | OK |
| KwhTotaliConsumati / PercPer100km | kwh_batt / percorrenza | Sì | OK | Sì | NO | OK |
| ArchivioViaggi | trips_recent | Sì | OK | Sì | NO | OK |
| ListaRicariche | charges_filtered | Sì | OK | Sì | NO | OK |
| ReportGenerale | report | Sì | OK | Sì | NO | OK |
| EfficienzaRicarica / PerditeRicarica | health | Sì | OK | Sì | NO | OK |
| SohStimato | health | Sì | OK | Sì | NO | OK |
| EnergiaBatteriaUltimaRicarica | last_charge / kwh_per_1pct | Sì | OK | Sì | NO | OK |
| KwhPer1Pct | kwh_per_1pct | Sì | OK | Sì | NO | OK |
| Tagliandi | maintenance | Sì | OK | Sì | NO | OK |
| DrainFermo / DrainMese | drain_* | Sì | OK | Sì | NO | OK |
| ConsumoZona | zone_routes | Sì | OK | Sì | NO | OK |
| CO2Risparmiata | co2 | Sì | OK | Sì | NO | OK |
| Scadenze | scadenze | Sì | OK | Sì | NO | OK |
| ViaggioEstremo | best_trip / worst_trip | Sì | OK | Sì | NO | OK |
| EnergiaCasaTotale | energia_casa_totale | Sì | OK | Sì | NO | OK |
| Programmazione | schedule | Sì | OK | Sì | NO | OK |
| Percorrenza | percorrenza | Sì | OK | Sì | NO | OK |
| Assicurazione | assicurazione | Sì | OK | Sì | NO | OK |
| FvMese / FvTotale | fv_mese / energia_fv_totale | Sì | OK | Sì | NO | OK |

Altre piattaforme: `binary_sensor` (in-carica), `button`, `number` (target carica), `select` (4 filtri
ricariche), `switch` (bilanciamento), `time` (programmazioni), `device_tracker` (mirror posizione),
`climate` (pre-climatizzazione). **Esito:** implementate e collegate; `device_tracker`/`climate` sono
**mirror** di entità Uconnect (non ricalcolate).

---

## 7. Tabella funzionalità (README ↔ codice)

| Funzionalità | README | Implementata | Collega dato corretto | Esito |
|---|---|---|---|---|
| Riepilogo veicolo (Vista Veicolo) | Sì | Sì (`panel.js` p12 + `uc_*`) | Sì | OK |
| Batteria/autonomia | Sì | Sì | Sì | OK |
| Stato/cronologia ricarica | Sì | Sì (`charge_session`) | Sì | OK |
| Viaggi automatici | Sì | Sì (`TripEngine`) | Sì | OK |
| Consumi/efficienza (+ PHEV guard) | Sì | Sì | Sì | OK (BEV; PHEV non runtime-testato) |
| Posizione veicolo | Sì | Sì (device_tracker + timeline) | Sì | OK |
| Porte/serrature/luci/finestrini | Sì | Sì (mappatura `uc_stato`/comandi) | Sì | OK |
| Climatizzazione | Sì | Sì (`climate.py` mirror) | Sì | OK |
| Manutenzione/diagnostica | Sì | Sì | Sì | OK |
| Grafici/statistiche | Sì | Sì | Sì | OK (dipende da HA recorder/apex) |
| Selezione modelli/foto | Sì | Sì (`MODELS` + `images/`) | Sì | OK |
| Aggiornamento manuale/auto | Sì | Sì (`refresh_car`, listener stato) | Sì | OK |
| Dashboard automatica | Sì | Sì (`dashboard.py`, 12 viste) | Sì | OK |
| Screenshot | Sì (README) | **No** (`docs/screenshots/` assente) | — | **MANCANTE** |

Nessuna altra funzionalità dichiarata risulta non implementata.

---

## 8. Analisi delle traduzioni

- Lingue: **it, en, fr, es, de** (in `translations/`), base = `strings.json` (= `it.json`).
- **Parità chiavi: 0 mancanti, 0 extra** su tutte e 5 le lingue rispetto alla base.
- Interfaccia pannello: 5 lingue (dizionari inline in `panel.js`).
- **Nomi entità HA: NON localizzati** — hardcoded italiano (`f"{name} …"`, 53×), nessuna sezione
  `entity` né `_attr_translation_key`. Coerente con l'origine del progetto ma **limite reale**.
- **Chiavi morte**: `config.step.car` e `config.step.wallbox` esistono nelle traduzioni ma **non
  esistono step** `async_step_car`/`async_step_wallbox` (il flow usa solo `user`/`settings`/`init`).
- Fallback: `_t(key, fallback)` con default italiano → nessun errore se una chiave UI manca.

### Tabella chiavi mancanti per lingua

| Lingua | Chiavi mancanti vs base | Chiavi extra |
|---|---|---|
| it | 0 | 0 |
| en | 0 | 0 |
| fr | 0 | 0 |
| es | 0 | 0 |
| de | 0 | 0 |

---

## 9. Bug confermati

**B1 — MEDIA — `REC_VER` pannello ≠ versione integrazione**
- File: `custom_components/uconnect_ev_center/www/uconnect-ev-center-panel.js:23` (`const REC_VER = "1.1.7";`) vs `VERSION`/`manifest.json` = `1.0.0`.
- Condizione: aggiunta card/pannello.
- Impatto: `_checkVersion()` / `_startVersionWatch()` vedono `serverVer (1.0.0) ≠ REC_VER (1.1.7)` → `_reloadOnce()` esegue **un reload spurio** a ogni nuova sessione; il badge mostra `v1.1.7` errato.
- Evidenza: `tools/check_status.py` → `ERR auto-refresh: … REC_VER 1.1.7 != VERSION 1.0.0`; logica a righe 2609/2629.
- Correzione: allineare `REC_VER` a `VERSION` (o ricavarlo); far sì che il build/release lo aggiorni.
- Regressioni: verificare auto-reload dopo un vero upgrade.
- Test: caricare il pannello e controllare che non ci sia il reload spurio e che il badge mostri `v1.0.0`.

**B2 — BASSA — I servizi non vengono rimossi all'unload**
- File: `custom_components/uconnect_ev_center/__init__.py:341-347` (tupla di rimozione) vs registrazioni a righe 272 (`set_maintenance`), 297 (`refresh_car`), 298 (`set_auto_state`), 304 (`set_schedule`).
- Condizione: rimozione dell'ultima entry.
- Impatto: 4 servizi restano registrati (handlers su `_all_coordinators`, che sarà vuoto → no-op).
- Correzione: aggiungere i 4 nomi alla tupla di rimozione.
- Test: rimuovere l'entry e verificare che `hass.services` non contenga più questi servizi.

**B3 — MEDIA (doc/provenienza) — Link donazione punta a un terzo**
- File: `README.md:25, 322, 604` → `https://www.paypal.me/lamortella`.
- Impatto: le donazioni vanno a una persona estranea al progetto; traccia della sorgente d'origine.
- Correzione: sostituire con il PayPal dell'autore o rimuovere il badge.
- (Non è un problema di sicurezza del software; è correttezza di pubblicazione.)

**B4 — BASSA (asset) — Copia divergente della card**
- File: `www/uconnect-ev-center-card.js` (7.219 B) ≠ `custom_components/uconnect_ev_center/www/uconnect-ev-center-card.js` (8.090 B). Le `dashboards/*` root sono invece **identiche** al pacchetto.
- Impatto: rischio di manutenzione/versioni stantie. Solo la copia nel **pacchetto** è servita a runtime.
- Correzione: eliminare/sincronizzare le copie root.

**B5 — BASSA (i18n) — Step di traduzione morti**
- File: `strings.json` (+ 5 traduzioni) → `config.step.car`, `config.step.wallbox` inutilizzati.
- Correzione: rimuoverli (o reimportarli se previsti).

**B6 — BASSA (tooling) — `check_status.py` non riproducibile su Windows**
- File: `tools/check_status.py` (es. riga 1150) → `UnicodeEncodeError 'charmap'` su console cp1252; e richiede file interni (`agent.md`, `preview/`) assenti nel repo pubblico → **falsi ERR**.
- Impatto: QA locale non affidabile; falsi negativi/positivi.
- Correzione: `sys.stdout.reconfigure(encoding="utf-8")`; rendere opzionali i controlli sui file interni.

---

## 10. Problemi sospetti da verificare

- **S1 — Semantica dei valori**: mappatura chiave↔sensore verificata, ma le **unità/scale/conversioni**
  (W↔kW, %↔kWh, s/min/h, °C) non sono state eseguite su dati reali.
- **S2 — Multi-entry**: i servizi agiscono su **tutte** le entry (`_all_coordinators`). Con ≥2 auto una
  `add_manual_charge`/`add_maintenance` viene applicata a **ogni** auto. Va deciso: accettare `entry_id`
  o documentare l'uso single-car.
- **S3 — Disponibilità per-sorgente**: `available` riflette solo `last_update_success` del coordinator,
  non la disponibilità della singola entità sorgente → possibili valori "vecchi" con auto offline.
- **S4 — Privacy geocoding**: coordinate dei viaggi inviate a OpenStreetMap/Nominatim (di default
  `geocode_enabled=True`). User-Agent impostato, cache su disco, throttle 1.1 s (buone pratiche), ma
  resta un **trasferimento di dati di localizzazione a terzi** da rendere esplicito.
- **S5 — Compatibilità HA 2025.11**: dichiarata, non testata su quell'istanza.

### Bug per gravità (riepilogo)
- Critici: **0**
- Alti: **0**
- Medi: **B1, B3** (+ S2 da decidere)
- Bassi: **B2, B4, B5, B6**

---

## 11. Problemi di sicurezza

Nessun problema di sicurezza del software rilevato. Punti informativi:

- **Nessun segreto** nel codice (grep su `password/token/secret/api_key/bearer/PRIVATE KEY` = 0).
- Log: non vengono loggati token/credenziali; il geocoding logga errori a `debug`.
- Rete: unica chiamata esterna = Nominatim (`coordinator.py:2118`), via `async_get_clientsession`,
  `timeout=6`, User-Agent dichiarato, cache locale, throttle per policy.
- Servizio `set_auto_state` (`__init__.py:158`) imposta lo stato di un'entità arbitraria fornita dal
  chiamante: richiede già l'autorizzazione ai servizi HA; rischio basso, da tenere presente.
- Nessun `eval`/`exec`/shell; export CSV confinato in `config/uconnect_ev_center_export`.
- Privacy: coordinate GPS → terzi (Nominatim) come da S4; presente anche una sezione timeline posizione
  nelle statistiche (solo locale).
- **Attenzione pubblicazione**: link PayPal di terzo (B3) — non è sicurezza tecnica ma va corretto.

---

## 12. Problemi di compatibilità

- `manifest.json`: `config_flow: true`, `iot_class: "calculated"`, `after_dependencies: ["lovelace"]`,
  `requirements: []`, nessuna `dependencies` bloccante → coerente.
- `hacs.json`: `homeassistant: "2025.11.0"`, `render_readme: true` → allineato al README (badge 2025.11+).
- Uso di `homeassistant.data_entry_flow.section` (HA ≥ 2024.4) e `EntitySelector`/`SelectSelector`
  moderni → ok rispetto a 2025.11.
- Nessuna API deprecata evidente (usa `async_track_state_change_event`, `DataUpdateCoordinator`,
  `config_flow` class-based).
- Non testato su HA reale: caricamento, hassfest, HACS action (i workflow li eseguono, non eseguiti qui).

---

## 13. Funzionalità mancanti / incoerenze

1. **Screenshot** README assenti (`docs/screenshots/{it,en,…}`) → immagini rotte.
2. **Localizzazione nomi entità** HA assente (solo pannello multilingua).
3. Copie duplicate/divergenti (card root; dashboards root identiche → ridondanti).
4. STEP di traduzione morti (`config.step.car`/`wallbox`).
5. Link donazione di terzo.

---

## 14. Controlli NON eseguiti (con motivo)

| Controllo | Motivo |
|---|---|
| Caricamento integrazione su HA reale | nessuna istanza HA disponibile |
| Config flow / Options flow (UI) | richiede HA in esecuzione |
| Creazione effettiva entità e attributi | richiede HA in esecuzione |
| Semantica/conversioni valori su dati reali | nessun campione di risposta attendibile |
| Test API/HTTP verso servizi | vietato usare credenziali/dati reali; nessun mock disponibile |
| hassfest | eseguibile solo nelle GitHub Actions |
| HACS validation | eseguibile solo nelle GitHub Actions |
| Lint/build JS (ESLint/TypeScript) | Node.js non presente nell'ambiente |
| `tools/check_status.py` completo | crash per encoding cp1252 (fallback UTF-8 parziale) |

Nessuno di questi controlli è dichiarato "superato".

---

## 15. Elenco correzioni raccomandate

1. `panel.js`: allineare `REC_VER` a `VERSION` (e automatizzarlo nel release).
2. `README.md`: correggere/rimuovere il link PayPal di terzo.
3. `__init__.py`: aggiungere i 4 servizi mancanti alla tupla di rimozione.
4. Decidere il comportamento multi-entry dei servizi (target per entry o documentazione).
5. Sincronizzare/rimuovere le copie root (`www/uconnect-ev-center-card.js`, `dashboards/*`).
6. Rimuovere gli step di traduzione morti.
7. Aggiungere `docs/screenshots/` (o rimuovere i riferimenti).
8. (Opzionale) Localizzare i nomi entità HA con `_attr_translation_key` + sezione `entity`.
9. Rendere `tools/check_status.py` robusto su Windows (UTF-8) e sui file interni opzionali.
10. Documentare il trasferimento coordinate a Nominatim (privacy) e il default `geocode_enabled`.

---

## 16. Piano di risoluzione ordinato per priorità

**P1 — Prima della release**
- B1 (`REC_VER`), B3 (PayPal), B2 (unload servizi).

**P2 — Subito dopo**
- S2 (multi-entry servizi), B4 (copie duplicate), B5 (traduzioni morte), B6 (tooling).

**P3 — Migliorie**
- Screenshot (B4-asset §13.1), localizzazione entità (§13.2), nota privacy (S4), eventuale test HA (S5).

---

## 17. Checklist "pronto alla release"

- [ ] `REC_VER` == `VERSION` (e coerente in `manifest.json`/`CHANGELOG`).
- [ ] Link donazione corretti (nessun riferimento a terzi).
- [ ] Servizi rimossi correttamente all'unload (tutti i registrati).
- [ ] Nessun asset mancante referenziato dal README.
- [ ] Nessuna copia divergente/duplicata di sorgenti.
- [ ] `strings.json` senza step morti; parità lingue OK (già OK).
- [ ] Working tree pulito; tag/release allineati alla versione.
- [ ] Workflow (validate/hassfest + HACS) verdi sul commit di release.

---

## Esito complessivo

# DA CORREGGERE

Non sono stati confermati bug bloccanti: l'integrazione compila, i controlli offline passano e i
sensori risultano collegati alle chiavi dati corrette. Restano **bug non bloccanti** (B1, B2, B3) e
**incoerenze di asset/duplicati** da risolvere prima di considerare la 1.0.0 "pronta". Le verifiche
dipendenti da un'istanza Home Assistant reale **non sono state eseguite** e non vengono dichiarate
superate.

> Fase di sola analisi: **nessuna modifica ai sorgenti** è stata effettuata. In attesa di approvazione
> esplicita prima di applicare le correzioni.

---

## Aggiornamento post-audit — risolto in v1.0.1

Su approvazione, applicate le correzioni (commit successivo a questo report):

| ID | Esito |
|---|---|
| B1 | `REC_VER` (panel) e `CARD_VER` (card) → `1.0.1`; nessun reload spurio, badge corretto |
| B2 | unload: aggiunti `set_maintenance`, `refresh_car`, `set_auto_state`, `set_schedule` alla rimozione |
| B3 | README (IT/EN/FR): rimossi i badge PayPal che puntavano a un terzo |
| B4 | `www/uconnect-ev-center-card.js` riallineata al pacchetto |
| B6 | `tools/check_status.py`: stdout UTF-8 + file interni non più trattati come errori |
| S2 | servizi: targeting opzionale per auto via `entry_id` (retro-compatibile; senza `entry_id` = tutte) |
| §  | versione → `1.0.1` (`VERSION`, `manifest.json`, `CHANGELOG.md`) |

Rimasti come da §13 (non bloccanti, non applicati): **B5** (step di traduzione morti — rumore innocuo) e
**screenshot** `docs/screenshots/` (richiedono immagini dell'utente). **S4** (privacy Nominatim) già
disclosure tramite l'etichetta dell'opzione in configurazione.

**Verifica post-fix:** `py_compile` 17/17 OK · JSON 6/6 OK · `trip_engine` self-check OK ·
`tools/check_status.py` → **TUTTO OK (148 controlli superati)**.

