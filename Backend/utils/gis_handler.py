"""
GIS handler with two modes:
 - mock: deterministic pseudo-NDVI for demo
 - gee: real Google Earth Engine NDVI retrieval (service account)

Ensure you placed your GEE service account key JSON at the path set in GEE_PRIVATE_KEY_PATH env var.
"""

import os
import random
from dotenv import load_dotenv

load_dotenv()

# Configuration
GEE_ENABLED = os.getenv("GIS_METHOD", "mock") == "gee"
GEE_SERVICE_ACCOUNT = os.getenv("GEE_SERVICE_ACCOUNT")
GEE_KEY_PATH = os.getenv("GEE_PRIVATE_KEY_PATH")

# Initialize Google Earth Engine if enabled
if GEE_ENABLED:
    try:
        import ee
        credentials = ee.ServiceAccountCredentials(GEE_SERVICE_ACCOUNT, GEE_KEY_PATH)
        ee.Initialize(credentials)
        print("Google Earth Engine initialized.")
    except Exception as e:
        print("Failed to initialize Google Earth Engine:", e)
        print("Falling back to mock NDVI.")
        GEE_ENABLED = False

def fetch_ndvi(latitude, longitude, method=None, date_from=None, date_to=None):
    """
    Returns NDVI float.
    method: optional override: 'mock' or 'gee'
    date_from/date_to: optional ISO strings for GEE time filtering
    """
    method = method or ("gee" if GEE_ENABLED else "mock")

    if method == "mock":
        # deterministic pseudo-random NDVI based on coords
        try:
            lat = float(latitude)
            lon = float(longitude)
        except Exception:
            lat, lon = 0.0, 0.0
        seed = int((abs(lat*1000) + abs(lon*1000)) % 100000)
        rnd = random.Random(seed)
        ndvi = rnd.uniform(0.05, 0.85)
        return round(ndvi, 3)

    # GEE branch
    try:
        import ee
        point = ee.Geometry.Point([float(longitude), float(latitude)])
        coll = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(point)
        if date_from and date_to:
            coll = coll.filterDate(date_from, date_to)
        coll = coll.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
        image = coll.median().clip(point.buffer(1000))

        ndvi_dict = image.normalizedDifference(['B8', 'B4']).reduceRegion(
            reducer=ee.Reducer.mean(), geometry=point, scale=10, bestEffort=True
        ).getInfo()

        ndvi_val = ndvi_dict.get('nd')
        if ndvi_val is None:
            # fallback to first image
            image2 = coll.first()
            ndvi2_dict = image2.normalizedDifference(['B8', 'B4']).reduceRegion(
                reducer=ee.Reducer.mean(), geometry=point, scale=10, bestEffort=True
            ).getInfo()
            ndvi_val = ndvi2_dict.get('nd', 0.15)

        return round(float(ndvi_val), 3)

    except Exception as e:
        print("GEE NDVI fetch failed:", e)
        # fallback to mock NDVI
        return fetch_ndvi(latitude, longitude, method="mock")
