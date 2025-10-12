import requests
import csv
import os
from utils import supabase_client

# Make sure the reports folder exists
reports_folder = "reports"
if not os.path.exists(reports_folder):
    os.makedirs(reports_folder)

# CSV file path
csv_file_path = os.path.join(reports_folder, "soil_health_results.csv")

# List of 15 cities with coordinates
cities = [
    {"name": "Nairobi", "latitude": -1.286389, "longitude": 36.817223},
    {"name": "Mombasa", "latitude": -4.043477, "longitude": 39.668206},
    {"name": "Kisumu", "latitude": -0.091702, "longitude": 34.767956},
    {"name": "Eldoret", "latitude": 0.5143, "longitude": 35.2696},
    {"name": "Nakuru", "latitude": -0.3031, "longitude": 36.0800},
    {"name": "Thika", "latitude": -1.0333, "longitude": 37.0692},
    {"name": "Kitale", "latitude": 1.0158, "longitude": 35.0056},
    {"name": "Garissa", "latitude": -0.4562, "longitude": 39.6589},
    {"name": "Malindi", "latitude": -3.2186, "longitude": 40.1168},
    {"name": "Meru", "latitude": 0.0465, "longitude": 37.6493},
    {"name": "Bungoma", "latitude": 0.5691, "longitude": 34.5605},
    {"name": "Kakamega", "latitude": 0.2821, "longitude": 34.7519},
    {"name": "Kitui", "latitude": -1.3667, "longitude": 38.0167},
    {"name": "Busia", "latitude": 0.4543, "longitude": 34.0902},
    {"name": "Siaya", "latitude": 0.0600, "longitude": 34.2867},
]

# Open CSV file in write mode and write headers
with open(csv_file_path, mode="w", newline="") as csv_file:
    fieldnames = ["name", "latitude", "longitude", "ndvi", "health_score", "status"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each city and send POST request
    for city in cities:
        try:
            response = requests.post(
                "http://127.0.0.1:5000/analyze",
                json={
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "name": city["name"]
                },
            )
            if response.status_code == 200:
                data = response.json()
                
                # Write to CSV
                writer.writerow({
                    "name": city["name"],
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "ndvi": data["ndvi"],
                    "health_score": data["health_score"],
                    "status": data["status"]
                })
                print(f"✅ Saved result for {city['name']} in CSV")

                # Save to Supabase
                if supabase_client.supabase:
                    try:
                        supabase_client.supabase.table("analysis_results").insert({
                            "name": city["name"],
                            "latitude": data["latitude"],
                            "longitude": data["longitude"],
                            "ndvi_value": data["ndvi"],
                            "soil_health_score": data["health_score"],
                            "health_label": data["status"]
                        }).execute()
                        print(f"✅ Saved result for {city['name']} in Supabase")
                    except Exception as e:
                        print(f"❌ Failed to save to Supabase for {city['name']}: {e}")
                else:
                    print("⚠️ Supabase client not initialized")
            else:
                print(f"❌ API error for {city['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Request failed for {city['name']}: {e}")

print(f"\nAll results saved to {csv_file_path} and Supabase (if configured).")
