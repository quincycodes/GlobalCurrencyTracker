import requests
import streamlit as st
from datetime import datetime, timedelta
import os
import time

BASE_URL = "https://open.er-api.com/v6"
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

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
    """Fetch historical exchange rates using Alpha Vantage API."""
    if not ALPHA_VANTAGE_API_KEY:
        st.error("Alpha Vantage API key is not configured")
        return None

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    historical_data = {'rates': {}}

    try:
        # Alpha Vantage has rate limits, so we'll fetch one currency at a time
        currencies = fetch_currency_names()
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, target_currency in enumerate(list(currencies.keys())[:5]):  # Limit to top 5 currencies due to API limits
            if target_currency == base_currency:
                continue

            status_text.text(f"Fetching {target_currency} rates...")

            # Fetch historical data for currency pair
            params = {
                "function": "FX_DAILY",
                "from_symbol": base_currency,
                "to_symbol": target_currency,
                "apikey": ALPHA_VANTAGE_API_KEY,
                "outputsize": "compact"  # Last 100 data points
            }

            response = requests.get(ALPHA_VANTAGE_URL, params=params)

            if response.status_code == 200:
                data = response.json()

                if "Time Series FX (Daily)" in data:
                    daily_rates = data["Time Series FX (Daily)"]

                    for date_str, values in daily_rates.items():
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        if start_date <= date_obj <= end_date:
                            if date_str not in historical_data['rates']:
                                historical_data['rates'][date_str] = {}

                            rate = float(values['4. close'])
                            historical_data['rates'][date_str][target_currency] = rate
                            # Add base currency rate (always 1.0)
                            historical_data['rates'][date_str][base_currency] = 1.0

                # Respect API rate limits
                time.sleep(12)  # Alpha Vantage free tier allows 5 requests per minute
            else:
                st.warning(f"Failed to fetch rates for {target_currency}: HTTP {response.status_code}")

            progress_bar.progress((i + 1) / 5)

        progress_bar.empty()
        status_text.empty()

        if not historical_data['rates']:
            st.error("No historical data available")
            return None

        return historical_data

    except Exception as e:
        st.error(f"Error fetching historical data: {str(e)}")
        return None