package com.pp.backend.service;
import com.pp.backend.entity.PredictionHistory;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Date;
import java.util.ArrayList;
import java.util.List;

public class PredictionHistoryService {
    private final DataSource dataSource;

    public PredictionHistoryService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<PredictionHistory> getPredictionHistory() {
        List<PredictionHistory> predictionHistoryList = new ArrayList<>();

        try (Connection connection = dataSource.getConnection()) {
            String query = "SELECT prediction_date, numerator, denominator FROM dailyPredictions ORDER BY prediction_date DESC";

            PreparedStatement statement = connection.prepareStatement(query);
            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                String predictionDate = resultSet.getString("prediction_date");
                int numerator = resultSet.getInt("numerator");
                int denominator = resultSet.getInt("denominator");

                PredictionHistory predictionHistory = new PredictionHistory(predictionDate, numerator, denominator);
                predictionHistoryList.add(predictionHistory);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return predictionHistoryList;
    }
}
