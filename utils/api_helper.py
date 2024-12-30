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
        data = response.json()
        # Add currency names to the response
        if 'rates' in data:
            currency_names = fetch_currency_names()
            data['currency_names'] = currency_names
        return data
    except Exception as e:
        st.error(f"Error fetching rates: {str(e)}")
        return None

@st.cache_data(ttl=86400)  # Cache for 24 hours
def fetch_currency_names():
    """Fetch all available currency names."""
    try:
        response = requests.get(f"{BASE_URL}/currencies")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching currency names: {str(e)}")
        return {}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_historical_rates(base_currency="USD", days=30):
    """Fetch historical exchange rates using Fixer API."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    historical_data = {'rates': {}}

    try:
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # Use Fixer API for historical data
            response = requests.get(
                f"{FIXER_BASE_URL}/{date_str}",
                params={
                    "access_key": FIXER_API_KEY,
                    "base": "EUR",  # Fixer free tier only supports EUR as base
                    "symbols": "USD,EUR,GBP,JPY,AUD,CAD,CHF,CNY,INR,NZD"
                }
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('success', False) and 'rates' in data:
                    # Convert rates from EUR to desired base currency
                    eur_to_base = data['rates'][base_currency] if base_currency != 'EUR' else 1
                    converted_rates = {
                        curr: rate / eur_to_base
                        for curr, rate in data['rates'].items()
                    }
                    historical_data['rates'][date_str] = converted_rates
                else:
                    st.warning(f"Invalid data received for {date_str}")
            else:
                st.warning(f"Failed to fetch rates for {date_str}")

            current_date += timedelta(days=1)

        if not historical_data['rates']:
            st.error("No historical data available")
            return None

        return historical_data

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching historical data: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None