import streamlit as st
import requests
from bs4 import BeautifulSoup

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=10.4611&longitude=-61.257&daily=weather_code,temperature_2m_max,temperature_2m_min&models=gfs_seamless&timezone=auto"

@st.cache_data(ttl=3600)
def get_five_day_forecast():

    """
    Fetches raw JSON data directly from a pre-configured Open-Meteo API URL link.
    """
    try:
        # Send the GET request directly to your generated URL
        response = requests.get(API_URL, timeout=15)

        #Verify if response is 200 OK code or HTTP error occurred
        response.raise_for_status()

        #Package weather data in dictionary
        weather_data = response.json()
        return weather_data

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

@st.cache_data(ttl=3600)
def get_forecast():

    url= "https://www.metoffice.gov.tt/forecast"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:

        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return f"Error: Cannot access webpage (Status Code = {response.status_code})"
        
        soup = BeautifulSoup(response.text, "html.parser")

        #Get date
        forecast_meta_value_list = soup.find_all("span", class_ = "meta-value")
        forecast_date_text = forecast_meta_value_list[1].get_text()
        forecast_date_text = " ".join(forecast_date_text.split())

        # Get bulk of forecast
        forecast_section = soup.find("div", class_= "forecast-text-section")
        forecast_section_text = forecast_section.get_text()
        forecast_section_text = " ".join(forecast_section_text.split())

        #Get high and low temperature at Piarco and Crown Point
        forecast_temps = soup.find_all("td")
        forecast_temps_low_P = forecast_temps[1].get_text()
        forecast_temps_high_P = forecast_temps[4].get_text()
        forecast_temps_low_CP = forecast_temps[2].get_text()
        forecast_temps_high_CP = forecast_temps[5].get_text()

        #Marine forecast
        seas_forecast = soup.find("span", class_ = "weather-marine-value").get_text().lower()
        waters_forecast = soup.find_all("span", class_ = "weather-wave-measurement")
        open_waters_forecast = waters_forecast[0].get_text().lower()
        sheltered_waters_forecast = waters_forecast[1].get_text().lower()

        #Sunrise - Sunset forecast
        sunrise_sunset = soup.find_all("div", class_ = "stat-value")
        sunrise = sunrise_sunset[0].get_text()
        sunset = sunrise_sunset[1].get_text()
        
        #Put full forecast together
        full_forecast_text_1 = forecast_date_text + " " + forecast_section_text + "\n\n"
        temp_forecast = "Forecasted low Temperature at Piarco is "+ forecast_temps_low_P+ " with a forecast high of "+ forecast_temps_high_P +". In Tobago, the low temperature is forecasted to be "+ forecast_temps_low_CP + " and a high temperature of " + forecast_temps_high_CP
        marine_forecast = "\n\nSeas are "+ seas_forecast +" with waves "+ open_waters_forecast + " in open waters and "+ sheltered_waters_forecast + " in sheltered areas"
        sunrise_sunset_forecast ="\n\nSunrise is at "+ sunrise +" and sunset is at "+ sunset

        full_forecast_text = full_forecast_text_1 + temp_forecast + marine_forecast + sunrise_sunset_forecast
        return full_forecast_text

        

    except Exception as e:
         return f"Connection failed: {str(e)}"
    
