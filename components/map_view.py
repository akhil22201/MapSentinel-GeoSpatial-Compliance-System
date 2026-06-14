import streamlit as st
import folium

from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium


# Interactive map
def show_map(
    filtered_df,
    summary,
    show_heatmap,
    show_hotspots
):

    st.subheader("Interactive Geo Analytics Map")

    # Prevent white flash behind map
    st.markdown(
        """
        <style>
        iframe {
            background-color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create map
    m = folium.Map(
        location=[22.97, 78.65],
        zoom_start=5,
        tiles="CartoDB dark_matter"
    )

    # Clusters
    safe_cluster = MarkerCluster(
        name="Safe Shops"
    ).add_to(m)

    illegal_cluster = MarkerCluster(
        name="Illegal Shops"
    ).add_to(m)


    # Add markers
    for _, row in filtered_df.iterrows():

        color = "green"

        if row["illegal"]:

            if row["severity"] == "High":
                color = "darkred"

            elif row["severity"] == "Medium":
                color = "orange"

            else:
                color = "red"

        popup_html = f"""
        <div style='width:250px;'>

        <h4>{row['name']}</h4>

        <b>City:</b> {row['city']}<br><br>

        <b>Status:</b>
        {'Illegal' if row['illegal'] else 'Safe'}
        <br><br>

        <b>Severity:</b> {row['severity']}<br><br>

        <b>Hotspot:</b>
        {row['hotspot_type']}
        <br><br>

        <b>Nearest School:</b>
        {row['nearest_school_distance']} m
        <br><br>

        <b>Nearest Temple:</b>
        {row['nearest_temple_distance']} m

        </div>
        """

        marker = folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(
                popup_html,
                max_width=300
            )
        )

        if row["illegal"]:
            marker.add_to(illegal_cluster)

        else:
            marker.add_to(safe_cluster)


    # Heatmap
    if show_heatmap:

        heat_data = filtered_df[
            filtered_df["illegal"] == True
        ][["lat", "lon"]].values.tolist()

        HeatMap(
            heat_data,
            radius=18,
            blur=15,
            min_opacity=0.4,
            name="Violation Heatmap"
        ).add_to(m)


    # Hotspot circles
    if show_hotspots:

        for _, row in summary.iterrows():

            risk_color = "yellow"

            if row["risk_level"] == "High Risk":
                risk_color = "red"

            elif row["risk_level"] == "Medium Risk":
                risk_color = "orange"

            folium.Circle(
                location=[row["avg_lat"], row["avg_lon"]],
                radius=row["total_violations"] * 120,
                color=risk_color,
                fill=True,
                fill_color=risk_color,
                fill_opacity=0.25,
                weight=3,
                popup=f"""
                <b>Hotspot Cluster:</b> {row['cluster']}<br>
                <b>Violations:</b> {row['total_violations']}<br>
                <b>Risk Level:</b> {row['risk_level']}<br>
                <b>Cities:</b> {row['cities']}
                """
            ).add_to(m)


    # Layer controls
    folium.LayerControl(
        position='topleft'
    ).add_to(m)


    # Render map
    st_folium(
    m,
    width=None,
    height=700,
    use_container_width=True
)