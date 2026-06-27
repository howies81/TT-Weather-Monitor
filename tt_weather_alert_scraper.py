import streamlit as st
import requests
from bs4 import BeautifulSoup

@st.cache_data(ttl=600)
def check_tt_alerts():

    url= "https://www.metoffice.gov.tt/alert"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return f"Error: Cannot access webpage (Status Code = {response.status_code})"
        
        soup = BeautifulSoup(response.text, "html.parser")

        found_threats = []
        active_tables = soup.find_all("table")
        page_text = soup.find_all(["h1", "h2", "h3"])
        for header in page_text:
            text = header.get_text(strip=True)
            
            if "level" in text or "adverse" in text or "hazardous" in text or "warning" in text:
                    found_threats.append(header.get_text(strip=True))
                
        # 3. Decision Logic: If warning structures exist, parse them. Otherwise, it is safe.
        if len(active_tables) > 0 or len(found_threats) > 0:
            print("🚨 Warning markers detected in the HTML markup!")
            if found_threats:
                return f"⚠️ Active Alert: {', '.join(found_threats)}"
            return "⚠️ Active warning tables detected on the webpage. Please check metoffice.gov.tt/alert."
            
        else:
            # If no warning tables, rows, or alert headings exist, the layout is clear
            return "🟢 Green Level: There are currently no active weather alerts for Trinidad & Tobago."
        
    except Exception as e:
        return f"Connection failed: {str(e)}"
    
