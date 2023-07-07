import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './PredictionsPage.css';

const PredictionsPage = () => {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/games')
        console.log(response.data);
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
      {predictions.map((data) => (
        <div key={data.mlbGame.gameId} className="prediction-item">
          <p>Home Team: {data.mlbGame.homeTeamName}</p>
          <p>Away Team: {data.mlbGame.awayTeamName}</p>
          <p>Score: {data.mlbGame.homeTeamScore} - {data.mlbGame.awayTeamScore}</p>
          {data.mlbGame.isWinnerHome || data.mlbGame.isWinnerAway ? <p>Final</p> : null}
          <p>Date: {data.mlbGame.gameDate}</p>
          <p>Time: {data.mlbGame.gameTime}</p>
          <p>Prediction: {data.prediction?.prediction}</p>
        </div>
      ))}
    </div>
  );
};

export default PredictionsPage;