import requests
import streamlit as st
from datetime import datetime, timedelta
import os

BASE_URL = "https://open.er-api.com/v6"
FIXER_BASE_URL = "http://data.fixer.io/api"
FIXER_API_KEY = os.environ.get('FIXER_API_KEY')

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_latest_rates(base_currency="USD"):
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
        # Get USD rates as base to get all available currencies
        response = requests.get(f"{BASE_URL}/latest/USD")
        response.raise_for_status()
        data = response.json()

        if 'rates' in data:
            # Create a dictionary of currency codes
            currencies = {
                code: code for code in data['rates'].keys()
            }
            # Add base currency (USD) as it's not in the rates
            currencies['USD'] = 'USD'
            return currencies
        return {}
    except Exception as e:
        st.error(f"Error fetching currencies: {str(e)}")
        return {}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_historical_rates(base_currency="USD", days=30):
    """Fetch historical exchange rates using Fixer API."""
    if not FIXER_API_KEY:
        st.error("Fixer API key is not configured")
        return None

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    historical_data = {'rates': {}}

    try:
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # Use Fixer API for historical data
            url = f"{FIXER_BASE_URL}/{date_str}"
            params = {
                "access_key": FIXER_API_KEY,
                "base": "EUR",  # Fixer free tier only supports EUR as base
                "symbols": base_currency
            }

            if base_currency != "EUR":
                params["symbols"] += ",EUR"

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get('success', False):
                    rates = data.get('rates', {})
                    if base_currency in rates:
                        rate = rates[base_currency]
                        if base_currency == "EUR":
                            historical_data['rates'][date_str] = rates
                        else:
                            # Convert from EUR base to desired base currency
                            converted_rates = {
                                curr: rates[curr] / rate
                                for curr in rates.keys()
                                if curr != base_currency
                            }
                            converted_rates[base_currency] = 1.0
                            historical_data['rates'][date_str] = converted_rates
                    else:
                        st.warning(f"Currency {base_currency} not available for {date_str}")
                else:
                    error_info = data.get('error', {})
                    error_type = error_info.get('type', 'Unknown error')
                    error_info = error_info.get('info', '')
                    st.warning(f"Error for {date_str}: {error_type} - {error_info}")
            except requests.exceptions.RequestException as e:
                st.warning(f"Failed to fetch data for {date_str}: {str(e)}")
                # Add a small delay to respect rate limits
                import time
                time.sleep(1)

            current_date += timedelta(days=1)

        if not historical_data['rates']:
            st.error("No historical data available")
            return None

        return historical_data

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None
