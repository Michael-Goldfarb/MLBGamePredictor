package com.pp.backend.entity;
import com.fasterxml.jackson.annotation.JsonProperty;

public class MLBGame {
    @JsonProperty("gameId")
    private String gameId;

    @JsonProperty("homeTeamName")
    private String homeTeam;

    @JsonProperty("awayTeamName")
    private String awayTeam;

    @JsonProperty("gameStatus")
    private String status;

    @JsonProperty("gameDate")
    private String gameDate;
    
    @JsonProperty("gameTime")
    private String gameTime;

    @JsonProperty("awayTeamScore")
    private String awayTeamScore;

    @JsonProperty("homeTeamScore")
    private String homeTeamScore;

    @JsonProperty("isWinnerHome")
    private Boolean isWinnerHome;

    @JsonProperty("isWinnerAway")
    private Boolean isWinnerAway;

    public MLBGame() {
    }

    public MLBGame(String gameId, String homeTeam, String awayTeam, String status, String gameDate, String gameTime, String awayTeamScore, String homeTeamScore, Boolean isWinnerHome, Boolean isWinnerAway) {
        this.gameId = gameId;
        this.homeTeam = homeTeam;
        this.awayTeam = awayTeam;
        this.status = status;
        this.gameDate = gameDate;
        this.gameTime = gameTime;
        this.awayTeamScore = awayTeamScore;
        this.homeTeamScore = homeTeamScore;
        this.isWinnerHome = isWinnerHome;
        this.isWinnerAway = isWinnerAway;
    }

    public String getGameId() {
        return gameId;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }

    public String getHomeTeam() {
        return homeTeam;
    }

    public void setHomeTeam(String homeTeam) {
        this.homeTeam = homeTeam;
    }

    public String getAwayTeam() {
        return awayTeam;
    }

    public void setAwayTeam(String awayTeam) {
        this.awayTeam = awayTeam;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getGameDate() {
        return gameDate;
    }

    public void setGameDate(String gameDate) {
        this.gameDate = gameDate;
    }
    
    public String getGameTime() {
        return gameTime;
    }

    public void setGameTime(String gameTime) {
        this.gameTime = gameTime;
    }

    public String getAwayTeamScore() {
        return awayTeamScore;
    }

    public void setAwayTeamScore(String awayTeamScore) {
        this.awayTeamScore = awayTeamScore;
    }

    public String getHomeTeamScore() {
        return homeTeamScore;
    }

    public void setHomeTeamScore(String homeTeamScore) {
        this.homeTeamScore = homeTeamScore;
    }

    public Boolean getIsWinnerHome() {
        return isWinnerHome;
    }

    public void setIsWinnerHome(Boolean isWinnerHome) {
        this.isWinnerHome = isWinnerHome;
    }

    public Boolean getIsWinnerAway() {
        return isWinnerAway;
    }

    public void setIsWinnerAway(Boolean isWinnerAway) {
        this.isWinnerAway = isWinnerAway;
    }
}