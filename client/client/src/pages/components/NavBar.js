import React from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../../images/logo.png";

function NavBar() {
  const navigate = useNavigate();

  const handleClickLogo = () => {
    navigate("/");
  };

  return (
    <nav className="bg-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-center">
        <Link to="/" className="flex items-center" onClick={handleClickLogo}>
          <img src={logo} alt="Logo" className="h-48 w-48 mr-2" />
        </Link>
      </div>
    </nav>
  );
}

export default NavBar;
