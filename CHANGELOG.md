# Changelog

Tutte le modifiche rilevanti di **Uconnect EV Center**.

Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/) e il progetto adotta il [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.7] - 2026-10-11

### Modificato
- Calendario ricariche: mostra il mese delle ricariche **filtrate** (segue i filtri tipo/periodo/mese/anno), così anche i mesi vecchi (es. settembre) diventano visibili; rimosso il cambio mese separato (più semplice). Storico ricariche esposto dal sensore: 30 → 120 record.
- Configura: *Chilometri all'attivazione* predefinito **1** (metti **0** per partire dal giorno d'installazione); README aggiornato — 0 = dal giorno d'installazione, 1 = dall'inizio vita auto, auto usata = km alla data d'acquisto.

## [1.0.6] - 2026-10-11

### Aggiunto
- Pannello Ricariche: **calendario mensile** con i kWh per giorno e filtro cliccando una data (mese persistito nel browser).

## [1.0.5] - 2026-10-11

### Aggiunto
- Indirizzo dell'auto nelle ricariche (via/paese dall'OpenStreetMap `geocoding`), mostrato nella tabella ricariche del pannello.
- Fusione automatica delle ricariche frammentate della **stessa sessione** (stessa zona, entro 360 s, nessun viaggio nel mezzo), con azione **Separa** (✂️) per annullarla. Opzione in Configura («Unisci ricariche frammentate»).
- Ricerca testuale nello storico ricariche (filtro client, persistito nel browser).
- Diagnostica scaricabile (Download diagnostics) con esito ultimo aggiornamento, stato sorgenti, ultimo errore di rete e statistiche geocoding — valori sensibili oscurati.

### Corretto
- Ricariche: la sessione **non viene più chiusa mentre la spina è ancora collegata** (la wallbox in pausa/load-balancing non spezzetta più una singola ricarica in tante sessioni). La chiusura avviene ora o **staccando la spina** oppure quando la **wallbox segnala "ricarica finita"** (utile alle colonnine pubbliche, dove la spina resta inserita): lo stacco spina resta la *guard* anti-spezzettamento.

## [1.0.4] - 2026-10-11

### Aggiunto
- Ricariche manuali: compaiono subito dopo l'inserimento, campo **Durata (min)** opzionale e azioni **modifica** (✏️) / **elimina** (🗑) sui record manuali (servizi `update_charge`, `delete_charge`).
- Risparmi: il **prezzo carburante** è salvato **giorno per giorno**; ogni periodo (totale/mese/anno) usa la **media pesata sui km** dei prezzi dei suoi giorni, così il prezzo di oggi non riscrive più i periodi passati.

### Corretto
- Viaggi: il delta batteria è ricostruito dai kWh quando il cloud Uconnect non aggiorna il SoC a fine viaggio (record coerenti: niente più `batteria_inizio == batteria_fine`).
- Percorrenza: gli "usati" (kWh) usano i kWh reali dei viaggi, non più 0 quando il delta batteria risulta nullo.
- Risparmi: il **totale** non può essere inferiore ai km realmente tracciati (non più sotto il mensile).
- Grafico Km (7 giorni): la linea "Media Consumi" usa il consumo **giornaliero reale** (pesato sui km) e non crolla più nei giorni a 0 km.

### Modificato
- Bollo EV predefinito **0 €/anno** (esenzione tipica EV in Italia; il termico resta 350).
- README: spiegazione dei km del confronto (campo *Chilometri all'attivazione*) e integrazione **Fuel Prices Italy** (open data MIMIT) consigliata per gli utenti italiani.

## [1.0.3] - 2026-10-10

### Modificato
- Configura: rimosso il campo inutile "Immagine veicolo" (la foto auto dipende solo dal modello).
- Configura: "Avvia A/C" rinominato "Avvia preriscaldamento"; luci esterne, clacson e number target di carica ora marcati come opzionali.
- Configura: confronto CO2 e confronto costi manutenzione attivi di default; costo tagliando EV predefinito 100 €/anno; costo diesel predefinito 2,0 €/l.
- Configura: la sperimentazione GSE ha un interruttore per attivarla/disattivarla.
- Configura: "Ultimo cambio (km)" non più precompilato (default 0), niente più valore gonfiato.
- Pannello Panoramica: clacson e luci lampeggianti nascosti se non mappati.
- Pannello Wallbox: stati tradotti (anche `free`); potenza del sensore convertita W→kW; corrente ricavata da potenza/tensione se manca il sensore.
- Pannello Automazioni: automazioni omonime raggruppate in una riga (niente doppioni).
- Notifiche: il servizio notify del pannello ora viene salvato nella config dell'integrazione (servizio `set_notify_service`).
- README e guide: nota sul riavvio di Home Assistant dopo la prima configurazione.

## [1.0.2] - 2026-10-10

### Modificato
- Statistiche: la colonna della batteria fotovoltaica è ora etichettata **"Batteria FV"** (storico mensile e percorrenza).

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
