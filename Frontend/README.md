🌱 SOIL HEALTH ANALYZER

AI-powered Soil Health Analysis web application that uses NDVI, geolocation, and machine learning to evaluate soil conditions and generate reports. Users can analyze single points or polygons, view results on a map, and download CSV or PDF reports.

---

## Features

- Analyze soil health for a single point or a polygon (GeoJSON support).  
- Auto-detect site name from coordinates using reverse geocoding.  
- Generate downloadable PDF soil health reports.  
- Visualize results on maps and charts.  
- Store results in Supabase for persistence.  
- Optional CSV export.  

---

## Tech Stack

- **Frontend:** React.js, Axios, Leaflet.js, Chart.js  
- **Backend:** Flask, Python, ReportLab, Geopy  
- **Database:** Supabase (PostgreSQL)  
- **Machine Learning:** Pre-trained model (`soil_model.pkl`) for soil health prediction  
- **Other Libraries:** dotenv, flask-cors  

---

## Requirements

### Python (Backend)

- Python 3.9+
- Flask
- Flask-CORS
- python-dotenv
- reportlab
- geopy
- requests
- supabase-py
- pandas (optional)
- numpy (optional)
- Any other packages required by `utils/gis_handler.py` and `utils/model_predictor.py`

**Install via pip:**

```bash
pip install Flask Flask-CORS python-dotenv reportlab geopy supabase pandas numpy
Node.js / Frontend
Node.js 18+ / npm

React.js

Axios

React Leaflet

Chart.js

Install frontend dependencies:

bash
Copy code
npm install axios react-router-dom leaflet react-leaflet chart.js
Setup Instructions
Backend
Navigate to the backend folder:

bash
Copy code
cd backend
Create a .env file and add the following:

env
Copy code
SUPABASE_URL=https://pmfhzmvfrmlsoxhzlgin.supabase.co
SUPABASE_ANON_KEY==eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtZmh6bXZmcm1sc294aHpsZ2luIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxMDAyMzYsImV4cCI6MjA3NTY3NjIzNn0.YourAnonKeyHere

GIS_METHOD=your_ndvi_method
PORT=5000
Run the backend server:

bash
Copy code
python app.py
The backend will run on http://127.0.0.1:5000 (or your local IPv4).

Frontend
Navigate to the frontend folder:

bash
Copy code
cd frontend
Create a .env file and add the backend URL:

env
Copy code
REACT_APP_BACKEND_URL=http://127.0.0.1:5000
Start the frontend:

bash
Copy code
npm start
Open your browser at http://localhost:3000.

Usage
Enter a Latitude and Longitude (optionally a site name).

Click Analyze to fetch soil health results.

View the results in the Result Card, Map, and Charts sections.

Optionally, download results as CSV or generate a PDF report.

Deployment
frontend: vercel :https://soil-health-analyzer.vercel.app
Pitch Deck URL : https://gamma.app/docs/Soil-Health-1jaua3af3e9iwc4