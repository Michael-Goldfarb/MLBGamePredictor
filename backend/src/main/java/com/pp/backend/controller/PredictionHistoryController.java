package com.pp.backend.controller;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.pp.backend.entity.PredictionHistory;
import com.pp.backend.service.PredictionHistoryService;
import java.util.List;

@RestController
@RequestMapping("/api/prediction-history")
public class PredictionHistoryController {
    private final PredictionHistoryService predictionHistoryService;

    public PredictionHistoryController(PredictionHistoryService predictionHistoryService) {
        this.predictionHistoryService = predictionHistoryService;
    }

    @GetMapping
    public ResponseEntity<List<PredictionHistory>> getPredictionHistory() {
        List<PredictionHistory> predictionHistoryList = predictionHistoryService.getPredictionHistory();
        return ResponseEntity.ok(predictionHistoryList);
    }
}