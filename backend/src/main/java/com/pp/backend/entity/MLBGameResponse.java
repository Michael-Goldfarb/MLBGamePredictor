package com.pp.backend.entity;
import com.pp.backend.entity.MLBGame;
import com.pp.backend.entity.Prediction;

public class MLBGameResponse {
    private MLBGame mlbGame;
    private Prediction prediction;

    public MLBGameResponse(MLBGame mlbGame) {
        this.mlbGame = mlbGame;
    }

    public MLBGame getMlbGame() {
        return mlbGame;
    }

    public void setMlbGame(MLBGame mlbGame) {
        this.mlbGame = mlbGame;
    }

    public Prediction getPrediction() {
        return prediction;
    }

    public void setPrediction(Prediction prediction) {
        this.prediction = prediction;
    }
}
