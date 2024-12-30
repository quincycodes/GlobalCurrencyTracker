import streamlit as st
from utils.api_helper import fetch_latest_rates
from utils.data_processor import get_currency_list

def currency_converter():
    """Display currency converter widget."""
    currencies = get_currency_list()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        from_currency = st.selectbox(
            "From Currency",
            options=list(currencies.keys()),
            format_func=lambda x: f"{x} - {currencies[x]}"
        )
    
    with col2:
        to_currency = st.selectbox(
            "To Currency",
            options=list(currencies.keys()),
            format_func=lambda x: f"{x} - {currencies[x]}",
            index=1
        )
    
    with col3:
        amount = st.number_input("Amount", value=1.0, min_value=0.0)
    
    rates = fetch_latest_rates(from_currency)
    
    if rates and 'rates' in rates:
        conversion_rate = rates['rates'][to_currency]
        converted_amount = amount * conversion_rate
        
        st.markdown(
            f"""
            <div class="currency-card">
                <h3>{amount:.2f} {from_currency} = </h3>
                <div class="metric-value">{converted_amount:.2f} {to_currency}</div>
                <p>1 {from_currency} = {conversion_rate:.4f} {to_currency}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
