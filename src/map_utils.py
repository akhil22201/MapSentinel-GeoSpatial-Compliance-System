import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap, Fullscreen
from src.config import OUTPUT_PATH


def load_data(path):
    df = pd.read_csv(path)

    # convert illegal column safely
    df["illegal"] = (
        df["illegal"]
        .astype(str)
        .str.lower()
        .map({"true": True, "false": False})
    )

    return df


def get_color(row):
    if row["illegal"]:
        if row["severity"] == "High":
            return "darkred"
        elif row["severity"] == "Medium":
            return "orange"
        else:
            return "red"

    return "green"


def create_map():
    return folium.Map(
        location=[22.97, 78.65],   # India center
        zoom_start=5,
        tiles="CartoDB dark_matter"
    )


def styled_popup(row):

    status_color = "red" if row["illegal"] else "green"
    status_text = "Illegal" if row["illegal"] else "Safe"

    html = f"""
    <div style="
        width:260px;
        font-family:Arial;
    ">

        <h3 style="
            margin-bottom:8px;
            color:#2E86C1;
        ">
            {row['name']}
        </h3>

        <hr>

        <b>City:</b> {row['city']}<br><br>

        <b>Status:</b>
        <span style="
            color:{status_color};
            font-weight:bold;
        ">
            {status_text}
        </span>

        <br><br>

        <b>Violation:</b> {row['violation_reason']}<br><br>

        <b>Severity:</b>
        <span style="font-weight:bold;">
            {row['severity']}
        </span>

        <hr>

        <b>Nearest School:</b><br>
        {row['nearest_school_name']}<br>
        Distance: {row['nearest_school_distance']} m

        <br><br>

        <b>Nearest Temple:</b><br>
        {row['nearest_temple_name']}<br>
        Distance: {row['nearest_temple_distance']} m

    </div>
    """

    return folium.Popup(html, max_width=300)


def add_markers(map_obj, df):

    safe_cluster = MarkerCluster(
        name="Safe Shops"
    ).add_to(map_obj)

    illegal_cluster = MarkerCluster(
        name="Illegal Shops"
    ).add_to(map_obj)

    for _, row in df.iterrows():

        marker = folium.Marker(
            location=[row["lat"], row["lon"]],

            popup=styled_popup(row),

            tooltip=f"""
            {row['name']} ({row['city']})
            """,

            icon=folium.Icon(
                color=get_color(row),

                icon=(
                    "warning-sign"
                    if row["illegal"]
                    else "ok-sign"
                )
            )
        )

        if row["illegal"]:
            marker.add_to(illegal_cluster)
        else:
            marker.add_to(safe_cluster)


def add_heatmap(map_obj, df):

    illegal_df = df[df["illegal"] == True]

    if illegal_df.empty:
        return

    heat_data = illegal_df[
        ["lat", "lon"]
    ].values.tolist()

    HeatMap(
        heat_data,

        name="Violation Heatmap",

        radius=18,

        blur=15,

        min_opacity=0.4
    ).add_to(map_obj)


def add_legend(map_obj):

    legend_html = """
    <div style="
        position: fixed;
        bottom: 40px;
        left: 40px;
        width: 220px;
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        z-index:9999;
        font-size:14px;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
    ">

    <h4 style="margin-top:0;">
        Map Legend
    </h4>

    🔴 High Risk Illegal<br><br>

    🟠 Medium Risk Illegal<br><br>

    🟢 Safe Shop<br><br>

    🔥 Heatmap = Violation Density

    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(legend_html)
    )


def add_stats_panel(map_obj, df):

    total = len(df)

    illegal = int(df["illegal"].sum())

    safe = total - illegal

    compliance = (
        (safe / total) * 100
        if total > 0
        else 0
    )

    city_count = df["city"].nunique()

    stats_html = f"""
    <div style="
        position: fixed;
        top: 90px;
        right: 40px;
        width: 260px;
        background-color: white;
        border-radius: 12px;
        padding: 18px;
        z-index:9999;
        box-shadow: 0 0 20px rgba(0,0,0,0.35);
        font-family: Arial;
    ">

    <h3 style="
        margin-top:0;
        color:#2E86C1;
    ">
        Geo Compliance Dashboard
    </h3>

    <hr>

    <b>Total Cities:</b> {city_count}<br><br>

    <b>Total Shops:</b> {total}<br><br>

    <b>Illegal Shops:</b>
    <span style="color:red;font-weight:bold;">
        {illegal}
    </span>

    <br><br>

    <b>Safe Shops:</b>
    <span style="color:green;font-weight:bold;">
        {safe}
    </span>

    <br><br>

    <b>Compliance Rate:</b>
    <span style="font-weight:bold;">
        {compliance:.2f}%
    </span>

    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(stats_html)
    )


def add_title(map_obj):

    title_html = """
    <div style="
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        z-index:9999;
        background-color: rgba(0,0,0,0.85);
        color: white;
        padding: 12px 25px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0,0,0,0.4);
    ">
        Geo Compliance Monitoring System
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(title_html)
    )


def enable_controls(map_obj):

    folium.LayerControl(
        position='topleft'
    ).add_to(map_obj)

    Fullscreen().add_to(map_obj)


def save_map(map_obj):

    output_file = OUTPUT_PATH.parent / "map.html"

    map_obj.save(output_file)

    print(f"\nMap saved at: {output_file}")


def run():

    print("Generating advanced geo map...\n")

    df = load_data(OUTPUT_PATH)

    print("\nIllegal count check:")
    print(df["illegal"].value_counts())

    map_obj = create_map()

    add_markers(map_obj, df)

    add_heatmap(map_obj, df)

    add_legend(map_obj)

    add_stats_panel(map_obj, df)

    add_title(map_obj)

    enable_controls(map_obj)

    save_map(map_obj)


if __name__ == "__main__":
    run()