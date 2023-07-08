package com.pp.backend.entity;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Prediction {
    @JsonProperty("gameId")
    private String gameId;

    @JsonProperty("prediction")
    private String prediction;

    public Prediction() {
    }

    public Prediction(String gameId, String prediction) {
        this.gameId = gameId;
        this.prediction = prediction;
    }

    public String getGameId() {
        return gameId;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }

    public String getPrediction() {
        return prediction;
    }

    public void setPrediction(String prediction) {
        this.prediction = prediction;
    }
}
