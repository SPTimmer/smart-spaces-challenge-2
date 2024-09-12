# The Trilateration.py is used to localize the user using the trilateration method. The math used in the python is
# based of documentation of Alan Zucconi (https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/#part1)
# More on this math above the function calculate_distance().

# Step-wise explanation:
# Step 1:   Load known beacon coordinates from beacon_coordinates.json. These are the beacons of which we know the
#           location as they were given on Canvas. It reads JSON and returns a python list of dictionaries where each
#           dictionary contains the MAC-address, longitude and latitude of a beacon.
# Step 2:   Convert RSSI to distance using (calculate_distance). For details about the calculation read above function.
# Step 3:   Get detected devices from detected_devices.json. These devices include their MAC-address and RSSI.
# Step 4:   Match detected devices with known beacons and calculate distances. We need at least 3 detected devices to
#           be listed in beacon_coordinates.json, otherwise we will not be able to estimate the user's location.
#           This is where we create a list of detected devices that have known coordinates, and the distance from the
#           user to these known coordinates, calculated using the detected RSSI.
# Step 5:   Perform trilateration: Using Alan Zucconi's method, we can perform trilateration by simplifying the
#           intersection of circles, making solving x for y linearly. Outputs the estimated user location.

import math
import json

R = 6371000  # Radius of the Earth in meters, used because of longitude/latitude


# Longitude and latitude are in degrees, whereas the distance is calculated in meters. That is why we convert them
# to a cartesian space :
# https://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
def latlon_to_cartesian(lat, lon):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    x = R * lon_rad * math.cos(lat_rad)
    y = R * lat_rad
    return x, y


def cartesian_to_latlon(x, y):
    lat_rad = y / R
    lon_rad = x / (R * math.cos(lat_rad))
    lat = math.degrees(lat_rad)
    lon = math.degrees(lon_rad)
    return lat, lon


def load_beacon_coordinates(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def load_detected_devices(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if len(data) == 0:
                print("No devices found in detected_devices.json.")
            return data
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return []


# Explanation of the math used for trilateration:
# PARAMETERS:   Measured RSSI
#               A: The reference RSSI value at 1 meter. This represents the signal strength dBm when the device is
#                  exactly 1 meter away from the beacon. As we can not measure this exactly, we use value -50, as this
#                  is a very common reference RSSI (Bluetooth typically has -50 dBm)
#               n: The path loss exponent, according to Alan Zucconi this is usually between 2 and 4, so we use 2.0
# CALCULATIONS: (A-rssi) computes the difference between the reference RSSI and the current measured RSSI, the larger
#               the difference, the farther away the device is.
#               (10 * n) accounts for the  noise in the indoor space.
def calculate_distance(rssi, A=-50, n=2.0):
    return 10 ** ((A - rssi) / (10 * n))


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


# Note that the trilateration will loop until there are < 3 detected beacons of which the coordinates are known.
# For example if there are 5 detected beacons with known location, the trilateration performs 3 times:
# Once for beacon 1,2,3; once for beacon 2,3,4 and once for beacon 3,4,5. It then takes the average coordinates.
# Perform trilateration and return estimated location
def perform_trilateration(beacon_data_file, detected_devices_file):
    beacons = load_beacon_coordinates(beacon_data_file)
    detected_devices = load_detected_devices(detected_devices_file)
    detected_known_beacons = []

    print(f"Devices in Trilateration process: {len(detected_devices)}")

    for device in detected_devices:
        device_mac_address = device['mac_address'].lower().strip()  # Normalize detected MAC address
        print(f"Checking detected device: {device_mac_address} with RSSI: {device['rssi']}")

        for beacon in beacons:
            beacon_mac_address = beacon['mac_address'].lower().strip()  # Normalize beacon MAC address

            if device_mac_address == beacon_mac_address:
                distance = calculate_distance(device['rssi'])
                x, y = latlon_to_cartesian(beacon['latitude'], beacon['longitude'])
                detected_known_beacons.append({'x': x, 'y': y, 'distance': distance})
                print(f"Matched beacon: {beacon_mac_address} at distance: {distance}")

    if len(detected_known_beacons) < 3:
        print(f"Less than 3 known beacons detected. Skipping trilateration. ({len(detected_known_beacons)} found)")
        return None

    estimated_positions = []
    while len(detected_known_beacons) >= 3:
        beacon_1, beacon_2, beacon_3 = detected_known_beacons[:3]
        x, y = calculate_trilateration(beacon_1['x'], beacon_1['y'], beacon_1['distance'],
                                       beacon_2['x'], beacon_2['y'], beacon_2['distance'],
                                       beacon_3['x'], beacon_3['y'], beacon_3['distance'])
        lat, lon = cartesian_to_latlon(x, y)
        estimated_positions.append((lon, lat))
        detected_known_beacons.pop(0)

    avg_lon = sum([pos[0] for pos in estimated_positions]) / len(estimated_positions)
    avg_lat = sum([pos[1] for pos in estimated_positions]) / len(estimated_positions)
    print(f"Final Estimated Position: Longitude: {avg_lon}, Latitude: {avg_lat}")
    return avg_lon, avg_lat


perform_trilateration('src/data/beacon_coordinates.json', 'src/data/detected_devices.json')
