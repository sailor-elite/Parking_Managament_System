package com.example.parking_management_system_app;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface AuthService {
    @POST("users/token/")
    Call<TokenResponse> loginUser(@Body LoginRequest loginRequest);
}
