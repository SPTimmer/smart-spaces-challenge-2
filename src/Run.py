import subprocess
import os
from time import sleep
from localization.Trilateration import perform_trilateration
from visualization.Visualization import visualize_estimated_position


def run_bluetooth_scan():
    bluetooth_scan_path = os.path.join('src', 'bluetooth', 'BluetoothScan.py')
    subprocess.run(['python', bluetooth_scan_path], check=True, env=dict(os.environ, PYTHONPATH=os.path.join(os.getcwd(), 'src')))


def main_loop():
    while True:
        run_bluetooth_scan()
        estimated_position = perform_trilateration('src/data/beacon_coordinates.json', 'src/data/detected_devices.json')
        if estimated_position:
            visualize_estimated_position(*estimated_position)
        else:
            print("No valid position to visualize.")
        sleep(2)  # Run every 10 seconds (or adjust based on your needs)


if __name__ == '__main__':
    main_loop()
