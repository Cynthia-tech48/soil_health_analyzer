import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView({ points }) {
  if (!points || points.length === 0) return null;

  const center = [points[0].latitude, points[0].longitude];

  return (
    <div className="map-container">
      <MapContainer center={center} zoom={6} style={{ height: "450px", width: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        {points.map((point, idx) => (
          <Marker key={idx} position={[point.latitude, point.longitude]}>
            <Popup>
              <strong>{point.name}</strong>
              <br />
              Health Score: {point.health_score}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
