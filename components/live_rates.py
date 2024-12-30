import streamlit as st
import plotly.express as px
from utils.api_helper import fetch_latest_rates
from utils.data_processor import prepare_rate_data

def display_live_rates(base_currency):
    """Display live currency rates in a modern dashboard layout."""
    rates_data = fetch_latest_rates(base_currency)
    
    if rates_data:
        df = prepare_rate_data(rates_data)
        
        # Search filter
        search = st.text_input("Search currencies", key="rate_search")
        if search:
            df = df[df['Currency'].str.contains(search.upper())]
        
        # Display rates in a grid
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart for top currencies
            fig = px.bar(
                df.head(10),
                x='Currency',
                y='Rate',
                title=f'Top Currency Rates (Base: {base_currency})',
                color_discrete_sequence=['#0066cc']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Table view
            st.dataframe(
                df,
                column_config={
                    "Currency": "Currency Code",
                    "Rate": st.column_config.NumberColumn(
                        "Exchange Rate",
                        format="%.4f"
                    )
                },
                hide_index=True
            )
