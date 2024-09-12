import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from localization.Trilateration import perform_trilateration
from visualization.Visualization import visualize_estimated_position

# Mock detected devices
mock_detected_devices = [
    {"mac_address": "CA:02:32:D2:A1:83", "rssi": -55},
    {"mac_address": "CD:79:35:3F:C3:8B", "rssi": -60},
    {"mac_address": "D4:50:FE:62:52:77", "rssi": -55},
    {"mac_address": "D6:CA:74:F4:6F:BB", "rssi": -40}
]

# Path to detected devices JSON file
detected_devices_file = 'src/data/detected_devices.json'

# Clear the contents of detected_devices.json
with open(detected_devices_file, 'w') as f:
    json.dump([], f)  # Empty the file by writing an empty list

# Write the mock data to detected_devices.json
with open(detected_devices_file, 'w') as f:
    json.dump(mock_detected_devices, f, indent=4)

# Perform trilateration using the mock detected devices
result = perform_trilateration('src/data/beacon_coordinates.json', detected_devices_file)

# Check if trilateration was successful
if result:
    avg_longitude, avg_latitude = result
    print(f"Estimated coordinates: {avg_longitude}, {avg_latitude}")

    # Visualize the estimated position
    visualize_estimated_position(avg_longitude, avg_latitude)
else:
    print("Trilateration failed.")
