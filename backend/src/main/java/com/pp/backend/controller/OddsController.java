package com.pp.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

import com.pp.backend.entity.Odds;
import com.pp.backend.service.OddsService;

@RestController
@RequestMapping("/planetpicksodds")
public class OddsController {
    private final OddsService oddsService;

    public OddsController(OddsService oddsService) {
        this.oddsService = oddsService;
    }

    @GetMapping
    public ResponseEntity<List<Odds>> getOdds() {
        List<Odds> oddsList = oddsService.getOdds();
        return ResponseEntity.ok(oddsList);
    }
}
