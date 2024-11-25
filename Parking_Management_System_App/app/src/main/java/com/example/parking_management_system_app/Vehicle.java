package com.example.parking_management_system_app;

import java.io.Serializable;

public class Vehicle implements Serializable {
    private String licensePlate;
    private String make;
    private String model;
    private String photo;

    public Vehicle(String licensePlate, String make, String model, String photo) {
        this.licensePlate = licensePlate;
        this.make = make;
        this.model = model;
        this.photo = photo;
    }

    public String getLicensePlate() {
        return licensePlate;
    }

    public String getMake() {
        return make;
    }

    public String getModel() {
        return model;
    }

    public String getPhoto() {
        return photo;
    }

    @Override
    public String toString() {
        return "Vehicle{" +
                "licensePlate='" + licensePlate + '\'' +
                ", make='" + make + '\'' +
                ", model='" + model + '\'' +
                ", vehiclePhotoUrl='" + photo + '\'' +
                '}';
    }

}
