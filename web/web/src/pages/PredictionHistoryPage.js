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
      const formattedPrediction = `${numerator}/${denominator}`;
  
      return `Prediction History\n${formattedDate}: ${formattedPrediction}`;
    };
  
    return (
      <div className="prediction-history-page">
        <h1>Prediction History</h1>
        {predictionHistory && (
          <div className="prediction-history">
            {formatPredictionHistory(predictionHistory)}
          </div>
        )}
      </div>
    );
  };
  
  export default PredictionHistoryPage;
  