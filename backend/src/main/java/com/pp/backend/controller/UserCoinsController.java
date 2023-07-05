package com.pp.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

import com.pp.backend.entity.UserCoins;
import com.pp.backend.service.UserCoinsService;

@RestController
@RequestMapping("/usersCoins")
public class UserCoinsController {
    private final UserCoinsService userCoinsService;

    public UserCoinsController(UserCoinsService userCoinsService) {
        this.userCoinsService = userCoinsService;
    }

    @GetMapping
    public ResponseEntity<List<UserCoins>> getUsersCoins() {
        List<UserCoins> usersCoins = userCoinsService.getUsersCoins();
        return ResponseEntity.ok(usersCoins);
    }
}
