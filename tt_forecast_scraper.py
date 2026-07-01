import streamlit as st
import requests


API_URL = "https://api.open-meteo.com/v1/forecast?latitude=10.4611&longitude=-61.257&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"

HOUR_API_URL = "https://api.open-meteo.com/v1/forecast?latitude=10.4611&longitude=-61.257&hourly=temperature_2m,weather_code,precipitation_probability&models=best_match&timezone=auto&forecast_days=1"

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

    

    try:
        
             
        # Send the GET request directly to your generated URL
        response = requests.get(HOUR_API_URL, timeout=15)

        #Verify if response is 200 OK code or HTTP error occurred
        response.raise_for_status()

        #Package weather data in dictionary
        hour_weather_data = response.json()
        return hour_weather_data
    

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

        

        
if __name__ == "__main__":
    get_forecast()