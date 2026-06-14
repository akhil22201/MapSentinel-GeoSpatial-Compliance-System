import streamlit as st
import plotly.express as px


# KPI cards
def show_kpi_cards(full_df, df, summary):

    total_cities = full_df["city"].nunique()

    total_shops = len(full_df)

    illegal_shops = len(df)

    compliance_rate = (
        ((total_shops - illegal_shops) / total_shops) * 100
    )

    total_hotspots = summary["cluster"].nunique()

    largest_cluster = summary["total_violations"].max()

    col1, col2, col3, col4, col5 = st.columns(5)

    cards = [
        (col1, "Cities", total_cities),
        (col2, "Illegal Shops", illegal_shops),
        (col3, "Compliance %", f"{compliance_rate:.1f}"),
        (col4, "Hotspots", total_hotspots),
        (col5, "Largest Cluster", largest_cluster)
    ]

    for col, title, value in cards:

        col.markdown(
            f"""
            <div style="
                background-color:#161B22;
                padding:20px;
                border-radius:14px;
                text-align:center;
                box-shadow:0px 0px 12px rgba(255,255,255,0.08);
            ">

            <div style="font-size:16px;color:#9CA3AF;">
                {title}
            </div>

            <div style="
                font-size:32px;
                color:white;
                font-weight:bold;
            ">
                {value}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


# Charts
def show_charts(df, summary):

    st.subheader("Analytics Dashboard")

    chart1, chart2 = st.columns(2)


    # City-wise violations
    city_counts = (
        df[df["illegal"] == True]
        .groupby("city")
        .size()
        .reset_index(name="violations")
    )

    fig1 = px.bar(
        city_counts,
        x="city",
        y="violations",
        title="City-wise Illegal Shops"
    )

    chart1.plotly_chart(
        fig1,
        use_container_width=True
    )


    # Severity distribution
    severity_counts = (
        df[df["illegal"] == True]["severity"]
        .value_counts()
        .reset_index()
    )

    fig2 = px.pie(
        severity_counts,
        names="severity",
        values="count",
        title="Severity Distribution"
    )

    chart2.plotly_chart(
        fig2,
        use_container_width=True
    )


    # Hotspot ranking
    st.subheader("Top Hotspots")

    rank_fig = px.bar(
        summary.sort_values(
            by="total_violations",
            ascending=False
        ),
        x="cluster",
        y="total_violations",
        color="risk_level",
        title="Hotspot Ranking"
    )

    st.plotly_chart(
        rank_fig,
        use_container_width=True
    )


# ML insights
def show_ml_insights(summary):

    largest_cluster = summary['total_violations'].max()

    largest_cluster_id = (
        summary.loc[
            summary['total_violations'].idxmax(),
            'cluster'
        ]
    )

    total_hotspots = summary["cluster"].nunique()

    st.subheader("Machine Learning Insights")

    st.info(
        f"""
        DBSCAN identified {total_hotspots} major hotspot regions.

        The largest hotspot cluster is Cluster {largest_cluster_id}
        containing {largest_cluster} concentrated violations.

        These hotspots represent dense spatial violation patterns.
        """
    )