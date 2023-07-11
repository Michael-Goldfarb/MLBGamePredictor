package com.pp.backend.config;
import javax.sql.DataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pp.backend.service.MLBGameService;
// import com.pp.backend.service.UserService;
import com.pp.backend.service.PredictionService;
import com.pp.backend.service.PredictionHistoryService;
import com.pp.backend.service.TeamRecordService;

@Configuration
public class AppConfig {

    @Value("${spring.datasource.driver-class-name}")
    private String driverClassName;

    @Value("${spring.datasource.url}")
    private String url;

    @Value("${spring.datasource.username}")
    private String username;

    @Value("${spring.datasource.password}")
    private String password;

    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName(driverClassName);
        dataSource.setUrl(url);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return dataSource;
    }

    // @Bean
    // public UserService userService(DataSource dataSource) {
    //     return new UserService(dataSource);
    // }

    @Bean
    public PredictionService predictionService(DataSource dataSource) {
        return new PredictionService(dataSource);
    }

    @Bean
    public TeamRecordService teamRecordService(DataSource dataSource) {
        return new TeamRecordService(dataSource);
    }

    @Bean
    public PredictionHistoryService predictionHistoryService(DataSource dataSource) {
        return new PredictionHistoryService(dataSource);
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }

    @Bean
    public MLBGameService mlbGameService(DataSource dataSource) {
        return new MLBGameService(dataSource);
    }


    // Other bean definitions and configurations...
}
