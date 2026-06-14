# 🌍 MapSentinel: Geo-Spatial Compliance System

Advanced ML-powered geospatial compliance monitoring and hotspot detection system using OpenStreetMap, Haversine distance analysis, DBSCAN clustering, and interactive GIS analytics.

---

## Features

- **Multi-City Geo Data Extraction**: Automated OpenStreetMap data extraction using Overpass API
- **Geospatial Distance Analysis**: Haversine formula-based nearest distance calculation
- **Compliance Detection Engine**: Detects illegal alcohol shops near schools and temples
- **Interactive Geo Visualization**: Folium-powered live analytics maps with hotspots & heatmaps
- **ML Hotspot Detection**: DBSCAN clustering for dense violation hotspot identification
- **Analytics Dashboard**: Streamlit-based professional monitoring dashboard
- **Risk Categorization**: High, Medium, Low risk-based violation analysis
- **Real-Time Insights**: Interactive charts, KPIs, hotspot rankings, and ML insights

---

## Tech Stack

- **Backend**: Python 3.12
- **Data Processing**: Pandas, NumPy
- **GIS & Mapping**: Folium, OpenStreetMap, Overpass API
- **Machine Learning**: Scikit-learn (DBSCAN)
- **Visualization**: Streamlit, Plotly
- **Distance Calculation**: Haversine Formula

---

## Installation

### Prerequisites

- Python 3.12+
- pip
- Git

---

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/akhil22201/MapSentinel-GeoSpatial-Compliance-System.git

cd MapSentinel-GeoSpatial-Compliance-System
```

---

2. **Create virtual environment**

```bash
python -m venv geo-env
```

---

3. **Activate virtual environment**

- Windows:

```bash
geo-env\Scripts\activate
```

- Linux/Mac:

```bash
source geo-env/bin/activate
```

---

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Usage

### Step 1 — Fetch OpenStreetMap Data

```bash
python -m src.data_fetch
```

---

### Step 2 — Clean & Process Data

```bash
python -m src.data_cleaning
```

---

### Step 3 — Run Distance Compliance Analysis

```bash
python -m src.distance_calc
```

---

### Step 4 — Run ML Hotspot Detection

```bash
python -m src.hotspot_detection
```

---

### Step 5 — Launch Analytics Dashboard

```bash
streamlit run app/app.py
```

---

## Dashboard Features

- Interactive Geo Analytics Map
- Violation Heatmaps
- Hotspot Cluster Visualization
- City-wise Analytics
- Severity Distribution Charts
- ML-Based Risk Insights
- Compliance Statistics
- Multi-City Filtering

---

## Project Structure

```plaintext
geo-compliance-monitoring-system/

├── app/
│   ├── app.py
│   └── components/
│       ├── map_view.py
│       ├── sidebar.py
│       └── stats.py
│
├── src/
│   ├── config.py
│   ├── data_fetch.py
│   ├── data_cleaning.py
│   ├── distance_calc.py
│   ├── hotspot_detection.py
│   └── map_utils.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   ├── output.csv
│   ├── hotspot_output.csv
│   ├── hotspot_summary.csv
│   └── map.html
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Machine Learning Module

### DBSCAN Clustering

The project uses DBSCAN (Density-Based Spatial Clustering of Applications with Noise) for hotspot detection.

### ML Objectives

- Detect dense violation regions
- Identify high-risk geographic zones
- Generate hotspot clusters
- Analyze spatial violation patterns

### ML Outputs

- Hotspot Cluster ID
- Cluster Risk Levels
- Violation Density
- Cluster-wise Analytics

---

## Compliance Detection Logic

The system flags alcohol shops as illegal if they are located within a threshold distance from:

- Schools
- Temples / Places of Worship

### Distance Formula

The project uses the **Haversine Formula** for accurate geospatial distance calculation between coordinates.

---

## Supported Cities

- Delhi
- Gurgaon
- Noida
- Chandigarh
- Bangalore
- Mumbai

---

## Performance Optimization

- Optimized API request handling
- Retry-based Overpass API fetching
- Marker clustering for large-scale visualization
- Heatmap rendering optimization
- Modular Streamlit architecture

---

## Future Improvements

- Real-time monitoring pipeline
- Live API integration
- Predictive violation forecasting
- Advanced GIS analytics
- AI-powered compliance prediction
- Government compliance reporting system

---

## Troubleshooting

### Overpass API Rate Limit

- Reduce simultaneous requests
- Fetch cities sequentially
- Increase retry delay

---

### Streamlit Dashboard Not Loading

Install missing dependencies:

```bash
pip install streamlit folium streamlit-folium plotly
```

---

### Import Errors in VS Code

Select correct Python interpreter:

```plaintext
Ctrl + Shift + P
→ Python: Select Interpreter
```

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## License

MIT License

---

## ## Results

The system was evaluated using geospatial data collected from multiple cities through OpenStreetMap and the Overpass API.

### Key Outcomes

* Total Cities Analyzed: 5
* Total Alcohol Shops Analyzed: 300
* Potential Compliance Violations Detected: 32
* Overall Compliance Rate: 89.3%
* Hotspot Regions Identified: 3
* Largest Hotspot Cluster Size: 16

### Key Findings

* Successfully automated compliance monitoring using GIS analytics.
* Identified high-risk geographic regions through DBSCAN clustering.
* Enabled interactive visualization of violations, hotspots, and compliance statistics.
* Improved monitoring efficiency through automated distance-based compliance analysis.
* Provided decision-support insights through an interactive Streamlit dashboard.

---

## Author

**Akhil**

---

## Acknowledgments

* OpenStreetMap
* Overpass API
* Folium
* Streamlit
* Scikit-learn
* GIS & Open Source Mapping Community
