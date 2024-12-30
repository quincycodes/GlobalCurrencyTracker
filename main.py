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

# Theme selection
theme = st.sidebar.selectbox(
    "Choose Theme",
    ["Light", "Dark"],
    key="theme_selector"
)

# Apply theme-specific styles
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
    /* Improve text visibility */
    .stSelectbox div [data-baseweb="select"] {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #2D2D2D;
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
    }
    .stTextInput div [data-baseweb="input"] {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #2D2D2D;
    }
    /* Additional dark theme improvements */
    .stTab {
        background-color: #1E1E1E;
        color: #FAFAFA;
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
</style>
"""

light_theme = """
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #262730;
    }
    .currency-card {
        background-color: white !important;
        color: #262730 !important;
    }
    .metric-value {
        color: #0066cc !important;
    }
    .chart-container {
        background-color: white !important;
    }
</style>
"""

# Load theme-specific CSS
if theme == "Dark":
    st.markdown(dark_theme, unsafe_allow_html=True)
else:
    st.markdown(light_theme, unsafe_allow_html=True)

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