package com.example.parking_management_system_app;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;

import java.util.List;

public class VehicleAdapter extends ArrayAdapter<Vehicle> {

    public VehicleAdapter(Context context, List<Vehicle> vehicles) {
        super(context, 0, vehicles);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        return createViewFromResource(position, convertView, parent, R.layout.vehicle_list_item);
    }

    @Override
    public View getDropDownView(int position, View convertView, ViewGroup parent) {
        return createViewFromResource(position, convertView, parent, R.layout.vehicle_list_item);
    }

    private View createViewFromResource(int position, View convertView, ViewGroup parent, int layoutResource) {
        Vehicle vehicle = getItem(position);

        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(layoutResource, parent, false);
        }

        ImageView vehicleImage = convertView.findViewById(R.id.vehicleImage);
        TextView licensePlateTextView = convertView.findViewById(R.id.vehicleLicensePlate);
        TextView makeModelTextView = convertView.findViewById(R.id.vehicleMakeModel);

        if (vehicle != null) {
            licensePlateTextView.setText(vehicle.getLicensePlate());
            makeModelTextView.setText(vehicle.getMake() + " " + vehicle.getModel());

            Glide.with(getContext())
                    .load(vehicle.getPhoto())
                    .placeholder(R.drawable.baseline_car_crash_24)
                    .error(R.drawable.baseline_car_crash_24)
                    .into(vehicleImage);
        }

        return convertView;
    }
}
