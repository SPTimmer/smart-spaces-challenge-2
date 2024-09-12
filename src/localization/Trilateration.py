import json
import math


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

    x = (C - F * B / E) / (A - D * B / E)
    y = (C - A * x) / B
    return x, y


def perform_trilateration(beacon_file, detected_file):
    beacons = load_beacon_coordinates(beacon_file)
    detected_devices = load_detected_devices(detected_file)

    matched_beacons = []

    for device in detected_devices:
        for beacon in beacons:
            if device['mac_address'] == beacon['mac_address']:
                matched_beacons.append({
                    'latitude': beacon['latitude'],
                    'longitude': beacon['longitude'],
                    'distance': calculate_distance(device['rssi'])
                })

    if len(matched_beacons) >= 3:
        matched_beacons = matched_beacons[:3]
        lat1, lon1, d1 = matched_beacons[0].values()
        lat2, lon2, d2 = matched_beacons[1].values()
        lat3, lon3, d3 = matched_beacons[2].values()

        x1, y1 = latlon_to_cartesian(lat1, lon1)
        x2, y2 = latlon_to_cartesian(lat2, lon2)
        x3, y3 = latlon_to_cartesian(lat3, lon3)

        x, y = calculate_trilateration(x1, y1, d1, x2, y2, d2, x3, y3, d3)

        lat, lon = cartesian_to_latlon(x, y)
        print(f"Trilateration result: {lat}, {lon}")
        return lat, lon
    else:
        print(
            f"Less than 3 known beacons detected. Skipping trilateration. (Found {len(matched_beacons)} known beacons)")
        return None
