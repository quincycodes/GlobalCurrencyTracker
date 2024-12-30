import requests
import streamlit as st
from datetime import datetime, timedelta

BASE_URL = "https://open.er-api.com/v6"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_latest_rates(base_currency="USD"):
    """Fetch latest exchange rates."""
    try:
        response = requests.get(f"{BASE_URL}/latest/{base_currency}")
        return response.json()
    except Exception as e:
        st.error(f"Error fetching rates: {str(e)}")
        return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_historical_rates(base_currency="USD", days=30):
    """Fetch historical exchange rates."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        response = requests.get(
            f"{BASE_URL}/time-series",
            params={
                "base": base_currency,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
            }
        )
        return response.json()
    except Exception as e:
        st.error(f"Error fetching historical data: {str(e)}")
        return None
