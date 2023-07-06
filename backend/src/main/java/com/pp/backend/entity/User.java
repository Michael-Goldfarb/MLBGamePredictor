package com.pp.backend.entity;
import com.fasterxml.jackson.annotation.JsonProperty;

public class User {
    @JsonProperty("email")
    private String email;
    @JsonProperty("name")
    private String name;

    public User() {
    }

    public User(String email, String name) {
        this.email = email;
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
