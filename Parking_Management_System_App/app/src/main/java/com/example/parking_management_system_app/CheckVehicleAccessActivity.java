package com.example.parking_management_system_app;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

public class CheckVehicleAccessActivity extends AppCompatActivity {

    private Button logoutBackButton, transactionBackButton, checkVehicleAccessButton;
    private Spinner zoneSpinner;
    private String username;
    private String accessToken;
    private EditText editTextUsernameVehicle;
    private Map<String, String> zoneMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_user);

        transactionBackButton = findViewById(R.id.transactionButton2);
        logoutBackButton = findViewById(R.id.logoutButton3);
        checkVehicleAccessButton = findViewById(R.id.checkVehicleAccessButton);
        zoneSpinner = findViewById(R.id.zoneSpinner);
        editTextUsernameVehicle = findViewById(R.id.editTextUsernameVehicle);


        accessToken = getIntent().getStringExtra("accessToken");

        zoneMap = new HashMap<>();
        zoneMap.put("Green Zone", "greenZone");
        zoneMap.put("Blue Zone", "blueZone");
        zoneMap.put("Red Zone", "redZone");

        ArrayList<String> zones = new ArrayList<>();
        zones.add("Green Zone");
        zones.add("Blue Zone");
        zones.add("Red Zone");

        ArrayAdapter<String> zoneAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, zones);
        zoneAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        zoneSpinner.setAdapter(zoneAdapter);

        transactionBackButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        logoutBackButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(CheckVehicleAccessActivity.this, MainActivity.class);
                startActivity(intent);
                finish();
            }
        });

        checkVehicleAccessButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                checkVehicleAccess();
            }
        });
    }

    private void checkVehicleAccess() {
        String selectedZone = zoneSpinner.getSelectedItem().toString();

        String username = editTextUsernameVehicle.getText().toString();

        if (username.isEmpty()) {
            Toast.makeText(this, "Please enter a username", Toast.LENGTH_SHORT).show();
            return;
        }
        String backendZone = zoneMap.get(selectedZone);

        Map<String, String> requestData = new HashMap<>();
        requestData.put("username", username);
        requestData.put("zone", backendZone);

        Log.d("CheckVehicleAccess", "Request data: username=" + username + ", zone=" + backendZone);


        Retrofit retrofit = ApiClient.getClient(accessToken);
        ApiService apiService = retrofit.create(ApiService.class);

        Call<Map<String, String>> call = apiService.checkVehicleAccess(requestData);
        call.enqueue(new Callback<Map<String, String>>() {
            @Override
            public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {
                if (response.isSuccessful()) {
                    String responseBody = response.body().toString();
                    Log.d("CheckVehicleAccess", "Response: " + responseBody);

                    if (response.body() != null) {
                        String message = response.body().get("message");
                        Toast.makeText(CheckVehicleAccessActivity.this, message, Toast.LENGTH_SHORT).show();
                        Log.d("CheckVehicleAccess", "Message: " + message);
                    }
                } else {
                    Log.d("CheckVehicleAccess", "Response error: " + response.code());
                    try {
                        String errorResponse = response.errorBody().string();
                        Log.d("CheckVehicleAccess", "Error body: " + errorResponse); 
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    Toast.makeText(CheckVehicleAccessActivity.this, "Access check failed", Toast.LENGTH_SHORT).show();
                }
                zoneSpinner.setSelection(0);
                editTextUsernameVehicle.setText("");
            }

            @Override
            public void onFailure(Call<Map<String, String>> call, Throwable t) {
                Toast.makeText(CheckVehicleAccessActivity.this, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                Log.d("CheckVehicleAccess", "Error: " + t.getMessage());
            }
        });

    }
}
