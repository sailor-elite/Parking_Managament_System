package com.example.parking_management_system_app;

import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface ApiService {

    @POST("transactions/add/")
    Call<Void> addTransaction(@Body Map<String, String> transactionData);

    @POST("/vehicle_access/api/vehicle-access/")
    Call<Map<String, String>> checkVehicleAccess(@Body Map<String, String> requestData);
}