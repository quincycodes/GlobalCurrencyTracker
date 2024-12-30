import requests
import streamlit as st
from datetime import datetime, timedelta
import time

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

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_historical_rates(base_currency="EUR", days=30):
    """Fetch historical exchange rates using Exchange Rates API."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    historical_data = {'rates': {}}

    try:
        # Fetch historical data day by day
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            try:
                response = requests.get(f"{BASE_URL}/{date_str}", params={'base': base_currency})
                response.raise_for_status()
                data = response.json()

                if data and 'rates' in data:
                    historical_data['rates'][date_str] = data['rates']
                    historical_data['rates'][date_str][base_currency] = 1.0

                time.sleep(0.2)  # Gentle rate limiting

            except requests.exceptions.RequestException:
                pass  # Skip failed dates silently

            current_date += timedelta(days=1)

        # Only return data if we have at least some historical rates
        if len(historical_data['rates']) > 0:
            return historical_data
        return None

    except Exception as e:
        st.error(f"Error fetching historical data: {str(e)}")
        return None