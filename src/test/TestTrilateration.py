import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from bluetooth.BluetoothDevice import BluetoothDevice
from localization.Trilateration import perform_trilateration
from visualization.Visualization import visualize_estimated_position

mock_detected_devices = [
    BluetoothDevice(mac_address='C2:8F:DF:51:4E:AF', rssi=-65),
    BluetoothDevice(mac_address='CA:02:32:D2:A1:83', rssi=-45),
    BluetoothDevice(mac_address='DO:2A:B7:EC:6C:44', rssi=-60),
    BluetoothDevice(mac_address='DE:AF:F9:8E:93:1D', rssi=-50)
]

with patch('bluetooth.BluetoothDevice.BluetoothDevice.get_devices', return_value=mock_detected_devices):
    result = perform_trilateration('src/data/beacon_coordinates.json')

    if result:
        avg_longitude, avg_latitude = result
        print(f"Estimated coordinates: {avg_longitude}, {avg_latitude}")

        visualize_estimated_position(avg_longitude, avg_latitude)
    else:
        print("Trilateration failed.")
