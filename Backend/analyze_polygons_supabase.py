import requests
import csv
import os
from utils import supabase_client

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

# Define 15 Kenyan city polygons (small bounding boxes)
polygons = [
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Nairobi"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[36.80, -1.28], [36.82, -1.28], [36.82, -1.30], [36.80, -1.30], [36.80, -1.28]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Mombasa"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[39.65, -4.05], [39.70, -4.05], [39.70, -4.10], [39.65, -4.10], [39.65, -4.05]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Kisumu"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[34.74, -0.10], [34.78, -0.10], [34.78, -0.14], [34.74, -0.14], [34.74, -0.10]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Eldoret"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[35.26, 0.50], [35.30, 0.50], [35.30, 0.46], [35.26, 0.46], [35.26, 0.50]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Nakuru"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[36.05, -0.28], [36.09, -0.28], [36.09, -0.32], [36.05, -0.32], [36.05, -0.28]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Thika"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[37.06, -1.03], [37.10, -1.03], [37.10, -1.07], [37.06, -1.07], [37.06, -1.03]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Meru"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[37.63, 0.04], [37.67, 0.04], [37.67, 0.00], [37.63, 0.00], [37.63, 0.04]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Kitui"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[38.00, -1.35], [38.05, -1.35], [38.05, -1.40], [38.00, -1.40], [38.00, -1.35]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Machakos"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[37.23, -1.50], [37.28, -1.50], [37.28, -1.55], [37.23, -1.55], [37.23, -1.50]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Bungoma"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[34.55, 0.56], [34.60, 0.56], [34.60, 0.52], [34.55, 0.52], [34.55, 0.56]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Kakamega"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[34.75, 0.28], [34.80, 0.28], [34.80, 0.24], [34.75, 0.24], [34.75, 0.28]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Busia"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[34.11, 0.44], [34.16, 0.44], [34.16, 0.40], [34.11, 0.40], [34.11, 0.44]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Siaya"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[33.90, 0.07], [33.95, 0.07], [33.95, 0.03], [33.90, 0.03], [33.90, 0.07]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Nyeri"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[36.95, -0.42], [37.00, -0.42], [37.00, -0.46], [36.95, -0.46], [36.95, -0.42]]]
                }
            }
        ]
    },
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Nanyuki"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[37.06, 0.01], [37.10, 0.01], [37.10, -0.03], [37.06, -0.03], [37.06, 0.01]]]
                }
            }
        ]
    }
]

# CSV file path
csv_file = "reports/polygon_soil_health_results.csv"

# Open CSV for writing
with open(csv_file, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "latitude", "longitude", "ndvi", "health_score", "status"])
    writer.writeheader()

    # Loop through each polygon
    for poly in polygons:
        city_name = poly["features"][0]["properties"]["name"]
        try:
            response = requests.post("http://127.0.0.1:5000/analyze_polygon", json=poly)
            response.raise_for_status()
            data = response.json()

            # The backend returns 'polygon_results' array
            for point in data.get("polygon_results", []):
                point["name"] = city_name  # add city name
                writer.writerow({
                    "name": city_name,
                    "latitude": point.get("latitude"),
                    "longitude": point.get("longitude"),
                    "ndvi": point.get("ndvi"),
                    "health_score": point.get("health_score"),
                    "status": point.get("status")
                })

                # Save to Supabase if configured
                if supabase_client.supabase:
                    try:
                        supabase_client.supabase.table("analysis_results").insert({
                            "name": city_name,
                            "latitude": point.get("latitude"),
                            "longitude": point.get("longitude"),
                            "ndvi_value": float(point.get("ndvi")),
                            "soil_health_score": float(point.get("health_score")),
                            "health_label": point.get("status")
                        }).execute()
                        print(f"✅ Saved result for {city_name} in Supabase")
                    except Exception as e:
                        print(f"❌ Failed to save {city_name} in Supabase:", e)

            print(f"✅ Saved result for {city_name} in CSV")

        except Exception as e:
            print(f"❌ Failed to process polygon {city_name}:", e)

print(f"\nAll results saved to {csv_file} and Supabase (if configured).")
