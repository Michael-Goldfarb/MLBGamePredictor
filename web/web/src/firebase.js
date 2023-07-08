import { initializeApp } from "firebase/app";
import {
  GoogleAuthProvider,
  getAuth,
  signInWithPopup,
  signOut,
} from "firebase/auth";
import {
  initializeFirestore,
  query,
  getDocs,
  collection,
  where,
  addDoc,
} from "firebase/firestore";
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDbS_yJYrLhAj55r639pdhb6kYINT-efi8",
  authDomain: "mlbgamepredictor.firebaseapp.com",
  databaseURL: "https://mlbgamepredictor-default-rtdb.firebaseio.com",
  projectId: "mlbgamepredictor",
  storageBucket: "mlbgamepredictor.appspot.com",
  messagingSenderId: "540979386958",
  appId: "1:540979386958:web:1eeb534adc2228c4f3c11f",
  measurementId: "G-5GT94Y3VBB"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const firestore = initializeFirestore(app, {
  experimentalForceLongPolling: true,
  useFetchStreams: false,
});

const googleProvider = new GoogleAuthProvider();
const signInWithGoogle = async () => {
  try {
    const res = await signInWithPopup(auth, googleProvider);
    const user = res.user;
    const q = query(collection(firestore, "users"), where("uid", "==", user.uid));
    const docs = await getDocs(q);
    if (docs.docs.length === 0) {
      await addDoc(collection(firestore, "users"), {
        uid: user.uid,
        name: user.displayName,
        authProvider: "google",
        email: user.email,
      });
    }
    console.log("User signed in:");
    console.log("Name:", user.displayName);
    console.log("Email:", user.email);
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
};

const logout = () => {
  signOut(auth);
};

export { auth, firestore as db, signInWithGoogle, logout };
