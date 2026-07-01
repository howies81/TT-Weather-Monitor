import streamlit as st
from tt_weather_alert_scraper import check_tt_alerts
from tt_forecast_scraper import get_forecast, get_five_day_forecast
from datetime import datetime, timedelta, timezone

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
        active_watches, active_warnings = check_tt_alerts()
    if active_warnings and len(active_warnings) > 0:
        with st.expander("🚨URGENT WEATHER WARNINGS!!🚨", expanded=True):
            for warning in active_warnings:
                st.error(warning)
    
    if active_watches and len(active_watches) > 0:
        with st.expander("⏳ MONITORING: Upcoming Advisories (Next 7-24 Hours)", expanded=False):
            for watch in active_watches:
                st.info(watch)

    if (not active_watches and not active_warnings) or (active_warnings == [] and active_watches == []):
         st.success("✅ No weather hazards expected over the next 24 hours.")

    st.markdown(f"<span style='font-weight:bold;'> For official weather alerts, check the <a href='https://metoffice.gov.tt/' target='_blank'>Trinidad & Tobago Meteorological Service website</a> </span>", unsafe_allow_html=True)
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
forecast_container = st.empty() #Hourly Forecast container

#Fetch hourly weather data
today_date = datetime.now()
with st.spinner(f"Fetching hourly weather forecast for {today_date.strftime("%a %d %Y")}"):
    hourly_weather_data = get_forecast()
if "error" in hourly_weather_data:
    with forecast_container.container(): 
        st.error(hourly_weather_data["error"])
else:
    with forecast_container.container():
        hours_col = st.columns(8, border=True)
        
        now = datetime.now(timezone(timedelta(hours=-4))) # get current time for Trinidad and Tobago
        
        # 2. Calculate the next immediate hour
        # Replace minutes, seconds, and microseconds with 0, then add 1 hour
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        
        #Get hours time data from API
        hours_data = hourly_weather_data["hourly"]
        hours_time = hours_data["time"]
        hours_weather_code = hours_data["weather_code"]
        hours_temperature = hours_data["temperature_2m"]
        hours_precipitation_prob = hours_data["precipitation_probability"]
        

        hours_list = []
        for i in range(8):
            hours_list.append(next_hour + timedelta(hours=i))
            for j in range(len(hours_time)):
                if hours_list[i].strftime("%I %p") == datetime.strptime(hours_time[j], "%Y-%m-%dT%H:%M").strftime("%I %p"):
                    with hours_col[i]:
                        st.markdown(f"### {hours_list[i].strftime("%I %p")}")
                        hour_weather_assets = WEATHER_INTERPRETATION_MAP.get(hours_weather_code[j], fallback)
                        st.markdown(f"<h1 style='margin:0;'>{hour_weather_assets['emoji']}</h1>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:{hour_weather_assets['color']}; font-weight:bold;'>{hour_weather_assets['desc']}</span>", unsafe_allow_html=True)
                        st.markdown(f"<span style='font-weight:bold;'>Temp: {hours_temperature[j]} C</span>", unsafe_allow_html=True)
                        st.markdown(f"<span>Rain Chance: {hours_precipitation_prob[j]} %</span>", unsafe_allow_html=True)

            
            

    

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



        

    

