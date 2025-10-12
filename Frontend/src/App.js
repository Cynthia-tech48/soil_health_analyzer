import React, { useState } from "react";
import axios from "axios";
import MapView from "./components/MapView";
import ResultCard from "./components/ResultCard";
import SoilHealthCharts from "./components/SoilHealthCharts";
import "./style.css";

function App() {
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [name, setName] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzePoint = async () => {
    if (!latitude || !longitude) {
      alert("Please enter Latitude and Longitude.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/analyze`,
        { latitude, longitude, name: name || "" }  // backend-safe
      );

      setResults([response.data]);
    } catch (error) {
      console.error("❌ Error analyzing point:", error);
      alert("Failed to fetch data. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (results.length === 0) return;
    const csvContent =
      "data:text/csv;charset=utf-8," +
      ["site,latitude,longitude,ndvi,soil_health_score,status"]
        .concat(
          results.map(
            (r) =>
              `${r.name || "Unknown"},${r.latitude},${r.longitude},${r.ndvi},${r.health_score},${r.status}`
          )
        )
        .join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "soil_health_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="app-container">
      <header>
        <h1>🌱 Soil Health Analyzer 🌱</h1>
        <p>AI-powered soil analysis using NDVI & geolocation</p>
      </header>

      <section className="input-section">
        <div className="input-group">
          <input
            type="text"
            placeholder="Site Name (optional)"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="number"
            placeholder="Latitude"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
          />
          <input
            type="number"
            placeholder="Longitude"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
          />
        </div>

        <div className="button-group">
          <button className="analyze-btn" onClick={analyzePoint} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
          <button className="download-btn" onClick={downloadCSV}>
            Download CSV
          </button>
        </div>
      </section>

      {results.length > 0 && (
        <>
          <section className="results-section">
            {results.map((r, idx) => (
              <ResultCard key={idx} data={r} />
            ))}
          </section>

          <section className="map-section">
            <MapView points={results} />
          </section>

          <section className="charts-section">
            <SoilHealthCharts results={results} />
          </section>
        </>
      )}
    </div>
  );
}

export default App;
