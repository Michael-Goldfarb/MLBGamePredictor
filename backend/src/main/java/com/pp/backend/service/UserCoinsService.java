package com.pp.backend.service;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;
import com.pp.backend.entity.UserCoins;
import java.sql.PreparedStatement;

public class UserCoinsService {
    private final DataSource dataSource;

    public UserCoinsService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<UserCoins> getUsersCoins() {
        List<UserCoins> usersCoins = new ArrayList<>();

        // Establish a connection to your database
        try (Connection connection = dataSource.getConnection()) {
            // Create a statement to execute the SQL query
            try (Statement statement = connection.createStatement()) {
                // Execute the query and retrieve the result set
                ResultSet resultSet = statement.executeQuery("SELECT * FROM user_coins");

                // Process the result set and map it to User objects
                while (resultSet.next()) {
                    UserCoins userCoins = new UserCoins();
                    userCoins.setEmail(resultSet.getString("email"));
                    userCoins.setCoin_balance(resultSet.getInt("coin_balance"));

                    usersCoins.add(userCoins);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return usersCoins;
    }
    

}
