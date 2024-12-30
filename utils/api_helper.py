import requests
import streamlit as st
from datetime import datetime, timedelta

BASE_URL = "https://open.er-api.com/v6"

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

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_historical_rates(base_currency="USD", days=30):
    """Fetch historical exchange rates by making multiple API calls."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    historical_data = {'rates': {}}
    current_date = start_date

    try:
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # Fetch rates for specific date
            response = requests.get(f"{BASE_URL}/{date_str}/{base_currency}")
            if response.status_code == 200:
                data = response.json()
                if 'rates' in data:
                    historical_data['rates'][date_str] = data['rates']

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