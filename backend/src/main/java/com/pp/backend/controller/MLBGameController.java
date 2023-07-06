package com.pp.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import com.pp.backend.entity.MLBGameResponse;
import com.pp.backend.entity.MLBGame;
import com.pp.backend.service.MLBGameService;

@RestController
@RequestMapping("/games")
public class MLBGameController {
    private final MLBGameService mlbGameService;

    public MLBGameController(MLBGameService mlbGameService) {
        this.mlbGameService = mlbGameService;
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
