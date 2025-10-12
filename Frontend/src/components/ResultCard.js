

import React from 'react';

function ResultCard({ data }) {
  return (
    <div className="result-card">
      <p><strong>Site:</strong> {data.name || 'Unknown'}</p>
      <p><strong>Latitude:</strong> {data.latitude}</p>
      <p><strong>Longitude:</strong> {data.longitude}</p>
      <p><strong>NDVI:</strong> {data.ndvi}</p>
      <p><strong>Health Score:</strong> {data.health_score}%</p>
      <p><strong>Status:</strong> {data.status}</p>
    </div>
  );
}

export default ResultCard;
