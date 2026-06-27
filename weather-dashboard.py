import streamlit as st
from tt_weather_alert_scraper import check_tt_alerts
from tt_forecast_scraper import get_forecast, get_five_day_forecast
from gtts import gTTS
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title= "TT Weather Monitor",
    page_icon= "🌩️",
    layout="wide"
)

sat_view_url = "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=8&overlay=satellite&product=satellite&level=surface&lat=10.359&lon=-61.326&message=true"
rain_view_url = "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=8&overlay=rain&product=ecmwf&level=surface&lat=10.376&lon=-61.405"
rain_acc_url = "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=8&overlay=rainAccu&product=ecmwf&level=surface&lat=10.409&lon=-61.405&message=true"
temp_url = "https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=km/h&zoom=8&overlay=temp&product=ecmwf&level=surface&lat=10.413&lon=-61.302&detailLat=10.653&detailLon=-61.458&marker=true&message=true"

WEATHER_INTERPRETATION_MAP = {
    0:  {"desc": "Sunny / Clear Sky", "emoji": "☀️", "color": "#FFD700"},
    1:  {"desc": "Mainly Clear", "emoji": "🌤️", "color": "#FFE4B5"},
    2:  {"desc": "Partly Cloudy", "emoji": "⛅", "color": "#B0C4DE"},
    3:  {"desc": "Overcast", "emoji": "☁️", "color": "#778899"},
    51: {"desc": "Light Drizzle", "emoji": "🌦️", "color": "#87CEFA"},
    53: {"desc": "Moderate Drizzle", "emoji": "🌦️", "color": "#4682B4"},
    55: {"desc": "Heavy Drizzle", "emoji": "🌧️", "color": "#4169E1"},
    61: {"desc": "Light Rain Showers", "emoji": "🌧️", "color": "#6495ED"},
    63: {"desc": "Moderate Rain", "emoji": "🌧️", "color": "#1E90FF"},
    65: {"desc": "Heavy Continuous Rain", "emoji": "🌧️", "color": "#0000CD"},
    80: {"desc": "Localized Showers", "emoji": "🌦️", "color": "#00BFFF"},
    81: {"desc": "Moderate Showers", "emoji": "🌧️", "color": "#1E90FF"},
    82: {"desc": "Violent Heavy Showers", "emoji": "⛈️", "color": "#8B0000"},
    95: {"desc": "Thunderstorms", "emoji": "🌩️", "color": "#FF4500"}
}

fallback = {"desc": "Variable Weather", "emoji": "🌦️", "color": "#2E8B57"}

st.title("⛅Trinidad & Tobago Weather Monitor🌩️")

alerts_container = st.empty() #Alerts box
with alerts_container.container():
    with st.spinner("Fetching alerts..."):
        ret_string = check_tt_alerts()
    st.info(ret_string)


st.subheader("Current Satellite Outlook")
satellite_container = st.empty() #Satellite Image box

with satellite_container.container():
    sat1_col, sat2_col, sat3_col, sat4_col = st.columns(4)

    
    with sat1_col:
        st.markdown("Trinidad & Tobago Satellite View")
        st.iframe(sat_view_url)

    with sat2_col:
        st.markdown("Trinidad & Tobago Rainfall")
        st.iframe(rain_view_url)

    with sat3_col:
        st.markdown("Trinidad & Tobago Rainfall Accumulation")
        st.iframe(rain_acc_url)

    with sat4_col:
        st.markdown("Trinidad & Tobago Temperature")
        st.iframe(temp_url)

