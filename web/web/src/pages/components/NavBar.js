import React from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../../images/logo.png";
import historyLogo from "../../images/history.png";
import "./NavBar.css"; // Import custom CSS file for styling

function NavBar() {
  const navigate = useNavigate();

  const handleClickLogo = () => {
    navigate("/");
  };

  const handleClickHistory = () => {
    navigate("/history");
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
          <Link to="/" onClick={handleClickLogo}>
            <img src={logo} alt="Logo" className="main-logo" />
          </Link>
        </div>
        <div></div>
      </div>
    </nav>
  );
}

export default NavBar;
