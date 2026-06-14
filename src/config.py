from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "cleaned_data.csv"

OUTPUT_PATH = BASE_DIR / "reports" / "output.csv"

# Cities (lat_min, lon_min, lat_max, lon_max)
CITIES = {
    # "delhi": (28.40, 76.80, 28.90, 77.50),
    # "gurgaon": (28.10, 76.60, 28.70, 77.30),
    # "noida": (28.4, 77.2, 28.8, 77.6),
    # "chandigarh": (30.68, 76.72, 30.78, 76.84),
    # "bangalore": (12.85, 77.50, 13.10, 77.75),
    "mumbai": (18.89, 72.80, 19.25, 72.99)

}
# Detection rule (meters)
DISTANCE_THRESHOLD = 100

# OSM tags
SCHOOL_TAG = "school"
TEMPLE_TAG = "place_of_worship"
SHOP_TAG = "alcohol"