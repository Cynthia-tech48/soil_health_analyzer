from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from utils.gis_handler import fetch_ndvi
from utils.model_predictor import predict_soil_health_from_ndvi
from utils import supabase_client
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "✅ Soil Health AI Backend is running"})

@app.route("/analyze", methods=["POST"])
def analyze_point():
    """Analyze soil health for a given point (auto-detects site name)."""
    data = request.get_json(force=True) or {}
    lat = data.get("latitude")
    lon = data.get("longitude")
    name = (data.get("name") or "").strip()

    # Validate coordinates
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except Exception:
        return jsonify({"error": "Invalid coordinates"}), 400

    # Reverse geocode if name not provided
    if not name:
        try:
            geolocator = Nominatim(user_agent="soil_health_app")
            location = geolocator.reverse((lat_f, lon_f), language="en", timeout=10)
            if location:
                name = location.address.split(",")[0]  # cleaner site name
                print(f"📍 Auto-detected site: {name}")
            else:
                name = "Unknown Site"
        except (GeocoderTimedOut, GeocoderUnavailable):
            name = "Unknown Site"
        except Exception as e:
            print("⚠️ Geocoding error:", e)
            name = "Unknown Site"

    # Fetch NDVI and predict health
    ndvi = fetch_ndvi(lat_f, lon_f, method=os.getenv("GIS_METHOD"))
    label, score = predict_soil_health_from_ndvi(ndvi)

    # Save to Supabase
    if supabase_client.supabase:
        try:
            supabase_client.supabase.table("analysis_results").insert({
                "name": name,
                "latitude": lat_f,
                "longitude": lon_f,
                "ndvi_value": float(ndvi),
                "soil_health_score": float(score),
                "health_label": label
            }).execute()
            print(f"✅ Saved to Supabase: {name}")
        except Exception as e:
            print("❌ Failed to save:", e)

    # Send result
    response = {
        "name": name,
        "latitude": lat_f,
        "longitude": lon_f,
        "ndvi": ndvi,
        "health_score": score,
        "status": label
    }
    return jsonify(response), 200

@app.route("/export_report", methods=["POST"])
def export_report():
    """Generate a downloadable soil report (PDF)."""
    data = request.get_json(force=True) or {}
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Soil Health Report")

    # Header
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 750, "Soil Health Report")
    p.setFont("Helvetica", 11)
    p.drawString(50, 730, f"Site name: {data.get('name', 'N/A')}")
    p.drawString(50, 710, f"Latitude: {data.get('latitude')}")
    p.drawString(50, 690, f"Longitude: {data.get('longitude')}")
    p.drawString(50, 670, f"NDVI: {data.get('ndvi')}")
    p.drawString(50, 650, f"Soil Health Score: {data.get('health_score')}%")
    p.drawString(50, 630, f"Status: {data.get('status')}")
    p.drawString(50, 590, "Notes:")
    p.drawString(70, 570, "- Recommendations are indicative. Validate with field sampling.")
    p.drawString(70, 550, "- Consult local agronomists for actionable steps.")
    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="soil_report.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
