import pandas as pd
import streamlit as st
from utils.api_helper import fetch_currency_names

def prepare_rate_data(rates_data):
    """Transform raw rates data into a pandas DataFrame."""
    if not rates_data or 'rates' not in rates_data:
        return pd.DataFrame()

    df = pd.DataFrame(rates_data['rates'].items(), columns=['Currency', 'Rate'])
    df['Rate'] = pd.to_numeric(df['Rate'])
    return df

@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_currency_list():
    """Return a dictionary of all available currencies."""
    currencies = fetch_currency_names()
    if not currencies:
        # Fallback to basic list if API fails
        currencies = {
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'JPY': 'Japanese Yen',
            'AUD': 'Australian Dollar'
        }
    return currencies