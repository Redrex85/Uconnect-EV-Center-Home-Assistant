# Changelog

Tutte le modifiche rilevanti di **Uconnect EV Center**.

Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/) e il progetto adotta il [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.1] - 2026-10-10

### Corretto
- Pannello: `REC_VER` allineata alla versione dell'integrazione (niente reload spurio, badge versione corretto).
- Rimozione completa dei servizi all'unload (mancavano `set_maintenance`, `refresh_car`, `set_auto_state`, `set_schedule`).
- Servizi: targeting opzionale per singola auto via `entry_id` (con più di un veicolo non agiscono più su tutti).
- README: rimosso il link di donazione che puntava a un terzo.
- Copia della card JS nella radice riallineata a quella del pacchetto.
- `tools/check_status.py`: esecuzione affidabile su Windows (UTF-8) e file interni non più segnalati come errori.

## [1.0.0] - 2026-10-10

### Aggiunto
- Prima release di **Uconnect EV Center**, *companion* delle auto Stellantis con **Uconnect** (costruito sopra l'integrazione [`hass-uconnect`](https://github.com/hass-uconnect/hass-uconnect)).
- Vista **Veicolo (Uconnect)**: stato auto (accensione, portiere, finestrini, baule, antifurto SVLA), pneumatici (pressioni + avvisi), ricarica (tipo colonnina, tempo L1/L2/L3, batteria stimata), termico (carburante, autonomia), diagnostica/service e **comandi rapidi** (precondiziona, HVAC, comfort, avvia carica, deep refresh, aggiorna posizione, luci, luci+clacson, blocco porte).
- **Mappatura guidata** delle entità Uconnect: ricarica, stato, termico, service, comandi e immagine veicolo (tutte opzionali).
- Viaggi automatici, ricariche, statistica, risparmi vs termica, salute batteria, manutenzione e automazioni integrate.
- Pannello web in **5 lingue** (it / en / fr / de / es); documentazione in italiano, inglese e francese.

### Note
- Progetto *companion* autonomo per le auto Stellantis con Uconnect.
</content>
