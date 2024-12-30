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

def prepare_historical_data(historical_data, target_currency):
    """Transform historical data into a format suitable for plotting."""
    if not historical_data or 'rates' not in historical_data:
        return pd.DataFrame(columns=['Date', 'Rate'])

    data = []
    for date, rates in historical_data['rates'].items():
        if target_currency in rates:
            data.append({
                'Date': pd.to_datetime(date),
                'Rate': float(rates[target_currency])
            })

    if not data:
        return pd.DataFrame(columns=['Date', 'Rate'])

    df = pd.DataFrame(data)

    # Ensure proper column types
    df['Date'] = pd.to_datetime(df['Date'])
    df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')

    # Drop any rows with NaN values
    df = df.dropna()

    # Sort by date and reset index
    df = df.sort_values('Date').reset_index(drop=True)

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