import streamlit as st
import requests
import json


API_URL = "https://api.open-meteo.com/v1/forecast?latitude=10.4611&longitude=-61.257&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"

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

    url= "https://metproducts.gov.tt/api/forecast"

    try:

        response = requests.get(url, timeout=15)
        
        if response.status_code != 200:
            return f"Error: Cannot access webpage (Status Code = {response.status_code})"
        
        #soup = BeautifulSoup(response.text, "html.parser")
        root = response.content
        clean_root = json.loads(root.decode("utf-8"))
        #print(clean_root)
        if clean_root is not None:
            forecast_data = clean_root['items'][0]# Convert text to Python dictionary
            #print(forecast_data)
            # Get bulk of forecast
            """
            forecast_period = forecast_data.get("forecastPeriod", "No forecast period") # -- Time period of forecast
            forecast_Area1 = forecast_data.get("forecastArea1", "No forecast Area") # -- Trinidad & Tobago
            forecast_A1 = forecast_data.get("textArea1", "No forecast") # -- Trinidad & Tobago forecast
            forecast_Area2 = forecast_data.get("forecastArea2","No forecast Area") # -- Windward Islands
            forecast_A2 = forecast_data.get("textArea2", "No forecast") # -- Windward Islands forecast
            forecast_Area3 = forecast_data.get("forecastArea3", "No forecast Area") # -- Leeward Islands
            forecast_A3 = forecast_data.get("textArea3", "No forecast") # -- Leeward Islands forecast
            seas_forecast = forecast_data.get("seas", "No seas forecast") # -- Seas status
            waves_forecast_1 = forecast_data.get("waves1", "No open seas forecast") # -- Waves in open waters forecast
            waves_forecast_2 = forecast_data.get("waves2", "No sheltered seas forecast") # -- Waves in sheltered waters forecast
            trinidad_max_temp = forecast_data.get("PiarcoFcstMxTemp", "No Trinidad Max temperature") # -- Trinidad High Temperature
            tobago_max_temp = forecast_data.get("CrownFcstMxTemp", "No Tobago Max temperature") # -- Tobago High Temperature """
             
            
            return forecast_data

        

    except Exception as e:
         return f"Connection failed: {str(e)}"
    
if __name__ == "__main__":
    get_forecast()