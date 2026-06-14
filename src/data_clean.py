import json
from pathlib import Path
import pandas as pd
from src.config import DATA_DIR, PROCESSED_DATA_PATH

RAW_DATA_DIR = DATA_DIR / "raw"


def load_files(folder: Path):
    return list(folder.glob("*.json"))


def extract_type(tags):
    if "amenity" in tags:
        return tags["amenity"]
    elif "shop" in tags:
        return tags["shop"]
    return None


def extract_name(tags):
    return (
        tags.get("name")
        or tags.get("brand")
        or tags.get("operator")
        or None
    )


def parse_file(file_path: Path):
    city = file_path.stem

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = data.get("elements", [])
    records = []

    for el in elements:
        tags = el.get("tags", {})

        lat = el.get("lat")
        lon = el.get("lon")

        if lat is None or lon is None:
            continue

        type_ = extract_type(tags)
        if type_ not in ["school", "place_of_worship", "alcohol"]:
            continue

        name = extract_name(tags)

        records.append((name, type_, lat, lon, city))

    return records


def build_dataframe(files):
    all_records = []

    for file in files:
        records = parse_file(file)
        print(f"{file.stem}: {len(records)} records")
        all_records.extend(records)

    df = pd.DataFrame(all_records, columns=["name", "type", "lat", "lon", "city"])
    return df


def clean_dataframe(df: pd.DataFrame):
    print("\nCleaning data...")

    # Fill missing names instead of dropping
    df["name"] = df["name"].fillna("Unknown")

    # Remove duplicates based on location + type
    df = df.drop_duplicates(subset=["lat", "lon", "type", "city"]).copy()

    # Normalize type safely
    df.loc[:, "type"] = df["type"].str.lower().str.strip()

    # Reset index
    df = df.reset_index(drop=True)

    return df


def save_data(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"\nSaved cleaned dataset: {path}")


def run():
    print("Starting data cleaning...\n")

    files = load_files(RAW_DATA_DIR)

    if not files:
        print("No raw files found")
        return

    df = build_dataframe(files)

    print(f"\nBefore cleaning: {len(df)} rows")

    df = clean_dataframe(df)

    print(f"After cleaning: {len(df)} rows")

    save_data(df, PROCESSED_DATA_PATH)


if __name__ == "__main__":
    run()