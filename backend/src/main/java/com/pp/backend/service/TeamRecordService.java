package com.pp.backend.service;
import com.pp.backend.entity.TeamRecord;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class TeamRecordService {
    private final DataSource dataSource;

    public TeamRecordService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<TeamRecord> getTeamRecords() {
        List<TeamRecord> teamRecords = new ArrayList<>();

        try (Connection connection = dataSource.getConnection()) {
            String query = "SELECT teamName, numerator, denominator, percentage FROM teamRecords";

            PreparedStatement statement = connection.prepareStatement(query);
            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                String teamName = resultSet.getString("teamName");
                int numerator = resultSet.getInt("numerator");
                int denominator = resultSet.getInt("denominator");
                float percentage = resultSet.getFloat("percentage");

                TeamRecord teamRecord = new TeamRecord(teamName, numerator, denominator, percentage);
                teamRecords.add(teamRecord);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return teamRecords;
    }
}
