import streamlit as st


# Sidebar filters
def show_sidebar(df):

    st.sidebar.title("Filters")

    city_filter = st.sidebar.multiselect(
        "Select Cities",
        options=sorted(df["city"].unique()),
        default=sorted(df["city"].unique())
    )

    severity_filter = st.sidebar.multiselect(
        "Select Severity",
        options=sorted(df["severity"].unique()),
        default=sorted(df["severity"].unique())
    )

    show_heatmap = st.sidebar.checkbox(
        "Show Heatmap",
        value=True
    )

    show_hotspots = st.sidebar.checkbox(
        "Show Hotspots",
        value=True
    )

    return (
        city_filter,
        severity_filter,
        show_heatmap,
        show_hotspots
    )