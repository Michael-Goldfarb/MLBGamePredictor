import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PredictionHistoryPage = () => {
  const [predictionHistory, setPredictionHistory] = useState(null);

  useEffect(() => {
    const fetchPredictionHistory = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/prediction-history');
        setPredictionHistory(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPredictionHistory();
  }, []);

  const formatPredictionHistory = (predictionHistory) => {
    if (!predictionHistory) {
      return null;
    }

    const { predictionDate, numerator, denominator } = predictionHistory;

    const formattedDate = predictionDate.substring(5).replace('-', '/');
    const formattedPrediction = `${formattedDate}: ${numerator}/${denominator}`;

    return formattedPrediction;
  };

  return (
    <div className="prediction-history-page bg-gray-800 min-h-screen flex flex-col items-center justify-start py-10">
      <div className="prediction-history-container text-white text-center">
        <h1 className="text-4xl font-bold mb-4">Prediction History</h1>
        {predictionHistory && (
          <ul className="prediction-list">
            {formatPredictionHistory(predictionHistory).split('\n').map((prediction, index) => (
              <li key={index} className="mb-2">
                {prediction}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default PredictionHistoryPage;
