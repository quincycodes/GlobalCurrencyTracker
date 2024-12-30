import streamlit as st
import plotly.express as px
from utils.api_helper import fetch_historical_rates
from utils.data_processor import prepare_historical_data

def display_historical_chart(base_currency, target_currency):
    """Display historical exchange rate chart."""
    # Time period selector
    period = st.select_slider(
        "Select Time Period",
        options=[7, 14, 30, 60, 90],
        value=30,
        format_func=lambda x: f'{x} days'
    )

    historical_data = fetch_historical_rates(base_currency, period)

    if historical_data:
        df = prepare_historical_data(historical_data, target_currency)

        # Use theme-aware colors
        is_dark_theme = st.session_state.get('theme_selector') == 'Dark'

        fig = px.line(
            df,
            x='Date',
            y='Rate',
            title=f'{base_currency}/{target_currency} Exchange Rate History',
            template='plotly_dark' if is_dark_theme else 'plotly_white'
        )

        fig.update_traces(
            line_color='#00B7FF' if is_dark_theme else '#0066cc'
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=f"Rate ({target_currency})",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)