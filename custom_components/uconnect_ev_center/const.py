"""Costanti per Uconnect EV Center."""
from __future__ import annotations

DOMAIN = "uconnect_ev_center"

# mesi per il filtro ricariche (indice 0 = "Tutti", così MESI.index() dà il numero del mese)
MESI_FILTRO = ["Tutti", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
               "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
MANUFACTURER = "Uconnect EV Center"
PLATFORMS: list[str] = ["sensor", "binary_sensor", "button", "number", "select", "switch", "time", "device_tracker", "climate"]

# --- chiavi config flow (nucleo veicolo) --------------------------------------
CONF_NAME = "name"
CONF_ODOMETER = "odometer_entity"
CONF_BATTERY_LEVEL = "battery_level_entity"
CONF_RANGE = "range_entity"
CONF_CHARGING_ENTITY = "charging_entity"
CONF_PLUG_ENTITY = "plug_entity"
CONF_LOCATION_ENTITY = "location_entity"

# --- chiavi config flow (entità Uconnect aggiuntive, sezione Veicolo) ---------
# Ricarica
CONF_CHARGER_TYPE = "charger_type_entity"
CONF_TIME_TO_CHARGE_L1 = "time_to_charge_l1_entity"
CONF_TIME_TO_CHARGE_L2 = "time_to_charge_l2_entity"
CONF_TIME_TO_CHARGE_L3 = "time_to_charge_l3_entity"
CONF_CHARGING_RATE = "charging_rate_entity"
CONF_EXTRAPOLATED_BATTERY = "extrapolated_battery_entity"
CONF_CHARGE_SCHEDULE = "charge_schedule_entity"
CONF_12V_BATTERY = "battery_12v_entity"
# Stato veicolo
CONF_IGNITION = "ignition_entity"
CONF_EV_RUNNING = "ev_running_entity"
CONF_DOOR_DRIVER = "door_driver_entity"
CONF_DOOR_PASSENGER = "door_passenger_entity"
CONF_DOOR_REAR_LEFT = "door_rear_left_entity"
CONF_DOOR_REAR_RIGHT = "door_rear_right_entity"
CONF_TRUNK = "trunk_entity"
CONF_WINDOW_DRIVER = "window_driver_entity"
CONF_WINDOW_PASSENGER = "window_passenger_entity"
CONF_TIRE_FL = "tire_pressure_fl_entity"
CONF_TIRE_FR = "tire_pressure_fr_entity"
CONF_TIRE_RL = "tire_pressure_rl_entity"
CONF_TIRE_RR = "tire_pressure_rr_entity"
CONF_TIRE_FL_WARN = "tire_warning_fl_entity"
CONF_TIRE_FR_WARN = "tire_warning_fr_entity"
CONF_TIRE_RL_WARN = "tire_warning_rl_entity"
CONF_TIRE_RR_WARN = "tire_warning_rr_entity"
CONF_HEATED_SEAT = "heated_seat_entity"
CONF_CABIN_COND = "cabin_conditioning_entity"
CONF_SVLA = "stolen_vehicle_entity"
# Termico / altri
CONF_FUEL_AMOUNT = "fuel_amount_entity"
CONF_FUEL_TYPE = "fuel_type_entity"
CONF_LOW_FUEL = "low_fuel_entity"
CONF_RANGE_GAS = "range_gas_entity"
CONF_RANGE_TOTAL = "range_total_entity"
CONF_OIL_LEVEL = "oil_level_entity"
# Manutenzione / diagnostica Uconnect
CONF_DISTANCE_TO_SERVICE = "distance_to_service_entity"
CONF_DAYS_TO_SERVICE = "days_to_service_entity"
CONF_VHR = "vhr_entity"
CONF_MAINTENANCE_HISTORY = "maintenance_history_entity"
# Comandi Uconnect
CONF_SWITCH_CHARGING = "switch_charging_entity"
CONF_SWITCH_ENGINE = "switch_engine_entity"
CONF_SWITCH_PRECONDITION = "switch_precondition_entity"
CONF_SWITCH_HVAC = "switch_hvac_entity"
CONF_SWITCH_COMFORT = "switch_comfort_entity"
CONF_SWITCH_TRUNK = "switch_trunk_entity"
CONF_LOCK_DOORS = "lock_doors_entity"
CONF_BUTTON_CHARGE = "button_charge_entity"
CONF_BUTTON_DEEP_REFRESH = "button_deep_refresh_entity"
CONF_BUTTON_REFRESH_LOCATION = "button_refresh_location_entity"
CONF_BUTTON_LIGHTS = "button_lights_entity"
CONF_BUTTON_LIGHTS_HORN = "button_lights_horn_entity"
CONF_SELECT_CHARGING_LEVEL = "select_charging_level_entity"
CONF_IMAGE = "image_entity"

CONF_WALLBOX_ENABLED = "wallbox_enabled"
# --- profilo di installazione: base (solo auto) · pro (+wallbox) · enterprise (+FV) ---
CONF_PROFILE = "profile"
PROFILE_BASE = "base"
PROFILE_PRO = "pro"
PROFILE_ENTERPRISE = "enterprise"
PROFILES = [PROFILE_BASE, PROFILE_PRO, PROFILE_ENTERPRISE]
DEFAULT_PROFILE = PROFILE_PRO
CONF_WB_POWER = "wallbox_power_entity"
CONF_WB_STATE = "wallbox_state_entity"
CONF_WB_SESSION_ENERGY = "wallbox_session_energy_entity"
CONF_WB_TOTAL_ENERGY = "wallbox_total_energy_entity"
CONF_WB_MAX_CURRENT = "wallbox_max_current_entity"
CONF_WB_SESSION_TIME = "wallbox_session_time_entity"
CONF_WB_TEMP = "wallbox_temp_entity"

CONF_CAPACITY = "battery_capacity"
CONF_TARGET_SOC = "target_soc"
CONF_PRICE_HOME = "price_home"
CONF_PRICE_PUBLIC = "price_public"
CONF_PRICE_SOLAR = "price_solar"
# ricariche fatte PRIMA di installare l'integrazione (per il calcolo dei risparmi)
CONF_PRE_KWH = "pre_kwh"
CONF_PRE_EUR = "pre_eur"
# odometro al momento dell'installazione: baseline del confronto "da installazione"
# (0 = la cattura da sola al primo avvio; serve per auto usate o baseline sbagliata)
CONF_INSTALL_ODO = "install_odo"
CONF_CHARGING_EFFICIENCY = "charging_efficiency"
CONF_POLL_INTERVAL = "poll_interval"
CONF_TRIP_TIMEOUT = "trip_timeout"

# confronto con auto termica (opzionale)
CONF_FUEL_ENABLED = "fuel_comparison"
CONF_FUEL_CONSUMPTION = "fuel_consumption"
CONF_FUEL_PRICE = "fuel_price"
CONF_FUEL_LABEL = "fuel_label"
CONF_DIESEL_PRICE_ENTITY = "diesel_price_entity"

# manutenzione e bollo (per il risparmio netto)
CONF_MAINT_ENABLED = "maint_comparison"
CONF_TAG_TERMICO = "service_cost_thermal"
CONF_TAG_EV = "service_cost_ev"
CONF_BOLLO_TERMICO = "road_tax_thermal"
CONF_BOLLO_EV = "road_tax_ev"
CONF_TAGLIANDO_INTERVALLO = "service_interval_km"
CONF_TYRE_INTERVAL = "tyre_interval_km"
CONF_PURCHASE_DATE = "purchase_date"
DEFAULT_TYRE_INTERVAL = 40000
DEFAULT_TAG_TERMICO = 450.0
DEFAULT_TAG_EV = 100.0
DEFAULT_BOLLO_TERMICO = 350.0
DEFAULT_BOLLO_EV = 150.0
DEFAULT_TAGLIANDO_INTERVALLO = 15000

# notifiche scadenze
CONF_NOTIFY_SERVICE = "notify_service"
CONF_NOTIFY_DAYS = "notify_days"
CONF_TAGLIANDO_MODE = "tagliando_mode"
CONF_TAGLIANDO_DATA = "tagliando_data"
CONF_ASSICURAZIONE_COSTO = "assicurazione_costo"
CONF_ASSICURAZIONE_DATA = "assicurazione_data"
DEFAULT_NOTIFY_DAYS = 30
DEFAULT_ASSICURAZIONE_COSTO = 400.0

# dashboard automatica e modello auto
CONF_CREATE_DASHBOARD = "create_dashboard"
CONF_MODEL = "model"
CONF_POWERTRAIN = "powertrain"  # "BEV" | "PHEV" (auto dal modello, modificabile)
# Solo auto 100% elettriche (BEV) e ibride plug-in (PHEV) dei brand con app Uconnect.
# Niente mild-hybrid (Tonale Hybrid, Ibrida) e niente Peugeot/Citroën/Opel/DS (non Uconnect).
MODELS = ["Jeep Avenger", "Fiat 500e", "Fiat 600e", "Abarth 600e", "Alfa Romeo Junior",
          "Lancia Ypsilon", "Maserati Grecale Folgore", "Ram 1500 REV", "Dodge Charger Daytona",
          "Jeep Renegade 4xe", "Jeep Compass 4xe", "Jeep Grand Cherokee 4xe", "Jeep Wrangler 4xe",
          "Alfa Romeo Tonale", "Custom"]

# notifiche e automazioni ricarica
CONF_NOTIFY_CHARGE_START = "notify_charge_start"
CONF_NOTIFY_CHARGE_END = "notify_charge_end"
CONF_LOW_SOC_ENABLED = "low_soc_enabled"
CONF_LOW_SOC_THRESHOLD = "low_soc_threshold"
CONF_LOW_SOC_START = "low_soc_start"
CONF_LOW_SOC_END = "low_soc_end"
CONF_LOW_SOC_DAYS = "low_soc_days"
CONF_CHARGE_SCHED_ENABLED = "charge_sched_enabled"
CONF_CHARGE_SCHED_MODE = "charge_sched_mode"  # orario | percentuale
CONF_CHARGE_START_TIME = "charge_start_time"
CONF_CHARGE_STOP_TIME = "charge_stop_time"
CONF_CHARGE_START_SOC = "charge_start_soc"
CONF_CHARGE_STOP_SOC = "charge_stop_soc"
CONF_CHARGE_START_BUTTON = "charge_start_button"
CONF_AC_BUTTON = "ac_button_entity"
CONF_CLIMATE_ENTITY = "climate_entity"
CONF_CHARGE_TARGET_NUMBER = "charge_target_number"
CONF_WB_CHARGE_SWITCH = "wb_charge_switch"
CONF_WB_STOP_SWITCH = "wb_stop_switch"
CONF_LIGHT_ENTITY = "light_entity"
CONF_HORN_ENTITY = "horn_entity"
DEFAULT_LOW_SOC_THRESHOLD = 25.0
DEFAULT_LOW_SOC_START = "18:00"
DEFAULT_LOW_SOC_END = "22:00"
DEFAULT_LOW_SOC_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# --- bilanciamento casalingo (potenza casa / contatore) -----------------------
CONF_HOME_POWER_SENSOR = "home_power_sensor"   # sensore consumo casa (W o kW)
CONF_HOME_METER_KW = "home_meter_kw"           # contatore: 3 · 4.5 · 6 · 10 (superiore)
CONF_HOME_MAX_AMPS = "home_max_amps"           # ampere da ripristinare (carico basso)
CONF_HOME_REDUCE_AMPS = "home_reduce_amps"     # ampere da impostare (carico alto)
DEFAULT_HOME_METER_KW = 6.0
DEFAULT_HOME_MAX_AMPS = 25.0
DEFAULT_HOME_REDUCE_AMPS = 18.0
HOME_METER_OPTIONS = ["3", "4.5", "6", "10"]

# profili installazione: minimal (solo auto) · pro (auto+wallbox) · enterprise (+FV)
CONF_HAS_PV = "has_pv"

# --- sperimentazione GSE (limite di potenza a fasce orarie) -------------------
CONF_GSE_WPA = "gse_wpa"                  # watt per ampere della wallbox (230 mono, 690 trifase)
CONF_GSE_KW_MAX = "gse_kw_max"            # potenza consentita nella fascia (es. 6 kW)
CONF_GSE_KW_RIDOTTA = "gse_kw_ridotta"    # potenza fuori fascia (es. 3 kW)
CONF_GSE_START = "gse_start"              # inizio fascia consentita (es. 23:00)
CONF_GSE_END = "gse_end"                  # fine fascia consentita (es. 07:00)
CONF_GSE_DOMENICA = "gse_domenica"        # domenica: tutto il giorno a potenza piena
CONF_GSE_HOLIDAY = "gse_holiday_entity"   # binary_sensor festivi (opzionale)
CONF_GSE_ENABLED = "gse_enabled"          # interruttore generale: attiva/disattiva la sperimentazione
DEFAULT_GSE_WPA = 230.0
DEFAULT_GSE_KW_MAX = 6.0
DEFAULT_GSE_KW_RIDOTTA = 3.0
DEFAULT_GSE_START = "23:00"
DEFAULT_GSE_END = "07:00"
GSE_TOLERANCE = 1.10                     # tolleranza +10% sulla soglia (3/4.5 kW ok sforare)

# bilanciamento solare
CONF_BALANCE_GRID_SENSOR = "balance_grid_sensor"
CONF_BALANCE_BATTERY_SENSOR = "balance_battery_sensor"
CONF_BALANCE_INVERT_GRID = "balance_invert_grid"
CONF_BALANCE_INCLUDE_BATTERY = "balance_include_battery"
CONF_BALANCE_WPA = "balance_watts_per_amp"
CONF_BALANCE_BATTERY_SOC_SENSOR = "balance_battery_soc_sensor"
CONF_BATTERY_PRIORITY_MIN = "battery_priority_min"
DEFAULT_WPA = 230.0 * 3  # monofase 230 V ≈ 690 W/A
DEFAULT_MIN_AMPS = 6.0
DEFAULT_BATTERY_PRIORITY = 80.0
DEFAULT_MAX_AMPS = 16.0
DEFAULT_WB_START_W = 10.0  # soglia: avvia il contatore tempo sessione wallbox
DEFAULT_AVG_KMH = 30.0  # velocità media stimata per l'orario di partenza dei viaggi

# extra: meteo, CO2, scadenze
CONF_TEMP_ENTITY = "temp_entity"
CONF_CO2_ENABLED = "co2_comparison"
CONF_GEOCODE_ENABLED = "geocode_enabled"
CONF_AVG_KMH = "avg_speed_kmh"
CONF_CO2_THERMAL_GKM = "co2_thermal_gkm"
CONF_CO2_GRID_GKWH = "co2_grid_gkwh"
CONF_SCADENZE_ENABLED = "scadenze_enabled"
CONF_SCAD_BOLLO = "scadenza_bollo"
CONF_SCAD_REVISIONE = "scadenza_revisione"
CONF_SCAD_ASSICURAZIONE = "scadenza_assicurazione"
DEFAULT_CO2_THERMAL_GKM = 120.0
DEFAULT_CO2_GRID_GKWH = 300.0

# zona considerata ricarica fotovoltaico/BEB ("beb", nome della tua zona...)
CONF_SOLAR_ZONE = "solar_zone"

# --- valori predefiniti -------------------------------------------------------
DEFAULT_NAME = "Uconnect"
DEFAULT_CAPACITY = 60.0
# capacità di fabbrica (kWh, lorda) per modello: usata come default nel wizard.
# Valori indicativi: l'utente può sempre correggere in Configura → Auto.
MODEL_CAPACITY: dict[str, float] = {
    "Jeep Avenger": 50.8,
    "Fiat 500e": 37.3,
    "Fiat 600e": 50.8,
    "Abarth 600e": 50.8,
    "Alfa Romeo Junior": 50.8,
    "Lancia Ypsilon": 50.8,
    "Maserati Grecale Folgore": 105.0,
    "Ram 1500 REV": 149.0,
    "Dodge Charger Daytona": 100.0,
    "Jeep Renegade 4xe": 11.4,
    "Jeep Compass 4xe": 11.4,
    "Jeep Grand Cherokee 4xe": 17.3,
    "Jeep Wrangler 4xe": 17.3,
    "Alfa Romeo Tonale": 15.5,
}

# Profilo di trazione per modello: BEV (100% elettrica) o PHEV (ibrida plug-in).
MODEL_POWERTRAIN: dict[str, str] = {
    "Jeep Avenger": "BEV", "Fiat 500e": "BEV", "Fiat 600e": "BEV", "Abarth 600e": "BEV",
    "Alfa Romeo Junior": "BEV", "Lancia Ypsilon": "BEV", "Maserati Grecale Folgore": "BEV",
    "Ram 1500 REV": "BEV", "Dodge Charger Daytona": "BEV",
    "Jeep Renegade 4xe": "PHEV", "Jeep Compass 4xe": "PHEV", "Jeep Grand Cherokee 4xe": "PHEV",
    "Jeep Wrangler 4xe": "PHEV", "Alfa Romeo Tonale": "PHEV",
}
DEFAULT_POWERTRAIN = "BEV"
DEFAULT_TARGET_SOC = 80.0
DEFAULT_PRICE_HOME = 0.25
DEFAULT_PRICE_PUBLIC = 0.45
DEFAULT_PRICE_SOLAR = 0.0
DEFAULT_EFFICIENCY = 0.90
DEFAULT_POLL_INTERVAL = 30
DEFAULT_TRIP_TIMEOUT = 20
DEFAULT_FUEL_CONSUMPTION = 6.5
DEFAULT_FUEL_PRICE = 2.0
DEFAULT_FUEL_LABEL = "Diesel"
DEFAULT_SOLAR_ZONE = "beb"

CHARGE_STATE_ON_VALUES = {"on", "charging", "charge_in_progress"}
WALLBOX_CHARGING_STATES = {"charging"}
# stati dell'entità plug_entity che significano "spina collegata" (Uconnect binary_sensor ev_charger + comuni)
PLUG_CONNECTED_VALUES = {"connected", "completed", "plugged", "plugged_in",
                         "cable_connected", "on", "true", "1"}

TRIP_MIN_KM = 0.5
TRIP_MIN_MINUTES = 2
