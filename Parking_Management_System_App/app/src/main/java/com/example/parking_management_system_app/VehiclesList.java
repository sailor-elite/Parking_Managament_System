package com.example.parking_management_system_app;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.util.List;

public class VehiclesList extends AppCompatActivity {

    private Button logoutBackButton, transactionBackButton, checkVehicleAccessButton;
    private ListView vehiclesListView;
    private TextView usernameGreeting;

    private String username;
    private List<Vehicle> vehiclesList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_vehicles_list);

        initializeViews();

        retrieveDataFromIntent();

        setupVehicleListView();

        setupButtonListeners();
    }

    private void initializeViews() {
        usernameGreeting = findViewById(R.id.usernameGreeting);
        transactionBackButton = findViewById(R.id.transactionButton2);
        logoutBackButton = findViewById(R.id.logoutButton3);
        checkVehicleAccessButton = findViewById(R.id.checkButton2);
        vehiclesListView = findViewById(R.id.vehiclesListView);
    }

    private void retrieveDataFromIntent() {
        Intent intent = getIntent();
        username = intent.getStringExtra("username");
        usernameGreeting.setText(username + ", here's a list of Your vehicles:");

        String vehiclesJson = intent.getStringExtra("vehicles");
        vehiclesList = new Gson().fromJson(vehiclesJson, new TypeToken<List<Vehicle>>() {
        }.getType());
    }

    private void setupVehicleListView() {
        VehicleAdapter vehicleAdapter = new VehicleAdapter(this, vehiclesList);
        vehiclesListView.setAdapter(vehicleAdapter);
    }

    private void setupButtonListeners() {
        transactionBackButton.setOnClickListener(v -> finish());

        logoutBackButton.setOnClickListener(v -> navigateToMainActivity());

        checkVehicleAccessButton.setOnClickListener(v -> navigateToCheckVehicleAccessActivity());
    }

    private void navigateToMainActivity() {
        Intent intent = new Intent(VehiclesList.this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    private void navigateToCheckVehicleAccessActivity() {
        Intent intent = new Intent(VehiclesList.this, CheckVehicleAccessActivity.class);
        intent.putExtra("username", username);
        intent.putExtra("accessToken", getIntent().getStringExtra("accessToken"));
        startActivity(intent);
    }
}
