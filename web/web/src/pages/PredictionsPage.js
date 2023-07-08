import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './PredictionsPage.css';

const PredictionsPage = () => {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/games');
        console.log(response.data);
        setPredictions(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPredictions();
  }, []);

  const convertToEST = (gameTime) => {
    const [hours, minutes] = gameTime.split(':');
    const estTime = new Date();
    estTime.setUTCHours(hours);
    estTime.setUTCMinutes(minutes);

    const options = { timeZone: 'America/New_York', hour12: true, hour: 'numeric', minute: 'numeric' };
    return estTime.toLocaleString('en-US', options);
  };

  return (
    <div className="predictions-page">
      <div className="predictions-title-wrapper">
        <h1 className="predictions-title">MLB Game Predictions</h1>
      </div>
      {predictions.map((data) => (
        <div key={data.mlbGame.gameId} className="prediction-item">
          <div className="team-info">
            <div className="away-team">
              <p>{data.mlbGame.awayTeamName}</p>
              <p>{data.mlbGame.awayTeamScore}</p>
            </div>
            <div className="home-team">
              <p>{data.mlbGame.homeTeamName}</p>
              <p>{data.mlbGame.homeTeamScore}</p>
            </div>
          </div>
          {data.mlbGame.isWinnerHome || data.mlbGame.isWinnerAway ? <p className="game-status">Final</p> : null}
          <p className="game-time">{convertToEST(data.mlbGame.gameTime)}</p>
          <p className="prediction">Prediction: {data.prediction?.prediction}</p>
        </div>
      ))}
    </div>
  );
};

export default PredictionsPage;