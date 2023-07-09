package com.pp.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.pp.backend.entity.PredictionHistory;
import com.pp.backend.service.PredictionHistoryService;

@RestController
@RequestMapping("/api/prediction-history")
public class PredictionHistoryController {
    private final PredictionHistoryService predictionHistoryService;

    public PredictionHistoryController(PredictionHistoryService predictionHistoryService) {
        this.predictionHistoryService = predictionHistoryService;
    }

    @GetMapping
    public ResponseEntity<PredictionHistory> getPredictionHistory() {
        PredictionHistory predictionHistory = predictionHistoryService.getPredictionHistory();
        return ResponseEntity.ok(predictionHistory);
    }
}
