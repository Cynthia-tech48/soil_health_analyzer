import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  const navStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "15px 30px",
    backgroundColor: "#2e7d32",
    color: "#fff",
    fontWeight: "bold",
  };

  const linkStyle = {
    color: "#fff",
    textDecoration: "none",
    marginLeft: "20px",
  };

  return (
    <nav style={navStyle}>
      <div>
        🌱 Soil Health Analyzer
      </div>
      <div>
        <Link style={linkStyle} to="/">Home</Link>
        <Link style={linkStyle} to="/analyze">Analyze</Link>
      </div>
    </nav>
  );
};

export default Navbar;
