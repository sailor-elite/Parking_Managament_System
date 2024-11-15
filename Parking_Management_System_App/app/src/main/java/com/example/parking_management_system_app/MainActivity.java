package com.example.parking_management_system_app;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private EditText editTextUsername;
    private EditText editTextPassword;
    private Button buttonLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });


        editTextUsername = findViewById(R.id.editTextUsername);
        editTextPassword = findViewById(R.id.editTextPassword);
        buttonLogin = findViewById(R.id.buttonLogin);


        buttonLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String username = editTextUsername.getText().toString();
                String password = editTextPassword.getText().toString();

                if (username.isEmpty() || password.isEmpty()) {
                    Toast.makeText(MainActivity.this, "All fields must be filled!", Toast.LENGTH_SHORT).show();
                } else {
                    loginUser(username, password);
                }
            }
        });

    }

    public void loginUser(String username, String password) {
        AuthService authService = RetrofitClient.getClient().create(AuthService.class);
        Call<TokenResponse> call = authService.loginUser(new LoginRequest(username, password));

        call.enqueue(new Callback<TokenResponse>() {
            @Override
            public void onResponse(Call<TokenResponse> call, Response<TokenResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    TokenResponse tokenResponse = response.body();

                    String accessToken = tokenResponse.getAccess();
                    String username = tokenResponse.getUsername();
                    String email = tokenResponse.getEmail();
                    String firstName = tokenResponse.getFirstName();
                    String lastName = tokenResponse.getLastName();
                    List<String> vehicles = tokenResponse.getVehicles();
                    List<String> userGroups = tokenResponse.getUserGroups();
                    List<String> accessibleZones = tokenResponse.getAccessibleZones();
                    List<String> parkings = tokenResponse.getParkings();


                    Log.d("LoginResponse", "Username: " + username);
                    Log.d("LoginResponse", "Email: " + email);
                    Log.d("LoginResponse", "Vehicles: " + vehicles);
                    Log.d("LoginResponse", "userGroups: " + userGroups);
                    Log.d("LoginResponse", "firstName: " + firstName);
                    Log.d("LoginResponse", "lastName: " + lastName);
                    Log.d("LoginResponse", "accessibleZones: " + accessibleZones);
                    Log.d("LoginResponse", "parkings: " + parkings);

                    Intent intent = new Intent(MainActivity.this, UserProfileActivity.class);
                    intent.putExtra("firstName", firstName);
                    intent.putExtra("lastName", lastName);
                    intent.putExtra("username", username);
                    intent.putExtra("email", email);
                    intent.putExtra("vehicles", new ArrayList<>(vehicles));
                    intent.putExtra("userGroups", new ArrayList<>(userGroups));
                    intent.putExtra("parkings", new ArrayList<>(parkings));
                    intent.putExtra("accessibleZones", new ArrayList<>(accessibleZones));
                    intent.putExtra("accessToken", accessToken);
                    startActivity(intent);
                } else {
                    Toast.makeText(MainActivity.this, "Login failed.", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<TokenResponse> call, Throwable t) {
                Toast.makeText(MainActivity.this, "Network error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                Log.e("LoginError", t.getMessage());
            }
        });
    }

}