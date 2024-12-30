import requests
import streamlit as st
from datetime import datetime, timedelta

BASE_URL = "https://open.er-api.com/v6"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_latest_rates(base_currency="USD"):
    """Fetch latest exchange rates."""
    try:
        response = requests.get(f"{BASE_URL}/latest/{base_currency}")
        response.raise_for_status()  # Raise an exception for bad status codes
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
        # Modified to use the correct endpoint format
        response = requests.get(
            f"{BASE_URL}/history",
            params={
                "base": base_currency,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d")
            }
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        # Add debug logging
        if response.status_code != 200:
            st.error(f"API Response Status: {response.status_code}")
            st.error(f"API Response Text: {response.text}")
            return None

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching historical data: {str(e)}")
        return None
    except ValueError as e:
        st.error(f"Error parsing JSON response: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None