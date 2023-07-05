package com.pp.backend.service;

import com.pp.backend.entity.Odds;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.sql.Statement;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.sql.Timestamp;
import com.fasterxml.jackson.databind.type.TypeFactory;
import com.fasterxml.jackson.databind.type.CollectionType;
import javax.sql.DataSource;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;
import org.springframework.scheduling.annotation.Scheduled;

public class OddsService {
    private final DataSource dataSource;
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public OddsService(DataSource dataSource, RestTemplate restTemplate, ObjectMapper objectMapper) {
        this.dataSource = dataSource;
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
    }

    public List<Odds> getOdds() {
        List<Odds> oddsList = new ArrayList<>();

        try (Connection connection = dataSource.getConnection()) {
            try (Statement statement = connection.createStatement()) {
                // Get the current date as a string in the desired format
                LocalDate currentDate = LocalDate.now();
                LocalDate tomorrowDate = currentDate.plusDays(1);
                String currentDateString = currentDate.toString();
                String tomorrowDateString = tomorrowDate.toString();

                // Construct the SQL query
                String query = "SELECT event_id, sport, team_a, team_b, odds_a, odds_b, odds_draw, fetched_at, commence_time, winner "
                        +
                        "FROM odds " +
                        "WHERE commence_time::date = '" + currentDateString + "' OR commence_time::date = '"
                        + tomorrowDateString + "'" +
                        "ORDER BY commence_time";

                ResultSet resultSet = statement.executeQuery(query);

                while (resultSet.next()) {
                    // Retrieve the column values
                    String eventId = resultSet.getString("event_id");
                    String sport = resultSet.getString("sport");
                    String teamA = resultSet.getString("team_a");
                    String teamB = resultSet.getString("team_b");
                    double oddsA = resultSet.getDouble("odds_a");
                    double oddsB = resultSet.getDouble("odds_b");
                    double oddsDraw = resultSet.getDouble("odds_draw");
                    String fetchedAt = resultSet.getString("fetched_at");
                    String commenceTime = resultSet.getString("commence_time");
                    String winner = resultSet.getString("winner");

                    // Create the Odds object
                    Odds odds = new Odds(eventId, sport, teamA, teamB, oddsA, oddsB, oddsDraw, fetchedAt, winner,
                            commenceTime);
                    oddsList.add(odds);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return oddsList;
    }

    public static class Game {
        private String id;
        private String sport_key;
        private String sport_title;
        private String commence_time;
        private String home_team;
        private String away_team;
        private List<Bookmaker> bookmakers;

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public String getSport_key() {
            return sport_key;
        }

        public void setSport_key(String sport_key) {
            this.sport_key = sport_key;
        }

        public String getSport_title() {
            return sport_title;
        }

        public void setSport_title(String sport_title) {
            this.sport_title = sport_title;
        }

        public String getCommence_time() {
            return commence_time;
        }

        public void setCommence_time(String commence_time) {
            this.commence_time = commence_time;
        }

        public String getHome_team() {
            return home_team;
        }

        public void setHome_team(String home_team) {
            this.home_team = home_team;
        }

        public String getAway_team() {
            return away_team;
        }

        public void setAway_team(String away_team) {
            this.away_team = away_team;
        }

        public List<Bookmaker> getBookmakers() {
            return bookmakers;
        }

        public void setBookmakers(List<Bookmaker> bookmakers) {
            this.bookmakers = bookmakers;
        }
    }

    public static class Bookmaker {
        private String key;
        private String title;
        private String last_update;
        private List<Market> markets;

        public String getKey() {
            return key;
        }

        public void setKey(String key) {
            this.key = key;
        }

        public String getTitle() {
            return title;
        }

        public void setTitle(String title) {
            this.title = title;
        }

        public String getLast_update() {
            return last_update;
        }

        public void setLast_update(String last_update) {
            this.last_update = last_update;
        }

        public List<Market> getMarkets() {
            return markets;
        }

        public void setMarkets(List<Market> markets) {
            this.markets = markets;
        }
    }

    public static class Market {
        private String key;
        private String last_update;
        private List<Outcome> outcomes;

        public String getKey() {
            return key;
        }

        public void setKey(String key) {
            this.key = key;
        }

        public String getLast_update() {
            return last_update;
        }

        public void setLast_update(String last_update) {
            this.last_update = last_update;
        }

        public List<Outcome> getOutcomes() {
            return outcomes;
        }

        public void setOutcomes(List<Outcome> outcomes) {
            this.outcomes = outcomes;
        }
    }

    public static class Outcome {
        private String name;
        private double price;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public double getPrice() {
            return price;
        }

        public void setPrice(double price) {
            this.price = price;
        }
    }

    @Scheduled(fixedRate = 3600000) // Run every hour (3,600,000 milliseconds)
    public void fetchOdds() {
        String apiUrl = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?regions=us&oddsFormat=american&bookmakers=fanduel,barstool,draftkings,betmgm&apiKey=7584c30c6bfaad63cb22396ca6bd979d";

        ResponseEntity<String> response = restTemplate.exchange(apiUrl, HttpMethod.GET, null, String.class);
        if (response.getStatusCode().is2xxSuccessful()) {
            try {
                String responseBody = response.getBody();
                if (responseBody != null) {
                    ObjectMapper objectMapper = new ObjectMapper();
                    TypeFactory typeFactory = objectMapper.getTypeFactory();
                    CollectionType collectionType = typeFactory.constructCollectionType(List.class, Game.class);
                    List<Game> games = objectMapper.readValue(responseBody, collectionType);

                    for (Game game : games) {
                        String eventId = game.getId();
                        String sport = game.getSport_key();
                        String teamA = game.getHome_team();
                        String teamB = game.getAway_team();
                        String fetchedAt = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME);
                        String commence_time = game.getCommence_time();

                        List<Bookmaker> bookmakers = game.getBookmakers();
                        for (Bookmaker bookmaker : bookmakers) {
                            String bookmakerKey = bookmaker.getKey();
                            String bookmakerTitle = bookmaker.getTitle();
                            String lastUpdate = bookmaker.getLast_update();

                            List<Market> markets = bookmaker.getMarkets();
                            for (Market market : markets) {
                                if ("h2h".equals(market.getKey())) {
                                    String marketLastUpdate = market.getLast_update();

                                    List<Outcome> outcomes = market.getOutcomes();
                                    if (outcomes.size() >= 2) {
                                        Outcome outcomeA = outcomes.get(0);
                                        Outcome outcomeB = outcomes.get(1);

                                        double oddsA = outcomeA.getPrice();
                                        double oddsB = outcomeB.getPrice();

                                        // Apply random modification to the odds
                                        double modifiedOddsA = applyRandomModification(oddsA);
                                        double modifiedOddsB = applyRandomModification(oddsB);

                                        // Create Odds object with modified odds only
                                        Odds odds = new Odds(eventId, sport, teamA, teamB, modifiedOddsA, modifiedOddsB,
                                                fetchedAt, commence_time);
                                        storeOdds(odds);
                                    }
                                }
                            }
                        }
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private double applyRandomModification(double odds) {
        double minModifier = 0.04; // 4%
        double maxModifier = 0.07; // 7%

        double modifier = minModifier + Math.random() * (maxModifier - minModifier);
        return odds * (1 + modifier);
    }

    private void storeOdds(Odds odds) {
        try (Connection connection = dataSource.getConnection()) {
            String selectQuery = "SELECT COUNT(*) FROM odds WHERE event_id = ?";
            PreparedStatement selectStatement = connection.prepareStatement(selectQuery);
            selectStatement.setString(1, odds.getEventId());
            ResultSet resultSet = selectStatement.executeQuery();
            resultSet.next();
            int count = resultSet.getInt(1);

            String query;
            PreparedStatement statement;
            if (count > 0) {
                query = "UPDATE odds SET odds_a = ?, odds_b = ?, fetched_at = CURRENT_TIMESTAMP, commence_time = ? WHERE event_id = ?";
                statement = connection.prepareStatement(query);
                statement.setDouble(1, odds.getOddsA());
                statement.setDouble(2, odds.getOddsB());
                statement.setString(3, odds.getCommenceTime());
                statement.setString(4, odds.getEventId());
            } else {
                query = "INSERT INTO odds (event_id, sport, team_a, team_b, odds_a, odds_b, fetched_at, commence_time) "
                        +
                        "VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)";
                statement = connection.prepareStatement(query);
                statement.setString(1, odds.getEventId());
                statement.setString(2, odds.getSport());
                statement.setString(3, odds.getTeamA());
                statement.setString(4, odds.getTeamB());
                statement.setDouble(5, odds.getOddsA());
                statement.setDouble(6, odds.getOddsB());
                statement.setString(7, odds.getCommenceTime());
            }

            statement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

}
