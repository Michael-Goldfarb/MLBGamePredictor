
package com.pp.backend.entity;

import com.fasterxml.jackson.annotation.JsonProperty;

public class UserCoins {
    @JsonProperty("email")
    private String email;
    @JsonProperty("coin_balance")
    private int coin_balance;


    public UserCoins() {
    }

    public UserCoins(String email, int coin_balance) {
        this.email = email;
        this.coin_balance = coin_balance;

    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getCoin_balance() {
        return coin_balance;
    }
    
    public void setCoin_balance(int coin_balance){
        this.coin_balance = coin_balance;
    }
}
