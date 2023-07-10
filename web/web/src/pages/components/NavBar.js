import React from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../../images/logo.png";
import historyLogo from "../../images/history.png";
import profileLogo from "../../images/profile.png";
import "./NavBar.css";

function NavBar() {
  const navigate = useNavigate();

  const handleClickLogo = () => {
    navigate("/predictions");
  };

  const handleClickHistory = () => {
    navigate("/history");
  };

  const handleClickProfile = () => {
    navigate("/profile");
  };

  return (
    <nav className="bg-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center">
        <div className="logo-container">
          <Link to="/history" onClick={handleClickHistory}>
            <img src={historyLogo} alt="History" className="history-logo" />
          </Link>
        </div>
        <div className="logo-container flex-grow flex justify-center">
          <Link to="/predictions" onClick={handleClickLogo}>
            <img src={logo} alt="Logo" className="main-logo" />
          </Link>
        </div>
        <div className="logo-container">
          <Link to="/profile" onClick={handleClickProfile}>
            <img src={profileLogo} alt="Profile" className="profile-logo" />
          </Link>
        </div>
      </div>
    </nav>
  );  
}

export default NavBar;
