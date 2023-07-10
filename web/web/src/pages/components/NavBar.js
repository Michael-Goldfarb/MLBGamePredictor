import React from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../../images/logo.png";
import historyLogo from "../../images/history.png";

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
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        <Link to="/history" className="flex items-center" onClick={handleClickHistory}>
          <img src={historyLogo} alt="History" className="h-10 w-10 mr-2" />
        </Link>
        <div className="flex items-center">
          <div className="mx-auto">
            <Link to="/" onClick={handleClickLogo}>
              <img src={logo} alt="Logo" className="h-32 w-32" />
            </Link>
          </div>
        </div>
        <div></div>
      </div>
    </nav>
  );
}

export default NavBar;
