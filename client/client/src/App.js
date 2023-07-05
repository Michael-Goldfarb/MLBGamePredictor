import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./Login.js";
import Dashboard from "./dashboard.js";
import Navbar from "./pages/components/NavBar.js";

function App() {
  return (
    <div className="app bg-gray-800 text-white">
      <Router>
        <Navbar /> {/* Include the Navbar component */}
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/mlbgamepredictions" />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
