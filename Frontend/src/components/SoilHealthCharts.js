import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function SoilHealthCharts({ results }) {
  if (!results || results.length === 0) return null;

  const labels = results.map((r) => r.name || "Unknown Site");
  const data = {
    labels,
    datasets: [
      {
        label: "Health Score",
        data: results.map((r) => r.health_score || 0),
        backgroundColor: "#4caf50",
      },
      {
        label: "NDVI",
        data: results.map((r) => r.ndvi || 0),
        backgroundColor: "#81c784",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Soil Health Metrics" },
    },
  };

  return (
    <div className="chart-container">
      <Bar data={data} options={options} />
    </div>
  );
}
