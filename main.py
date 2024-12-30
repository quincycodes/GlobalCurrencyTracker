import streamlit as st
from components.currency_converter import currency_converter
from components.historical_chart import display_historical_chart
from components.live_rates import display_live_rates
from utils.data_processor import get_currency_list

# Page configuration
st.set_page_config(
    page_title="Currency Dashboard",
    page_icon="💱",
    layout="wide"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main application
st.title("💱 Real-Time Currency Dashboard")

# Sidebar for base currency selection
currencies = get_currency_list()
base_currency = st.sidebar.selectbox(
    "Select Base Currency",
    options=list(currencies.keys()),
    format_func=lambda x: f"{x} - {currencies[x]}"
)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["Live Rates", "Currency Converter", "Historical Charts"])

with tab1:
    display_live_rates(base_currency)

with tab2:
    currency_converter()

with tab3:
    target_currency = st.selectbox(
        "Select Target Currency",
        options=[c for c in currencies.keys() if c != base_currency],
        format_func=lambda x: f"{x} - {currencies[x]}"
    )
    display_historical_chart(base_currency, target_currency)

# Footer
st.markdown("---")
st.markdown(
    "Data provided by Exchange Rates API | Updated every 5 minutes",
    help="Exchange rates are cached for 5 minutes to optimize performance"
)
