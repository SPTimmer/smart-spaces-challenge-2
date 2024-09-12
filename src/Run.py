import time
import subprocess
from localization.Trilateration import perform_trilateration
from visualization.Visualization import visualize_estimated_position


def run_bluetooth_scan():
    print("Running Bluetooth scan...")
    subprocess.run(['python', 'src/bluetooth/BluetoothScan.py'], check=True)
    print("Bluetooth scan completed.")


def run_trilateration():
    print("Running trilateration...")
    estimated_position = perform_trilateration('src/data/beacon_coordinates.json')
    if estimated_position:
        print(f"Trilateration successful: Estimated Position = {estimated_position}")
        return estimated_position
    else:
        print("Trilateration skipped. Less than 3 beacons detected.")
        return None


def visualize_position(estimated_position):
    if estimated_position:
        lon, lat = estimated_position
        print(f"Visualizing position: Longitude = {lon}, Latitude = {lat}")
        visualize_estimated_position(lon, lat)
    else:
        print("No valid position to visualize.")


def main_loop():
    try:
        while True:
            # Step 1: Run Bluetooth scan
            run_bluetooth_scan()

            # Step 2: Run Trilateration to estimate position
            estimated_position = run_trilateration()

            # Step 3: Visualize the estimated position
            visualize_position(estimated_position)

            # Wait for a few seconds before the next iteration
            time.sleep(5)  # Adjust the sleep duration as needed

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")


if __name__ == '__main__':
    main_loop()
