package com.pp.backend.service;
import com.pp.backend.entity.PredictionHistory;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Date;

public class PredictionHistoryService {
    private final DataSource dataSource;

    public PredictionHistoryService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public PredictionHistory getPredictionHistory() {
        PredictionHistory predictionHistory = null;

        try (Connection connection = dataSource.getConnection()) {
            String query = "SELECT prediction_date, numerator, denominator FROM dailyPredictions ORDER BY prediction_date DESC LIMIT 1";

            PreparedStatement statement = connection.prepareStatement(query);
            ResultSet resultSet = statement.executeQuery();

            if (resultSet.next()) {
                String predictionDate = resultSet.getString("prediction_date");
                int numerator = resultSet.getInt("numerator");
                int denominator = resultSet.getInt("denominator");

                predictionHistory = new PredictionHistory(predictionDate, numerator, denominator);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return predictionHistory;
    }
}
