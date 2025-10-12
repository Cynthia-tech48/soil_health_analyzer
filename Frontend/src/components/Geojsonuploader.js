import React, { useState } from "react";
import axios from "axios";

export default function GeoJSONUploader() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);

  const handleUpload = async () => {
    if (!file) return alert("Select a GeoJSON file first.");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/analyze_polygon`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResults(response.data.polygon_results);
    } catch (error) {
      alert("Failed to process polygon.");
      console.error(error);
    }
  };

  return (
    <div>
      <input type="file" accept=".json,.geojson" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Analyze Polygon</button>

      {results.length > 0 &&
        results.map((r, idx) => (
          <div key={idx} className="result-card">
            <p>
              <strong>Latitude:</strong> {r.latitude}
            </p>
            <p>
              <strong>Longitude:</strong> {r.longitude}
            </p>
            <p>
              <strong>NDVI:</strong> {r.ndvi}
            </p>
            <p>
              <strong>Health Score:</strong> {r.health_score}%
            </p>
            <p>
              <strong>Status:</strong> {r.status}
            </p>
          </div>
        ))}
    </div>
  );
}
