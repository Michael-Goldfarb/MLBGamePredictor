import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './PredictionsPage.css';
import metsLogo from "../images/mets.png";
import yankeesLogo from "../images/yankees.png";
import oriolesLogo from "../images/orioles.png";
import redsoxLogo from "../images/redsox.png";
import raysLogo from "../images/rays.png";
import bluejaysLogo from "../images/bluejays.png";
import bravesLogo from "../images/braves.png";
import philliesLogo from "../images/phillies.png";
import marlinsLogo from "../images/marlins.png";
import nationalsLogo from "../images/nationals.png";
import guardiansLogo from"../images/guardians.png";
import piratesLogo from "../images/pirates.png";
import tigersLogo from "../images/tigers.png";
import brewersLogo from "../images/brewers.png";
import cardinalsLogo from "../images/cardinals.png";
import whitesoxLogo from "../images/whitesox.png";
import cubsLogo from "../images/cubs.png";
import royalsLogo from "../images/royals.png";
import twinsLogo from "../images/twins.png";
import rangersLogo from "../images/rangers.png";
import redsLogo from "../images/reds.png";
import angelsLogo from "../images/angels.png";
import padresLogo from "../images/padres.png";
import dodgersLogo from "../images/dodgers.png";
import athleticsLogo from "../images/athletics.png";
import marinersLogo from "../images/mariners.png";
import astrosLogo from "../images/astros.png";
import rockiesLogo from "../images/rockies.png";
import diamondbacksLogo from "../images/diamondbacks.png";
import giantsLogo from "../images/giants.png";

const PredictionsPage = () => {
  const [predictions, setPredictions] = useState([]);
  const teamLogos = {
    "Arizona Diamondbacks": diamondbacksLogo,
    "Atlanta Braves": bravesLogo,
    "Baltimore Orioles": oriolesLogo,
    "Boston Red Sox": redsoxLogo,
    "Chicago Cubs": cubsLogo,
    "Chicago White Sox": whitesoxLogo,
    "Cincinnati Reds": redsLogo,
    "Cleveland Guardians": guardiansLogo,
    "Colorado Rockies": rockiesLogo,
    "Detroit Tigers": tigersLogo,
    "Houston Astros": astrosLogo,
    "Kansas City Royals": royalsLogo,
    "Los Angeles Angels": angelsLogo,
    "Los Angeles Dodgers": dodgersLogo,
    "Miami Marlins": marlinsLogo,
    "Milwaukee Brewers": brewersLogo,
    "Minnesota Twins": twinsLogo,
    "New York Mets": metsLogo,
    "New York Yankees": yankeesLogo,
    "Oakland Athletics": athleticsLogo,
    "Philadelphia Phillies": philliesLogo,
    "Pittsburgh Pirates": piratesLogo,
    "San Diego Padres": padresLogo,
    "San Francisco Giants": giantsLogo,
    "Seattle Mariners": marinersLogo,
    "St. Louis Cardinals": cardinalsLogo,
    "Tampa Bay Rays": raysLogo,
    "Texas Rangers": rangersLogo,
    "Toronto Blue Jays": bluejaysLogo,
    "Washington Nationals": nationalsLogo,
  };
  

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

  const convertToLocalTime = (gameTime) => {
    const [hours, minutes] = gameTime.split(':');
    const localTime = new Date();
    localTime.setUTCHours(hours);
    localTime.setUTCMinutes(minutes);

    const options = { hour12: true, hour: 'numeric', minute: 'numeric' };
    return localTime.toLocaleString('en-US', options);
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
              <div className="logo-container">
                <img src={teamLogos[data.mlbGame.awayTeamName]} alt={data.mlbGame.awayTeamName} />
              </div>
              <div className="team-name-score">
                <p>{data.mlbGame.awayTeamName}</p>
                <p>{data.mlbGame.awayTeamScore}</p>
              </div>
            </div>
            <div className="inning-info">
              <p className="current-inning">
                {data.mlbGame.inningHalf ? `${data.mlbGame.inningHalf} of the ` : ''}{data.mlbGame.currentInning ? `${data.mlbGame.currentInning}` : 'Game not started'}
              </p>
            </div>
            <div className="home-team">
              <div className="team-name-score">
                <p>{data.mlbGame.homeTeamName}</p>
                <p>{data.mlbGame.homeTeamScore}</p>
              </div>
              <div className="logo-container">
                <img src={teamLogos[data.mlbGame.homeTeamName]} alt={data.mlbGame.homeTeamName} />
              </div>
            </div>
          </div>
          <p className="game-time">{convertToLocalTime(data.mlbGame.gameTime)}</p>
          <p className={`prediction ${data.mlbGame.correct === null ? 'white' : (data.mlbGame.correct ? 'green' : 'red')}`}>
            Prediction: {data.prediction?.prediction}
          </p>
        </div>
      ))}
    </div>
  );
};

export default PredictionsPage;
