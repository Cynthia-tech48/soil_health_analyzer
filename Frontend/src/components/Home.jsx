import React from "react";

const Home = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        minHeight: "100vh",
        padding: "20px",
        backgroundColor: "#f0f8ff",
      }}
    >
      <h1 style={{ fontSize: "3rem", marginBottom: "20px", color: "#2e7d32" }}>
        🌱 Welcome to the Soil Health Analyzer 🌱
      </h1>
      <p style={{ maxWidth: "700px", fontSize: "1.2rem", marginBottom: "15px" }}>
        This AI-powered application allows you to analyze soil health using NDVI (Normalized Difference Vegetation Index) and geolocation data. 
      </p>
      <p style={{ maxWidth: "700px", fontSize: "1.2rem", marginBottom: "15px" }}>
        You can input the latitude and longitude of a site to fetch real-time soil health data, visualize it on a map, and even download the results in CSV format.
      </p>
      <p style={{ maxWidth: "700px", fontSize: "1.2rem" }}>
        Explore the application, gain insights about soil conditions, and make data-driven decisions for agricultural planning and environmental monitoring.
      </p>
      <p style={{ marginTop: "30px", fontSize: "1rem", color: "#555" }}>
        Navigate to <strong>Analyze</strong> to start analyzing your site data.
      </p>
    </div>
  );
};

export default Home;
