package com.pp.backend.entity;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.*;

public class Odds {
    @JsonProperty("id")
    private String eventId;

    @JsonProperty("sport_title")
    private String sport;

    @JsonProperty("home_team")
    private String teamA;

    @JsonProperty("away_team")
    private String teamB;

    private double oddsA;
    private double oddsB;
    private double oddsDraw;

    @JsonProperty("fetched_at")
    private String fetchedAt;

    @JsonProperty("commence_time")
    private String commence_time;

    private String winner;

    public Odds() {
    }

    public Odds(String eventId, String sport, String teamA, String teamB, double oddsA, double oddsB, double oddsDraw, String fetchedAt, String winner) {
        this.eventId = eventId;
        this.sport = sport;
        this.teamA = teamA;
        this.teamB = teamB;
        this.oddsA = oddsA;
        this.oddsB = oddsB;
        this.oddsDraw = oddsDraw;
        this.fetchedAt = fetchedAt;
        this.winner = winner;
    }
    public Odds(String eventId, String sport, String teamA, String teamB, double oddsA, double oddsB, double oddsDraw, String fetchedAt, String winner, String commence_time) {
        this.eventId = eventId;
        this.sport = sport;
        this.teamA = teamA;
        this.teamB = teamB;
        this.oddsA = oddsA;
        this.oddsB = oddsB;
        this.oddsDraw = oddsDraw;
        this.fetchedAt = fetchedAt;
        this.winner = winner;
        this.commence_time = commence_time;
    }
    public Odds(String eventId, String sport, String teamA, String teamB, double oddsA, double oddsB, String fetchedAt) {
        this.eventId = eventId;
        this.sport = sport;
        this.teamA = teamA;
        this.teamB = teamB;
        this.oddsA = oddsA;
        this.oddsB = oddsB;
        this.fetchedAt = fetchedAt;
    }

    public Odds(String eventId, String sport, String teamA, String teamB, double oddsA, double oddsB, String fetchedAt, String commence_time) {
        this.eventId = eventId;
        this.sport = sport;
        this.teamA = teamA;
        this.teamB = teamB;
        this.oddsA = oddsA;
        this.oddsB = oddsB;
        this.fetchedAt = fetchedAt;
        this.commence_time = commence_time;
    }

    public String getEventId() {
        return eventId;
    }

    public void setEventId(String eventId) {
        this.eventId = eventId;
    }

    public String getSport() {
        return sport;
    }

    public void setSport(String sport) {
        this.sport = sport;
    }

    public String getTeamA() {
        return teamA;
    }

    public void setTeamA(String teamA) {
        this.teamA = teamA;
    }

    public String getTeamB() {
        return teamB;
    }

    public void setTeamB(String teamB) {
        this.teamB = teamB;
    }

    public double getOddsA() {
        return oddsA;
    }

    public void setOddsA(double oddsA) {
        this.oddsA = oddsA;
    }

    public double getOddsB() {
        return oddsB;
    }

    public void setOddsB(double oddsB) {
        this.oddsB = oddsB;
    }

    public double getOddsDraw() {
        return oddsDraw;
    }

    public void setOddsDraw(double oddsDraw) {
        this.oddsDraw = oddsDraw;
    }

    public String getFetchedAt() {
        return fetchedAt;
    }

    public void setFetchedAt(String fetchedAt) {
        this.fetchedAt = fetchedAt;
    }

    public String getCommenceTime(){
        return commence_time;
    }

    public void setCommenceTime(String commence_time){
        this.commence_time = commence_time;
    }

    public String getWinner() {
        return winner;
    }

    public void setWinner(String winner) {
        this.winner = winner;
    }

    public static class Bookmaker {
        private String key;
        private String title;
        private String last_update;
        private List<Market> markets;

        // Getters and Setters
    }

    public static class Market {
        private String key;
        private String last_update;
        private List<Outcome> outcomes;

        // Getters and Setters
    }

    public static class Outcome {
        private String name;
        private double price;

        // Getters and Setters
    }
}
