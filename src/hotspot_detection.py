import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from src.config import OUTPUT_PATH
from pathlib import Path


HOTSPOT_OUTPUT_PATH = Path("reports/hotspot_output.csv")
HOTSPOT_SUMMARY_PATH = Path("reports/hotspot_summary.csv")


# Load data
def load_data(path):

    df = pd.read_csv(path)

    df["illegal"] = (
        df["illegal"]
        .astype(str)
        .str.lower()
        .map({"true": True, "false": False})
    )

    return df


# Keep only illegal shops
def get_illegal_shops(df):

    illegal_df = df[df["illegal"] == True].copy()

    illegal_df = illegal_df.reset_index(drop=True)

    return illegal_df


# Prepare coordinates
def prepare_features(df):

    coords = df[["lat", "lon"]].values

    scaler = StandardScaler()

    scaled_coords = scaler.fit_transform(coords)

    return scaled_coords


# Run DBSCAN
def apply_dbscan(coords):

    model = DBSCAN(
        eps=0.15,
        min_samples=3
    )

    clusters = model.fit_predict(coords)

    return clusters


# Add cluster labels
def assign_clusters(df, clusters):

    df["cluster"] = clusters

    return df


# Assign hotspot level
def classify_hotspots(df):

    cluster_counts = (
        df[df["cluster"] != -1]
        .groupby("cluster")
        .size()
        .to_dict()
    )

    hotspot_types = []

    for _, row in df.iterrows():

        cluster = row["cluster"]

        if cluster == -1:
            hotspot_types.append("Noise")
            continue

        count = cluster_counts[cluster]

        if count >= 15:
            hotspot_types.append("High Risk Zone")

        elif count >= 8:
            hotspot_types.append("Medium Risk Zone")

        else:
            hotspot_types.append("Low Risk Zone")

    df["hotspot_type"] = hotspot_types

    return df


# Create hotspot summary
def generate_cluster_summary(df):

    hotspot_df = df[df["cluster"] != -1]

    summary = (
        hotspot_df
        .groupby("cluster")
        .agg(
            total_violations=("cluster", "size"),
            avg_lat=("lat", "mean"),
            avg_lon=("lon", "mean"),
            cities=("city", lambda x: ", ".join(sorted(set(x))))
        )
        .reset_index()
    )

    def classify(count):

        if count >= 15:
            return "High Risk"

        elif count >= 8:
            return "Medium Risk"

        return "Low Risk"

    summary["risk_level"] = (
        summary["total_violations"]
        .apply(classify)
    )

    return summary


# Print ML stats
def generate_statistics(df, summary):

    total_hotspots = summary["cluster"].nunique()

    noise_points = (df["cluster"] == -1).sum()

    largest_cluster = (
        summary["total_violations"].max()
        if not summary.empty
        else 0
    )

    print("\n========== ML HOTSPOT ANALYSIS ==========")

    print(f"\nTotal Illegal Shops: {len(df)}")

    print(f"Total Hotspots Detected: {total_hotspots}")

    print(f"Noise Points: {noise_points}")

    print(f"Largest Hotspot Size: {largest_cluster}")

    print("\nHotspot Risk Distribution:")

    print(
        summary["risk_level"]
        .value_counts()
    )


# Save files
def save_outputs(df, summary):

    HOTSPOT_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(HOTSPOT_OUTPUT_PATH, index=False)

    summary.to_csv(HOTSPOT_SUMMARY_PATH, index=False)

    print(f"\nSaved hotspot data: {HOTSPOT_OUTPUT_PATH}")

    print(f"Saved hotspot summary: {HOTSPOT_SUMMARY_PATH}")


# Main function
def run():

    print("Starting ML hotspot detection...\n")

    df = load_data(OUTPUT_PATH)

    illegal_df = get_illegal_shops(df)

    print(f"Illegal shops for ML analysis: {len(illegal_df)}")

    coords = prepare_features(illegal_df)

    clusters = apply_dbscan(coords)

    illegal_df = assign_clusters(
        illegal_df,
        clusters
    )

    illegal_df = classify_hotspots(illegal_df)

    summary = generate_cluster_summary(illegal_df)

    generate_statistics(
        illegal_df,
        summary
    )

    save_outputs(
        illegal_df,
        summary
    )

    print("\nDBSCAN hotspot detection completed.")


if __name__ == "__main__":
    run()