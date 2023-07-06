import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './PredictionsPage.css';

const PredictionsPage = () => {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('/api/predictions'); // Replace with your backend API endpoint for predictions
        setPredictions(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPredictions();
  }, []);

  return (
    <div className="predictions-page">
      <h1 className="predictions-title">MLB Game Predictions</h1>
      {predictions.map((prediction) => (
        <div key={prediction.gameId} className="prediction-item">
          <h2>Game ID: {prediction.gameId}</h2>
          <p>Early Winner: {prediction.earlyWinner}</p>
          <p>Prediction: {prediction.prediction}</p>
        </div>
      ))}
    </div>
  );
};

export default PredictionsPage;