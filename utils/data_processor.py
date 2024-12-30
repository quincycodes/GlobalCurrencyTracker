import pandas as pd
import streamlit as st

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
        return pd.DataFrame()
    
    data = []
    for date, rates in historical_data['rates'].items():
        data.append({
            'Date': date,
            'Rate': rates[target_currency]
        })
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date')

def get_currency_list():
    """Return a list of common currencies with their names."""
    return {
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'AUD': 'Australian Dollar',
        'CAD': 'Canadian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'INR': 'Indian Rupee',
        'NZD': 'New Zealand Dollar'
    }
