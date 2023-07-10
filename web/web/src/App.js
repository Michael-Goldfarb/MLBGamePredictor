import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./Login.js";
import Dashboard from "./dashboard.js";
import Profile from "./profile.js";
import Prediction from "./pages/PredictionsPage.js";
import Navbar from "./pages/components/NavBar.js";
import PredictionHistory from "./pages/PredictionHistoryPage.js";

function App() {
  return (
    <div className="app bg-gray-800 text-white">
      <Router>
        <Navbar /> 
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/predictions" element={<Prediction />} />
          <Route path="/history" element={<PredictionHistory />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
