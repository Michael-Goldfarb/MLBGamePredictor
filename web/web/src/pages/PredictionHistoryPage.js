import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './PredictionHistoryPage.css';

const PredictionHistoryPage = () => {
  const [predictionHistory, setPredictionHistory] = useState(null);
  const [teamRecords, setTeamRecords] = useState(null);
  const [sortType, setSortType] = useState(''); // Track the current sort type

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

    let sortedTeamRecords = [...teamRecords]; // Create a copy of the teamRecords array

    // Sort the teamRecords based on the current sort type
    if (sortType === 'highest') {
      sortedTeamRecords.sort((a, b) => b.percentage - a.percentage);
    } else if (sortType === 'lowest') {
      sortedTeamRecords.sort((a, b) => a.percentage - b.percentage);
    }

    return sortedTeamRecords.map((teamRecord) => {
      const { teamName, numerator, denominator, percentage } = teamRecord;
      const formattedPercentage = (percentage * 100).toFixed(2);
      return `${teamName}: ${numerator}/${denominator} (${formattedPercentage}%)`;
    }).join('\n');
  };

  const handleSortByHighest = () => {
    setSortType('highest');
  };

  const handleSortByLowest = () => {
    setSortType('lowest');
  };

  return (
    <div className="prediction-history-page bg-gray-800 min-h-screen flex flex-col items-center justify-center py-10">
  <div className="container flex mr-12">
    <div className="left-section w-3/4 text-center column prediction-history-column">
      <h1 className="column-heading">Prediction History</h1>
      {predictionHistory && (
        <ul className="prediction-list">
          {formatPredictionHistory(predictionHistory).split('\n').map((prediction, index) => (
            <li key={index} className="mb-3">
              {prediction}
            </li>
          ))}
        </ul>
      )}
    </div>
    <div className="right-section w-1/2 text-center column">
      <h1 className="column-heading">Team Records</h1>
      <div className="sort-button-container">
        <button className="sort-button" onClick={handleSortByHighest}>
          Sort by Highest
        </button>
        <button className="sort-button" onClick={handleSortByLowest}>
          Sort by Lowest
        </button>
      </div>
      {teamRecords && (
        <ul className="prediction-list">
          {formatTeamRecords(teamRecords).split('\n').map((teamRecord, index) => (
            <li key={index} className="mb-3">
              {teamRecord}
            </li>
          ))}
        </ul>
      )}
    </div>
  </div>
</div>

  );
};

export default PredictionHistoryPage;
