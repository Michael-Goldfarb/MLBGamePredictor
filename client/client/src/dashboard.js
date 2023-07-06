import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useNavigate, Link } from "react-router-dom";
import { auth, db, logout } from "./firebase";
import { query, collection, getDocs, where } from "firebase/firestore";

function Dashboard() {
  const [user, loading, error] = useAuthState(auth);
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const fetchUserName = async () => {
    try {
      const q = query(collection(db, "users"), where("uid", "==", user?.uid));
      const querySnapshot = await getDocs(q);
      if (!querySnapshot.empty) {
        const data = querySnapshot.docs[0].data();
        setName(data.name || ""); // Set an empty string if the name is undefined or null
      }
    } catch (err) {
      console.error(err);
      alert("An error occurred while fetching user data");
    }
  };

  useEffect(() => {
    if (loading) return;
    if (!user) return navigate("/");
    fetchUserName();
  }, [user, loading, navigate]);

  return (
    <div className="flex items-center justify-center bg-gray-900 min-h-screen text-white">
      <div className="bg-gray-800 text-white px-8 py-6 rounded-lg">
        {loading ? (
          <div>Loading...</div>
        ) : (
          <>
            {name ? (
              <>
                <div>Logged in as {name}</div>
                <div>{user?.email}</div>
              </>
            ) : (
              <div>Name not available</div>
            )}
            <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg mt-4" onClick={logout}>
              Logout
            </button>
            <Link to="/predictions" className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg mt-4">
              Go to MLB Game Predictions
            </Link>
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
