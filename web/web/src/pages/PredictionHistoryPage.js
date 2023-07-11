import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PredictionHistoryPage = () => {
  const [predictionHistory, setPredictionHistory] = useState(null);
  const [teamRecords, setTeamRecords] = useState(null);

  useEffect(() => {
    const fetchPredictionHistory = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/prediction-history');
        setPredictionHistory(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    const fetchTeamRecords = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/team-records');
        setTeamRecords(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPredictionHistory();
    fetchTeamRecords();
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

  const formatTeamRecords = (teamRecords) => {
    if (!teamRecords || teamRecords.length === 0) {
      return null;
    }
    const sortedTeamRecords = teamRecords.sort((a, b) => a.teamName.localeCompare(b.teamName)); // Sort the teamRecords array alphabetically by teamName
    return sortedTeamRecords.map((teamRecord) => {
      const { teamName, numerator, denominator, percentage } = teamRecord;
      const formattedPercentage = (percentage * 100).toFixed(2); // Multiply by 100 and format to 2 decimal places
      return `${teamName}: ${numerator}/${denominator} (${formattedPercentage}%)`;
    }).join('\n');
  };

  return (
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
      {teamRecords && (
        <>
          <h2 className="text-2xl font-bold mt-4">Team Records</h2>
          <ul className="prediction-list">
            {formatTeamRecords(teamRecords).split('\n').map((teamRecord, index) => (
              <li key={index} className="mb-2">
                {teamRecord}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default PredictionHistoryPage;
