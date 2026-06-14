import requests
import json
import time
from pathlib import Path
from src.config import CITIES

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "geo-compliance-system"
}

TAGS = [
    ("amenity", "school"),
    ("amenity", "place_of_worship"),
    ("shop", "alcohol")
]

MAX_RETRIES = 3
RETRY_DELAY = 5


def build_query(lat_min, lon_min, lat_max, lon_max, key, value):
    return f"""
[out:json][timeout:60];
node["{key}"="{value}"]({lat_min},{lon_min},{lat_max},{lon_max});
out;
"""


def fetch_data(query):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                OVERPASS_URL,
                params={"data": query},
                headers=HEADERS,
                timeout=120
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print("Skipping...")
                return None


def save_data(city, combined_elements):
    path = Path("data/raw") / f"{city}.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"elements": combined_elements}, f, indent=2)

    print(f"Saved: {path}")


def process_city(city, coords):
    print(f"\nProcessing {city}...")

    lat_min, lon_min, lat_max, lon_max = coords
    all_elements = []

    for key, value in TAGS:
        print(f"Fetching {value}...")

        query = build_query(lat_min, lon_min, lat_max, lon_max, key, value)
        data = fetch_data(query)

        if data and "elements" in data:
            count = len(data["elements"])
            print(f"{value}: {count} records")
            all_elements.extend(data["elements"])

        time.sleep(5)  # prevent rate limit

    print(f"{city}: total {len(all_elements)} records")

    save_data(city, all_elements)


def run():
    print("Starting optimized data fetch...\n")

    for city, coords in CITIES.items():
        process_city(city, coords)
        time.sleep(10)

    print("\nData fetching completed.")


if __name__ == "__main__":
    run()