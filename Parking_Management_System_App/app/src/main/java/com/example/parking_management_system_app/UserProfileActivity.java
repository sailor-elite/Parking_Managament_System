package com.example.parking_management_system_app;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

public class UserProfileActivity extends AppCompatActivity {

    private TextView usernameText, emailText, groupsText, userGreetingText;
    private Spinner vehicleSpinner, parkingSpinner, zoneSpinner;
    private Button saveButton, logoutButton, transactionButton, checkButton, vehiclesButton;
    private String username;
    private Serializable vehicles;
    private List<Vehicle> vehiclesList;
    private String accessToken;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_profile);
        setupWindowInsets();

        initializeViews();
        populateUserData();

        setListeners();
    }

    private void setupWindowInsets() {
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    private void initializeViews() {
        userGreetingText = findViewById(R.id.userGreeting);
        usernameText = findViewById(R.id.usernameText);
        emailText = findViewById(R.id.emailText);
        groupsText = findViewById(R.id.groupsText);
        vehicleSpinner = findViewById(R.id.vehicleSpinner);
        parkingSpinner = findViewById(R.id.parkingSpinner);
        zoneSpinner = findViewById(R.id.zoneSpinner);
        saveButton = findViewById(R.id.addTransactionButton);
        logoutButton = findViewById(R.id.logoutButton);
        transactionButton = findViewById(R.id.transactionButton);
        checkButton = findViewById(R.id.checkButton);
        vehiclesButton = findViewById(R.id.vehiclesButton);
    }

    private void setListeners() {
        saveButton.setOnClickListener(v -> {
            Vehicle selectedVehicle = (Vehicle) vehicleSpinner.getSelectedItem();
            String selectedParking = parkingSpinner.getSelectedItem().toString();
            String selectedZone = zoneSpinner.getSelectedItem().toString();
            saveData(selectedVehicle, selectedParking, selectedZone, accessToken);
        });

        logoutButton.setOnClickListener(v -> {
            Intent intent = new Intent(UserProfileActivity.this, MainActivity.class);
            startActivity(intent);
            finish();
        });

        transactionButton.setOnClickListener(v -> populateUserData());

        checkButton.setOnClickListener(v -> {
            Intent intent = new Intent(UserProfileActivity.this, CheckVehicleAccessActivity.class);
            intent.putExtra("username", usernameText.getText().toString().split(": ")[1]);
            intent.putExtra("accessToken", accessToken);
            intent.putExtra("vehicles", new Gson().toJson(vehiclesList));
            startActivity(intent);
        });

        vehiclesButton.setOnClickListener(v -> {
            Intent intent = new Intent(UserProfileActivity.this, VehiclesList.class);
            intent.putExtra("vehicles", new Gson().toJson(vehiclesList));
            intent.putExtra("username", usernameText.getText().toString().split(": ")[1]);
            intent.putExtra("accessToken", accessToken);
            startActivity(intent);
        });
    }

    private void populateUserData() {
        Intent intent = getIntent();

        String firstName = intent.getStringExtra("firstName");
        String lastName = intent.getStringExtra("lastName");
        username = intent.getStringExtra("username");
        String email = intent.getStringExtra("email");
        ArrayList<String> userGroups = intent.getStringArrayListExtra("userGroups");
        ArrayList<String> accessibleZones = intent.getStringArrayListExtra("accessibleZones");
        ArrayList<String> parkings = intent.getStringArrayListExtra("parkings");

        String vehiclesJson = intent.getStringExtra("vehicles");
        Gson gson = new Gson();
        vehiclesList = gson.fromJson(vehiclesJson, new TypeToken<List<Vehicle>>() {
        }.getType());

        Log.wtf("UserProfileActivity", vehiclesJson);

        accessToken = intent.getStringExtra("accessToken");

        setUserInfo(firstName, lastName, email);
        setUserGroups(userGroups);
        setParkings(parkings);
        setupSpinners(parkings, accessibleZones);
    }

    private void setUserInfo(String firstName, String lastName, String email) {
        userGreetingText.setText("Hello " + firstName + " " + lastName + "!");
        usernameText.setText("Username: " + username);
        emailText.setText(email == null || email.isEmpty() ? "Email: not found" : "Email: " + email);
    }

    private void setUserGroups(ArrayList<String> userGroups) {
        String groupsTextString = "Groups: " + (userGroups != null && !userGroups.isEmpty() ? String.join(", ", userGroups) : "No groups");
        groupsText.setText(groupsTextString);
    }

    private void setParkings(ArrayList<String> parkings) {
        StringBuilder parkingsText = new StringBuilder("Parkings:\n");
        if (parkings != null) {
            for (String parking : parkings) {
                parkingsText.append(parking).append("\n");
            }
        }
    }

    private void setupSpinners(ArrayList<String> parkings, ArrayList<String> accessibleZones) {
        VehicleAdapter vehicleAdapter = new VehicleAdapter(this, vehiclesList);
        vehicleSpinner.setAdapter(vehicleAdapter);

        setupSpinner(parkingSpinner, parkings);
        setupSpinner(zoneSpinner, accessibleZones);
    }

    private void setupSpinner(Spinner spinner, List<String> data) {
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, data);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);
    }

    private void saveData(Vehicle vehicle, String parking, String zone, String token) {
        String vehicleLicensePlate = vehicle.getLicensePlate();

        Log.wtf("UserProfileActivity", "vehicle valid: " + vehicleLicensePlate);
        Log.d("UserProfileActivity", "Parking: " + parking);
        Log.d("UserProfileActivity", "Zone: " + zone);

        Map<String, String> transactionData = new HashMap<>();
        transactionData.put("vehicle", vehicleLicensePlate);
        transactionData.put("parking", parking);
        transactionData.put("zone", zone);

        sendTransactionToServer(transactionData, token);
    }
    
    private void sendTransactionToServer(Map<String, String> transactionData, String token) {
        Retrofit retrofit = ApiClient.getClient(token);
        ApiService apiService = retrofit.create(ApiService.class);
        Call<Void> call = apiService.addTransaction(transactionData);
        call.enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                handleTransactionResponse(response);
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                handleTransactionFailure(t);
            }
        });
    }

    private void handleTransactionResponse(Response<Void> response) {
        if (response.isSuccessful()) {
            Toast.makeText(UserProfileActivity.this, "Transaction successfully submitted.", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(UserProfileActivity.this, "Failed to submit transaction", Toast.LENGTH_SHORT).show();
        }
    }

    private void handleTransactionFailure(Throwable t) {
        Log.d("UserProfileActivity", "Error: " + t.getMessage());
        Toast.makeText(UserProfileActivity.this, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
    }
}
