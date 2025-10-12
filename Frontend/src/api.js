import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000"; // Your Flask backend

export const analyzePoint = async (latitude, longitude, name) => {
  const response = await axios.post(`${BASE_URL}/analyze`, { latitude, longitude, name });
  return response.data;
};

export const analyzePolygon = async (geojson) => {
  const response = await axios.post(`${BASE_URL}/analyze_polygon`, geojson);
  return response.data;
};

export const downloadReport = async (data) => {
  const response = await axios.post(`${BASE_URL}/export_report`, data, { responseType: 'blob' });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'soil_report.pdf');
  document.body.appendChild(link);
  link.click();
};
