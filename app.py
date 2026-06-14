import streamlit as st
import pandas as pd

from components.sidebar import show_sidebar
from components.stats import (
    show_kpi_cards,
    show_charts,
    show_ml_insights
)
from components.map_view import show_map


# Page config
st.set_page_config(
    page_title="Geo Compliance Monitoring System",
    page_icon="🌍",
    layout="wide"
)


# Custom styling
st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
    }

    .block-container {
        padding-top: 1rem;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: white;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #A0A0A0;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Load data
@st.cache_data
def load_data():

    df = pd.read_csv("reports/hotspot_output.csv")

    summary = pd.read_csv("reports/hotspot_summary.csv")

    df["illegal"] = (
        df["illegal"]
        .astype(str)
        .str.lower()
        .map({"true": True, "false": False})
    )

    return df, summary


try:
    df, summary = load_data()

    full_df = pd.read_csv("reports/output.csv")

except:
    st.error("Run hotspot_detection.py first")
    st.stop()


# Header
st.markdown(
    """
    <h1 style='
        text-align: center;
        color: white;
        font-size: 48px;
        margin-top: 10px;
        margin-bottom: 0;
        line-height: 1.4;
    '>
        🌍 Geo Compliance Monitoring System
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">ML-Powered Geospatial Violation Detection & Hotspot Analytics</div>',
    unsafe_allow_html=True
)


# Sidebar filters
city_filter, severity_filter, show_heatmap, show_hotspots = show_sidebar(df)


# Apply filters
filtered_df = df[
    (df["city"].isin(city_filter)) &
    (df["severity"].isin(severity_filter))
]


# KPI cards
show_kpi_cards(full_df, filtered_df, summary)


# Map
show_map(
    filtered_df,
    summary,
    show_heatmap,
    show_hotspots
)


# Charts
show_charts(filtered_df, summary)


# ML insights
show_ml_insights(summary)


# Footer
st.markdown("---")

st.markdown(
    """
    <center>
    <h4 style='color:gray;'>
    Built using Python, Streamlit, Folium, Plotly & DBSCAN
    </h4>
    </center>
    """,
    unsafe_allow_html=True
)