package com.pp.backend.controller;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.ArrayList;
import com.pp.backend.entity.Prediction;
import com.pp.backend.entity.MLBGameResponse;
import com.pp.backend.entity.MLBGame;
import com.pp.backend.service.MLBGameService;
import com.pp.backend.service.PredictionService;


@RestController
@RequestMapping("/games")
public class MLBGameController {
    private final MLBGameService mlbGameService;
    private final PredictionService predictionService; // Add this line

    public MLBGameController(MLBGameService mlbGameService, PredictionService predictionService) { // Update the constructor
        this.mlbGameService = mlbGameService;
        this.predictionService = predictionService; // Initialize the predictionService
    }

    @GetMapping
    public ResponseEntity<List<MLBGameResponse>> getMLBGames() {
        List<MLBGame> mlbGames = mlbGameService.getMLBGames();
        List<Prediction> predictions = predictionService.getPredictions();

        List<MLBGameResponse> combinedData = new ArrayList<>();
        for (MLBGame mlbGame : mlbGames) {
            MLBGameResponse mlbGameResponse = new MLBGameResponse(mlbGame);
            for (Prediction prediction : predictions) {
                if (mlbGame.getGameId().equals(prediction.getGameId())) {
                    mlbGameResponse.setPrediction(prediction);
                    break;
                }
            }
            combinedData.add(mlbGameResponse);
        }

        return ResponseEntity.ok(combinedData);
    }

}
