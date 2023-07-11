package com.pp.backend.service;
import com.pp.backend.entity.Prediction;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;

public class PredictionService {
    private final DataSource dataSource;

    public PredictionService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<Prediction> getPredictions() {
        List<Prediction> predictions = new ArrayList<>();

        try (Connection connection = dataSource.getConnection()) {
            String query = "SELECT gameId, earlyWinner, theWinner, featuredWinner " +
                    "FROM games";

            PreparedStatement statement = connection.prepareStatement(query);
            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                String gameId = resultSet.getString("gameId");
                String earlyWinner = resultSet.getString("earlyWinner");
                String theWinner = resultSet.getString("theWinner");
                String featuredWinner = resultSet.getString("featuredWinner");

                Prediction prediction = new Prediction(gameId, earlyWinner);
                if (theWinner != null && !theWinner.isEmpty()) {
                    prediction.setPrediction(theWinner);
                }

                predictions.add(prediction);
                if (featuredWinner != null && !featuredWinner.isEmpty()) {
                    Prediction featuredPrediction = new Prediction(gameId, featuredWinner);
                    predictions.add(featuredPrediction);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return predictions;
    }
}
