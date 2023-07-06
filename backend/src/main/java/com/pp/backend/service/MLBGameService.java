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
            String query = "SELECT gameId, homeTeamName, awayTeamName, gameStatus, gameDate, gameTime, isWinnerHome, isWinnerAway" +
                    "FROM gamesRefresh";

            PreparedStatement statement = connection.prepareStatement(query);
            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                String gameId = resultSet.getString("game_id");
                String homeTeam = resultSet.getString("homeTeamName");
                String awayTeam = resultSet.getString("awayTeamName");
                String status = resultSet.getString("gameStatus");
                String gameTime = resultSet.getString("gameTime");
                String gameDate = resultSet.getString("gameDate");
                String isWinnerHome = resultSet.getString("isWinnerHome");
                String isWinnerAway = resultSet.getString("isWinnerAway");

                MLBGame mlbGame = new MLBGame(gameId, homeTeam, awayTeam, status, gameTime, gameDate, isWinnerHome, isWinnerAway);
                mlbGames.add(mlbGame);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return mlbGames;
    }
}
