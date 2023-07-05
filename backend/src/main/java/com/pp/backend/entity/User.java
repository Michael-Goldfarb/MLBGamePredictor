package com.pp.backend.entity;

import com.fasterxml.jackson.annotation.JsonProperty;

public class User {
    @JsonProperty("email")
    private String email;
    @JsonProperty("name")
    private String name;
    @JsonProperty("phoneNumber")
    private String phoneNumber;
    @JsonProperty("age_or_older")
    private String ageOrOlder;
    @JsonProperty("user_status")
    private String userStatus;

    public User() {
    }

    public User(String email, String name, String phoneNumber, String ageOrOlder, String userStatus) {
        this.email = email;
        this.name = name;
        this.phoneNumber = phoneNumber;
        this.ageOrOlder = ageOrOlder;
        this.userStatus = userStatus;
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

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getAgeOrOlder() {
        return ageOrOlder;
    }

    public void setAgeOrOlder(String ageOrOlder) {
        this.ageOrOlder = ageOrOlder;
    }

    public String getUserStatus() {
        return userStatus;
    }

    public void setUserStatus(String userStatus) {
        this.userStatus = userStatus;
    }
}
