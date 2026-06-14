import pandas as pd
import numpy as np
from src.config import PROCESSED_DATA_PATH, DISTANCE_THRESHOLD, OUTPUT_PATH


def load_data(path):
    return pd.read_csv(path)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000 # Earth radius in meters

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def split_data(df):
    schools = df[df["type"] == "school"]
    temples = df[df["type"] == "place_of_worship"]
    shops = df[df["type"] == "alcohol"]

    return schools, temples, shops


def compute_nearest(shop_df, ref_df):
    distances = []
    names = []

    ref_lat = ref_df["lat"].values
    ref_lon = ref_df["lon"].values
    ref_name = ref_df["name"].values

    for _, shop in shop_df.iterrows():
        lat1 = shop["lat"]
        lon1 = shop["lon"]

        if len(ref_lat) == 0:
            distances.append(np.nan)
            names.append("None")
            continue

        dists = haversine(lat1, lon1, ref_lat, ref_lon)

        idx = np.argmin(dists)
        distances.append(dists[idx])
        names.append(ref_name[idx])

    return distances, names


def apply_rules(df):
    df = df.copy()

    df["nearest_type"] = np.where(
        df["nearest_school_distance"] < df["nearest_temple_distance"],
        "school",
        "temple"
    )

    df["illegal"] = (
        (df["nearest_school_distance"] < DISTANCE_THRESHOLD) |
        (df["nearest_temple_distance"] < DISTANCE_THRESHOLD)
    )

    def get_reason(row):
        if row["nearest_school_distance"] < DISTANCE_THRESHOLD and row["nearest_temple_distance"] < DISTANCE_THRESHOLD:
            return "Near Both"
        elif row["nearest_school_distance"] < DISTANCE_THRESHOLD:
            return "Near School"
        elif row["nearest_temple_distance"] < DISTANCE_THRESHOLD:
            return "Near Temple"
        else:
            return "Safe"

    df["violation_reason"] = df.apply(get_reason, axis=1)

    def get_severity(row):
        min_dist = min(row["nearest_school_distance"], row["nearest_temple_distance"])

        if min_dist < 50:
            return "High"
        elif min_dist < 100:
            return "Medium"
        else:
            return "Low"

    df["severity"] = df.apply(get_severity, axis=1)

    df["nearest_school_distance"] = df["nearest_school_distance"].round(2)
    df["nearest_temple_distance"] = df["nearest_temple_distance"].round(2)

    return df


def generate_stats(df):
    total = len(df)
    illegal = df["illegal"].sum()
    percent = (illegal / total) * 100 if total > 0 else 0

    print("\nStatistics:")
    print(f"Total Shops: {total}")
    print(f"Illegal Shops: {illegal}")
    print(f"Illegal %: {percent:.2f}%")


def run():
    print("Starting distance analysis...\n")

    df = load_data(PROCESSED_DATA_PATH)

    schools, temples, shops = split_data(df)

    print(f"Total alcohol shops: {len(shops)}")

    shops = shops.copy()

    shops["nearest_school_distance"], shops["nearest_school_name"] = compute_nearest(shops, schools)
    shops["nearest_temple_distance"], shops["nearest_temple_name"] = compute_nearest(shops, temples)

    shops = apply_rules(shops)

    generate_stats(shops)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shops.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved final report: {OUTPUT_PATH}")


if __name__ == "__main__":
    run()   