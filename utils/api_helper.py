import requests
import streamlit as st
from datetime import datetime, timedelta
import os
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
        # Get EUR rates as base to get all available currencies
        response = requests.get(f"{BASE_URL}/latest/EUR")
        response.raise_for_status()
        data = response.json()

        if 'rates' in data:
            # Create a dictionary of currency codes
            currencies = {
                code: code for code in data['rates'].keys()
            }
            # Add base currency (EUR) as it's not in the rates
            currencies['EUR'] = 'EUR'
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
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # Fetch historical data for the date
            response = requests.get(f"{BASE_URL}/{date_str}", params={'base': base_currency})

            if response.status_code == 200:
                data = response.json()
                if 'rates' in data:
                    historical_data['rates'][date_str] = data['rates']
                    historical_data['rates'][date_str][base_currency] = 1.0

            # Move to next date
            current_date += timedelta(days=1)
            time.sleep(0.5)  # Rate limiting

        if not historical_data['rates']:
            return None

        return historical_data

    except Exception as e:
        st.error(f"Error fetching historical data: {str(e)}")
        return None