st.subheader("Today's Forecast")
forecast_container = st.empty() #Forecast container
with forecast_container.container():
    fore_col1, fore_col2 = st.columns([2,1])
    with st.spinner("Fetching forecast..."):
        today_forecast = get_forecast()
    with fore_col1:
        if not isinstance(today_forecast, dict):
            st.error(today_forecast)
        else:
            
            forecast_period = today_forecast.get("forecastPeriod", "No forecast period") # -- Time period of forecast
            forecast_Area1 = today_forecast.get("forecastArea1", "No forecast Area") # -- Trinidad & Tobago
            forecast_A1 = today_forecast.get("textArea1", "No forecast") # -- Trinidad & Tobago forecast
            forecast_Area2 = today_forecast.get("forecastArea2","No forecast Area") # -- Windward Islands
            forecast_A2 = today_forecast.get("textArea2", "No forecast") # -- Windward Islands forecast
            forecast_Area3 = today_forecast.get("forecastArea3", "No forecast Area") # -- Leeward Islands
            forecast_A3 = today_forecast.get("textArea3", "No forecast") # -- Leeward Islands forecast
            seas_forecast = today_forecast.get("seas", "No seas forecast") # -- Seas status
            waves_forecast_1 = today_forecast.get("waves1", "No open seas forecast") # -- Waves in open waters forecast
            waves_forecast_2 = today_forecast.get("waves2", "No sheltered seas forecast") # -- Waves in sheltered waters forecast
            trinidad_max_temp = today_forecast.get("PiarcoFcstMxTemp", "No Trinidad Max temperature") # -- Trinidad High Temperature
            tobago_max_temp = today_forecast.get("CrownFcstMxTemp", "No Tobago Max temperature") # -- Tobago High Temperature """

            forecast_period = " ".join(forecast_period.split())
            forecast_Area1 = " ".join(forecast_Area1.split())
            forecast_A1 = " ".join(forecast_A1.split())
            forecast_Area2 = " ".join(forecast_Area2.split())
            forecast_A2 = " ".join(forecast_A2.split())
            forecast_Area3 = " ".join(forecast_Area3.split())
            forecast_A3 = " ".join(forecast_A3.split())
            seas_forecast = " ".join(seas_forecast.split())
            waves_forecast_1 = " ".join(waves_forecast_1.split())
            waves_forecast_2 = " ".join(waves_forecast_2.split())
            trinidad_max_temp = " ".join(trinidad_max_temp.split())
            tobago_max_temp = " ".join(tobago_max_temp.split())

            today_forecast = "For the period "+ forecast_period +" "+ forecast_Area1 +" "+ forecast_A1 + forecast_Area2 +" "+ forecast_A2 + forecast_Area3 +" "+ forecast_A3 + ". Seas are "+ seas_forecast+ ", with waves "+ waves_forecast_1+" in open waters and "+waves_forecast_2+" in sheltered areas"
            today_max_temps = "\n\nThe high temperature in Trinidad is "+ trinidad_max_temp + " deg C and "+tobago_max_temp + " deg C in Tobago"
            today_forecast = today_forecast + today_max_temps
            st.text(today_forecast)

    with fore_col2:
        if not today_forecast.startswith("Connection failed:"):
            st.markdown("Audio forecast")
            audio_buffer = BytesIO()
            tts = gTTS(text=today_forecast, lang="en")
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(audio_buffer, format="audio/mp3")

st.subheader("Five Day Forecast")
five_day_forecast = st.empty() #Five-day forecast container

#Fetch weather data
with st.spinner("Fetching 5 day forecast..."):
    weather_data = get_five_day_forecast()
if "error" in weather_data:
    with five_day_forecast.container(): 
        st.error(weather_data["error"])
else:
    with five_day_forecast.container():
        days = st.columns(5, border=True) #Set placeholders for 5 day forecast
        daily_data = weather_data["daily"]

        for i in range(5):
            raw_date = daily_data["time"][i]
            formatted_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%A")
            daily_weather_code = daily_data["weather_code"][i]
            daily_max_temp = daily_data["temperature_2m_max"][i]
            daily_min_temp = daily_data["temperature_2m_min"][i]

            with days[i]:
                st.markdown(f"### {formatted_date}")
                weather_assets = WEATHER_INTERPRETATION_MAP.get(daily_weather_code, fallback)
                st.markdown(f"<h1 style='margin:0;'>{weather_assets['emoji']}</h1>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:{weather_assets['color']}; font-weight:bold;'>{weather_assets['desc']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold;'>High: {daily_max_temp} C</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold;'>Low: {daily_min_temp} C</span>", unsafe_allow_html=True)



        

    

