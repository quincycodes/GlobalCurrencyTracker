import streamlit as st
from components.currency_converter import currency_converter
from components.historical_chart import display_historical_chart
from components.live_rates import display_live_rates
from utils.data_processor import get_currency_list

# Page configuration
st.set_page_config(
    page_title="Currency Dashboard",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply dark theme styles
dark_theme = """
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .currency-card {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border: 1px solid #2D2D2D !important;
    }
    .metric-value {
        color: #00B7FF !important;
    }
    .chart-container {
        background-color: #1E1E1E !important;
    }
    /* Improve mobile visibility */
    .stSelectbox div [data-baseweb="select"] {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #2D2D2D;
        min-height: 45px; /* Better touch targets */
    }
    .stDataFrame {
        color: #FAFAFA;
    }
    div[data-testid="stMarkdownContainer"] {
        color: #FAFAFA;
    }
    .stNumberInput div [data-baseweb="input"] {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #2D2D2D;
        min-height: 45px;
    }
    .stTextInput div [data-baseweb="input"] {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #2D2D2D;
        min-height: 45px;
    }
    /* Mobile-optimized tabs */
    .stTab {
        background-color: #1E1E1E;
        color: #FAFAFA;
        min-height: 50px;
    }
    .stTab[data-baseweb="tab"] {
        color: #FAFAFA;
    }
    .stMarkdown {
        color: #FAFAFA;
    }
    div[data-testid="stToolbar"] {
        background-color: #0E1117;
    }
    .stSlider div[data-testid="stThumbValue"] {
        color: #FAFAFA;
    }
    .stTable {
        background-color: #1E1E1E;
        color: #FAFAFA;
    }
    /* Mobile-optimized containers */
    div.element-container {
        padding: 0.5rem 0;
    }
    /* Better touch targets */
    button {
        min-height: 45px !important;
    }
    /* Improved mobile spacing */
    .main .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }
</style>
"""

# Load dark theme
st.markdown(dark_theme, unsafe_allow_html=True)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main application
st.title("💱 Real-Time Currency Dashboard")

# Currency selection (moved from sidebar to main content)
currencies = get_currency_list()
default_base_index = list(currencies.keys()).index('EUR') if 'EUR' in currencies else 0
base_currency = st.selectbox(
    "Base Currency",
    options=list(currencies.keys()),
    format_func=lambda x: f"{x} - {currencies[x]}",
    index=default_base_index
)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["Live Rates", "Convert", "History"])

with tab1:
    display_live_rates(base_currency)

with tab2:
    currency_converter()

with tab3:
    available_targets = [c for c in currencies.keys() if c != base_currency]
    default_target_index = available_targets.index('USD') if 'USD' in available_targets else 0 if available_targets else 0
    if base_currency == 'USD' and 'EUR' in available_targets:
        default_target_index = available_targets.index('EUR')

    target_currency = st.selectbox(
        "Target Currency",
        options=available_targets,
        format_func=lambda x: f"{x} - {currencies[x]}",
        index = default_target_index
    )
    display_historical_chart(base_currency, target_currency)

# Footer
st.markdown("---")
st.markdown(
    "Data provided by Exchange Rates API | Updated every 5 minutes",
    help="Exchange rates are cached for 5 minutes to optimize performance"
)