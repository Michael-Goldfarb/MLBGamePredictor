package com.pp.backend.service;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;
import com.pp.backend.entity.User;
import java.sql.PreparedStatement;

public class UserService {
    private final DataSource dataSource;

    public UserService(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<User> getUsers() {
        List<User> users = new ArrayList<>();

        // Establish a connection to your database
        try (Connection connection = dataSource.getConnection()) {
            // Create a statement to execute the SQL query
            try (Statement statement = connection.createStatement()) {
                // Execute the query and retrieve the result set
                ResultSet resultSet = statement.executeQuery("SELECT * FROM user_data");

                // Process the result set and map it to User objects
                while (resultSet.next()) {
                    User user = new User();
                    user.setEmail(resultSet.getString("email"));
                    user.setName(resultSet.getString("name"));
                    users.add(user);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return users;
    }
    public User createUser(User user) {
        String sql = "INSERT INTO user_data (email, name) VALUES (?, ?)";

        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {

            statement.setString(1, user.getEmail());
            statement.setString(2, user.getName());


            int rowsAffected = statement.executeUpdate();
            if (rowsAffected > 0) {
                return user;
            } else {
                throw new SQLException("Unable to create user");
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }

}
