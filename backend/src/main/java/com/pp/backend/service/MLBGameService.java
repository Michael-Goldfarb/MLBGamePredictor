package com.pp.backend.service;
import com.pp.backend.entity.MLBGame;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;

public class MLBGameService {
    private final DataSource dataSource;

    public MLBGameService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<MLBGame> getMLBGames() {
        List<MLBGame> mlbGames = new ArrayList<>();

        try (Connection connection = dataSource.getConnection()) {
            String query = "SELECT gameId, homeTeamName, awayTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, isWinnerHome, isWinnerAway, featuredWinner, correct, currentInning, inningHalf " +
                    "FROM gamesRefresh " +
                    "ORDER BY gameDate ASC, gameTime ASC";

            PreparedStatement statement = connection.prepareStatement(query);
            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                String gameId = resultSet.getString("gameId");
                String homeTeam = resultSet.getString("homeTeamName");
                String awayTeam = resultSet.getString("awayTeamName");
                String status = resultSet.getString("gameStatus");
                String gameDate = resultSet.getString("gameDate");
                String gameTime = resultSet.getString("gameTime");
                String awayTeamScore = resultSet.getString("awayTeamScore");
                String homeTeamScore = resultSet.getString("homeTeamScore");
                String currentInning = resultSet.getString("currentInning");
                String inningHalf = resultSet.getString("inningHalf");
                Boolean isWinnerHome = resultSet.getBoolean("isWinnerHome");
                Boolean isWinnerAway = resultSet.getBoolean("isWinnerAway");
                String featuredWinner = resultSet.getString("featuredWinner");
                Boolean correct = resultSet.getObject("correct", Boolean.class);

                MLBGame mlbGame = new MLBGame(gameId, homeTeam, awayTeam, status, gameDate, gameTime, awayTeamScore, homeTeamScore, isWinnerHome, isWinnerAway, featuredWinner, correct, currentInning, inningHalf);
                mlbGames.add(mlbGame);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return mlbGames;
    }
}