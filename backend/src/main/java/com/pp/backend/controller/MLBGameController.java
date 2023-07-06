package com.pp.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
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
    public ResponseEntity<List<MLBGame>> getMLBGames() {
        List<MLBGame> mlbGames = mlbGameService.getMLBGames();
        return ResponseEntity.ok(mlbGames);
    }
}
