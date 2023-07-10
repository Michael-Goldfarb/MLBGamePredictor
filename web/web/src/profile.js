import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useNavigate, Link } from "react-router-dom";
import { auth, db, logout } from "./firebase";
import { query, collection, getDocs, where } from "firebase/firestore";

function Profile() {
  const [user, loading, error] = useAuthState(auth);
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const fetchUserName = async () => {
    try {
      const q = query(collection(db, "users"), where("uid", "==", user?.uid));
      const querySnapshot = await getDocs(q);
      if (!querySnapshot.empty) {
        const data = querySnapshot.docs[0].data();
        setName(data.name || "");
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
    <div className="bg-black-400 min-h-screen flex items-center justify-center">
      <div className="bg-white text-black px-8 py-6 rounded-lg shadow-lg text-center">
        {loading ? (
          <div>Loading...</div>
        ) : (
          <>
            {name ? (
              <>
                <div className="text-2xl font-bold mb-4">{name}</div>
                <div className="mb-6">{user?.email}</div>
              </>
            ) : (
              <div>Name not available</div>
            )}
            <button className="bg-blue-700 hover:bg-blue-600 text-white px-4 py-2 rounded-lg mx-auto" onClick={logout}>
              Logout
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default Profile;
