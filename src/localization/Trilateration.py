# The Trilateration.py is used to localize the user using the trilateration method. The math used in the python is
# based of documentation of Alan Zucconi (https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/#part1)
# More on this math above the function calculate_distance().

# Step-wise explanation:
# Step 1:   Load known beacon coordinates from beacon_coordinates.json. These are the beacons of which we know the
#           location as they were given on Canvas. It reads JSON and returns a python list of dictionaries where each
#           dictionary contains the MAC-address, longitude and latitude of a beacon.
# Step 2:   Convert RSSI to distance using (calculate_distance). For details about the calculation read above function.
# Step 3:   Get detected devices from BluetoothDevice.py. These devices include their MAC-address and RSSI.
# Step 4:   Match detected devices with known beacons and calculate distances. We need at least 3 detected devices to
#           be listed in beacon_coordinates.json, otherwise we will not be able to estimate the user's location.
#           This is where we create a list of detected devices that have known coordinates, and the distance from the
#           user to these known coordinates, calculated using the detected RSSI.
# Step 5:   Perform trilateration: Using Alan Zucconi's method, we can perform trilateration by simplifying the
#           intersection of circles, making solving x for y linearly. Outputs the estimated user location.

import math
import json
from bluetooth import BluetoothDevice


def load_beacon_coordinates(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


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


def trilaterate(beacon1, beacon2, beacon3):
    x1, y1 = beacon1['longitude'], beacon1['latitude']
    x2, y2 = beacon2['longitude'], beacon2['latitude']
    x3, y3 = beacon3['longitude'], beacon3['latitude']

    r1 = beacon1['distance']
    r2 = beacon2['distance']
    r3 = beacon3['distance']

    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2

    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)

    return (x, y)


def perform_trilateration(beacon_file):
    beacons_data = load_beacon_coordinates(beacon_file)
    detected_known_beacons = []

    detected_devices = BluetoothDevice.get_devices()

    for device in detected_devices:
        for beacon in beacons_data:
            if device.mac_address == beacon['mac_address']:
                distance = calculate_distance(device.rssi)
                detected_known_beacons.append({
                    'mac_address': device.mac_address,
                    'longitude': beacon['longitude'],
                    'latitude': beacon['latitude'],
                    'distance': distance
                })

    if len(detected_known_beacons) >= 3:
        beacon1 = detected_known_beacons[0]
        beacon2 = detected_known_beacons[1]
        beacon3 = detected_known_beacons[2]

        position = trilaterate(beacon1, beacon2, beacon3)
        if position:
            print(f"Estimated Position: Longitude: {position[0]}, Latitude: {position[1]}")
        else:
            print("Trilateration failed.")
    else:
        print("Less than 3 known beacons detected. Skipping trilateration.")


perform_trilateration('src/data/beacon_coordinates.json')
