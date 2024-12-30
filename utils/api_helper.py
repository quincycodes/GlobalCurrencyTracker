import requests
import streamlit as st

BASE_URL = "https://open.er-api.com/v6"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_latest_rates(base_currency="EUR"):
    """Fetch latest exchange rates."""
    try:
        response = requests.get(f"{BASE_URL}/latest/{base_currency}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching rates: {str(e)}")
        return None

@st.cache_data(ttl=86400)  # Cache for 24 hours
def fetch_currency_names():
    """Get available currencies from the latest rates."""
    try:
        response = requests.get(f"{BASE_URL}/latest/EUR")
        response.raise_for_status()
        data = response.json()

        if data and 'rates' in data:
            currencies = {
                code: code for code in data['rates'].keys()
            }
            currencies['EUR'] = 'EUR'  # Add base currency
            return currencies
        return {}
    except Exception as e:
        st.error(f"Error fetching currencies: {str(e)}")
        return {}