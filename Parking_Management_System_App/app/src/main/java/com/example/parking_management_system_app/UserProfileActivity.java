package com.example.parking_management_system_app;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

public class UserProfileActivity extends AppCompatActivity {

    private TextView usernameText, emailText, groupsText, userGreetingText;
    private Spinner vehicleSpinner, parkingSpinner, zoneSpinner;
    private Button saveButton, logoutButton, transactionButton, checkButton;

    String accessToken;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_profile);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

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

        populateUserData();

        saveButton.setOnClickListener(v -> {
            String selectedVehicle = vehicleSpinner.getSelectedItem().toString();
            String selectedParking = parkingSpinner.getSelectedItem().toString();
            String selectedZone = zoneSpinner.getSelectedItem().toString();

            saveData(selectedVehicle, selectedParking, selectedZone, accessToken);
        });

        logoutButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(UserProfileActivity.this, MainActivity.class);
                startActivity(intent);
                finish();
            }
        });


        transactionButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                populateUserData();
            }
        });

        checkButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(UserProfileActivity.this, CheckVehicleAccessActivity.class);
                intent.putExtra("username", usernameText.getText().toString().split(": ")[1]);
                intent.putExtra("accessToken", accessToken);
                startActivity(intent);
            }
        });

    }

    private void populateUserData() {
        Intent intent = getIntent();

        String firstName = intent.getStringExtra("firstName");
        String lastName = intent.getStringExtra("lastName");
        String username = intent.getStringExtra("username");
        String email = intent.getStringExtra("email");
        ArrayList<String> userGroups = intent.getStringArrayListExtra("userGroups");
        ArrayList<String> accessibleZones = intent.getStringArrayListExtra("accessibleZones");
        ArrayList<String> parkings = (ArrayList<String>) intent.getStringArrayListExtra("parkings");
        ArrayList<String> vehicles = (ArrayList<String>) intent.getStringArrayListExtra("vehicles");
        accessToken = intent.getStringExtra("accessToken");

        userGreetingText.setText("Hello " + firstName + " " + lastName + "!");
        usernameText.setText("Username: " + username);
        if (email == null || email.isEmpty()) {
            emailText.setText("Email: not found");
        } else {
            emailText.setText("Email: " + email);
        }

        String groupsTextString = "Groups: " + (userGroups != null && !userGroups.isEmpty() ? String.join(", ", userGroups) : "No groups");
        groupsText.setText(groupsTextString);


        StringBuilder parkingsText = new StringBuilder("Parkings:\n");
        if (parkings != null) {
            for (String parking : parkings) {
                parkingsText.append(parking + "\n");
            }
        }

        ArrayAdapter<String> vehicleAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, vehicles);
        vehicleAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        vehicleSpinner.setAdapter(vehicleAdapter);

        ArrayAdapter<String> parkingAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, parkings);
        parkingAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        parkingSpinner.setAdapter(parkingAdapter);

        ArrayAdapter<String> zoneAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, accessibleZones);
        zoneAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        zoneSpinner.setAdapter(zoneAdapter);


    }


    private void saveData(String vehicle, String parking, String zone, String token) {

        String[] vehicleNameSplit = vehicle.split(" ", 4);
        String vehicleNameOnly = vehicleNameSplit[0];

        Log.d("UserProfileActivity", "Vehicle: " + vehicleNameOnly);
        Log.d("UserProfileActivity", "Parking: " + parking);
        Log.d("UserProfileActivity", "Zone: " + zone);
        Log.d("UserProfileActivity", "Token: " + token);

        Map<String, String> transactionData = new HashMap<>();


        transactionData.put("vehicle", vehicleNameOnly);
        transactionData.put("parking", parking);
        transactionData.put("zone", zone);

        Retrofit retrofit = ApiClient.getClient(token);

        ApiService apiService = retrofit.create(ApiService.class);

        Call<Void> call = apiService.addTransaction(transactionData);
        call.enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                if (response.isSuccessful()) {
                    Log.d("UserProfileActivity", "Transaction successfully submitted.");
                    Toast.makeText(UserProfileActivity.this, "Transaction successfully submitted.", Toast.LENGTH_SHORT).show();
                } else {
                    Log.d("UserProfileActivity", "Failed to submit transaction.");
                    Toast.makeText(UserProfileActivity.this, "Failed to submit transaction", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Log.d("UserProfileActivity", "Error: " + t.getMessage());
                Toast.makeText(UserProfileActivity.this, " Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}

