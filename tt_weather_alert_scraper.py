import streamlit as st
import requests

ALERT_URL = "https://api.open-meteo.com/v1/forecast?latitude=10.461&longitude=-61.257&hourly=precipitation,wind_speed_10m,wind_gusts_10m&models=best_match&timezone=auto&forecast_days=1"
@st.cache_data(ttl=1800)
def check_tt_alerts():
    found_watches = []
    found_warnings = []
    try:

        response = requests.get(ALERT_URL, timeout=15)

        response.raise_for_status()

        alert_data = response.json()

        # Get weather data for next 24 hrs ---
        hourly = alert_data.get("hourly",{})
        rain_data = hourly.get("precipitation", [])
        wind_speed_data = hourly.get("wind_speed_10m", [])
        wind_gust_data = hourly.get("wind_gusts_10m", [])

        # Rain warning data
        rain_warning = rain_data[:6]

        #Rain watch data
        rain_watch = rain_data[6:24]

        rain_warning_total =sum(rain_warning)
        rain_warning_max = max(rain_warning)
        rain_watch_total = sum(rain_watch)
        rain_watch_max = max(rain_watch)

        # Wind speed warning data
        wind_speed_warning = wind_speed_data[:6]

        # Wind speed watch data
        wind_speed_watch = wind_speed_data[6:24]

        #Wind gust warning data
        wind_gust_warning = wind_gust_data[:6]

        #Wind gust watch data
        wind_gust_watch = wind_gust_data[6:24]

        
        wind_speed_warning_max = max(wind_speed_warning)
        wind_speed_watch_max = max(wind_speed_watch)
        wind_gust_warning_max = max(wind_gust_warning)
        wind_gust_watch_max = max(wind_gust_watch)

        # --- RAIN WARNING CHECKS-----
        if rain_warning_total == 100 or rain_warning_total > 100:
            found_warnings.append("** ADVERSE WEATHER ALERT: 🚨 RED LEVEL: ** Torrential downpours are imminent. Expect flash flooding in low-lying areas shortly.")
        elif rain_warning_total > 75 or rain_warning_max > 25:
            found_warnings.append("** ADVERSE WEATHER ALERT: 🟧 ORANGE LEVEL: ** Severe threat of flash flooding and landslips.")
        elif rain_warning_total > 50 or rain_warning_max > 15:
            found_warnings.append("** ADVERSE WEATHER ALERT: 🟨 YELLOW LEVEL: ** Isolated street/flash flooding likely in low-lying areas.")
        
        #---- WIND WARNING CHECKS-----
        if wind_gust_warning_max > 75:
            found_warnings.append("** WIND ALERT: 🚨 RED LEVEL: ** Destructive gusts >75 km/h likely.")
        elif wind_gust_warning_max > 55 or wind_speed_warning_max > 45:
            found_warnings.append("** WIND ALERT: 🟧 ORANGE LEVEL: ** Structural damage and falling trees possible.")
        elif wind_gust_warning_max > 44 or wind_speed_warning_max > 34:
            found_warnings.append("** WIND ALERT: 🟨 YELLOW LEVEL: ** Strong gusts accompanying showers.")

        #---RAIN WATCH CHECKS -----
        if rain_watch_total == 100 or rain_watch_total > 100:
            found_watches.append("⏳ **Flood Watch:** A heavy prolonged rainfall system is modeled to move in later today/tonight. Flash flooding in low-lying areas is expected.")
        elif rain_watch_total > 75 or rain_watch_max > 25:
            found_watches.append("⏳ **Weather Watch:** Increased tropical moisture and widespread showers are expected later in the forecast period. Saturated soils may trigger landslips")
        elif rain_watch_total > 50 or rain_watch_max > 15:
            found_watches.append("⏳ **Weather Watch:** Increased tropical moisture and widespread showers are expected later in the forecast period.")

        # ---WIND WATCH CHECKS -----
        if wind_gust_watch_max > 44 or wind_speed_watch_max > 34:
            found_watches.append(f"⏳ **High Wind Watch:** Wind models show strong gust capabilities ({wind_gust_watch_max:.1f} km/h) developing later in the cycle.")


        return found_watches, found_warnings
        
    except requests.exceptions.HTTPError as http_err:
        return [], []
    except Exception as err:
        return [], []
    
