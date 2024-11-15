package com.example.parking_management_system_app;

import java.util.List;

public class TokenResponse {
    private String access;
    private String refresh;
    private int userId;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private List<String> vehicles;
    private List<String> userGroups;
    private List<String> accessibleZones;
    private List<String> parkings;

    public TokenResponse(String access, String refresh, int userId, String username, String email,
                         String firstName, String lastName, List<String> vehicles, List<String> userGroups,
                         List<String> accessibleZones, List<String> parkings) {
        this.access = access;
        this.refresh = refresh;
        this.userId = userId;
        this.username = username;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.vehicles = vehicles;
        this.userGroups = userGroups;
        this.accessibleZones = accessibleZones;
        this.parkings = parkings;
    }


    public String getAccess() {
        return access;
    }

    public void setAccess(String access) {
        this.access = access;
    }

    public String getRefresh() {
        return refresh;
    }

    public void setRefresh(String refresh) {
        this.refresh = refresh;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public List<String> getVehicles() {
        return vehicles;
    }

    public void setVehicles(List<String> vehicles) {
        this.vehicles = vehicles;
    }

    public List<String> getUserGroups() {
        return userGroups;
    }

    public void setUserGroups(List<String> userGroups) {
        this.userGroups = userGroups;
    }

    public List<String> getAccessibleZones() {
        return accessibleZones;
    }

    public void setAccessibleZones(List<String> accessibleZones) {
        this.accessibleZones = accessibleZones;
    }

    public List<String> getParkings() {
        return parkings;
    }

    public void setParkings(List<String> parkings) {
        this.parkings = parkings;
    }

}
