import json
import math
from typing import List, Dict, Tuple


# The python program used for the trilateration algorithm.
# It works as following:
#   Step 1) Loading the known coordinates and the detected devices
#   Step 2) Calculating the distances using the RSSI of the detected devices
#   Step 3) Performing the trilateration algorithm (as described by Alan Zucconi)
#   Step 4) Return the estimated longitude and latitude to Run.py

# Function for loading beacon_coordinates.json. This lists the coordinates given on canvas.
def load_beacon_coordinates(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Function for loading the files written in detected_devices.json by BluetoothScan.py
def load_detected_devices(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Function for calculating the distance (in meters) using the RSSI (dBm) of a beacon
def calculate_distance(rssi):
    # RSSI to distance conversion logic goes here
    return 10 ** ((-60 - rssi) / (10 * 3))


# Convert latitude/longitude to Cartesian coordinates
def latlon_to_cartesian(lat, lon):
    R = 6371000  # Earth radius in meters
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    x = R * lon_rad * math.cos(lat_rad)
    y = R * lat_rad
    return x, y


# Convert Cartesian coordinates back to latitude/longitude
def cartesian_to_latlon(x, y):
    R = 6371000  # Earth radius in meters
    lat_rad = y / R
    lon_rad = x / (R * math.cos(lat_rad))
    lat = math.degrees(lat_rad)
    lon = math.degrees(lon_rad)
    return lat, lon


# Alan Zucconi's trilateration formula
def calculate_trilateration(x1, y1, d1, x2, y2, d2, x3, y3, d3):
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = d1 ** 2 - d2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = d2 ** 2 - d3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2

    # Adding a small epsilon to avoid division by zero
    epsilon = 1e-6

    if abs(E) < epsilon or abs(B) < epsilon:
        raise ValueError("Division by zero detected in trilateration calculation.")

    x = (C - F * B / E) / (A - D * B / E)
    y = (C - A * x) / B

    return x, y


def perform_trilateration(filtered_beacons: List[dict]) -> Tuple[float, float]:
    if len(filtered_beacons) >= 3:
        # Sort beacons by RSSI (higher RSSI is closer to 0, meaning stronger signal)
        sorted_beacons = sorted(filtered_beacons, key=lambda b: b["rssi"], reverse=True)

        # Select the three strongest beacons
        strongest_beacons = sorted_beacons[:3]

        rssis = " ".join([str(beacon["rssi"]) for beacon in filtered_beacons])
        print("all: ")
        print(rssis)

        strongest_rssis = " ".join([str(beacon["rssi"]) for beacon in strongest_beacons])
        print("strongest: ")
        print(strongest_rssis)

        # Perform trilateration using the three strongest beacons
        lat1, lon1, d1 = strongest_beacons[0]["lat"], strongest_beacons[0]["lon"], calculate_distance(strongest_beacons[0]["rssi"])
        lat2, lon2, d2 = strongest_beacons[1]["lat"], strongest_beacons[1]["lon"], calculate_distance(strongest_beacons[1]["rssi"])
        lat3, lon3, d3 = strongest_beacons[2]["lat"], strongest_beacons[2]["lon"], calculate_distance(strongest_beacons[2]["rssi"])

        x1, y1 = latlon_to_cartesian(lat1, lon1)
        x2, y2 = latlon_to_cartesian(lat2, lon2)
        x3, y3 = latlon_to_cartesian(lat3, lon3)

        x_strong, y_strong = calculate_trilateration(x1, y1, d1, x2, y2, d2, x3, y3, d3)

        lat_strong, lon_strong = cartesian_to_latlon(x_strong, y_strong)
        print(f"First trilateration result (strongest): {lat_strong}, {lon_strong}")

        # Check if there are at least 6 beacons, then use 4th, 5th, and 6th strongest beacons
        if len(filtered_beacons) >= 6:
            second_strongest_beacons = sorted_beacons[3:6]
            second_rssis = " ".join([str(beacon["rssi"]) for beacon in second_strongest_beacons])
            print("second strongest: ")
            print(second_rssis)

            lat4, lon4, d4 = second_strongest_beacons[0]["lat"], second_strongest_beacons[0]["lon"], calculate_distance(second_strongest_beacons[0]["rssi"])
            lat5, lon5, d5 = second_strongest_beacons[1]["lat"], second_strongest_beacons[1]["lon"], calculate_distance(second_strongest_beacons[1]["rssi"])
            lat6, lon6, d6 = second_strongest_beacons[2]["lat"], second_strongest_beacons[2]["lon"], calculate_distance(second_strongest_beacons[2]["rssi"])

            x4, y4 = latlon_to_cartesian(lat4, lon4)
            x5, y5 = latlon_to_cartesian(lat5, lon5)
            x6, y6 = latlon_to_cartesian(lat6, lon6)

            x_second, y_second = calculate_trilateration(x4, y4, d4, x5, y5, d5, x6, y6, d6)

            lat_second, lon_second = cartesian_to_latlon(x_second, y_second)
            print(f"Second trilateration result (second strongest): {lat_second}, {lon_second}")

            # Weigh the first trilateration result 2x, and the second 1x, and take the average
            final_lat = (2 * lat_strong + lat_second) / 3
            final_lon = (2 * lon_strong + lon_second) / 3

            print(f"Final weighted trilateration result: {final_lat}, {final_lon}")
            return final_lat, final_lon
        else:
            # If there are less than 6 beacons, return the result from the three strongest
            print(f"Not enough beacons for second calculation. Returning strongest trilateration result.")
            return lat_strong, lon_strong
    else:
        print(f"Less than 3 known beacons detected. Skipping trilateration. (Found {len(filtered_beacons)} known beacons)")
        return None
