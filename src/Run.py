import asyncio
import time

from bluetooth.BluetoothScan import BluetoothScan
from data.knownbeacons import KNOWN_BEACONS_ZILVERLING
from concurrent.futures import ThreadPoolExecutor
from localization.Trilateration import perform_trilateration
from visualization.Visualization import visualize_estimated_position
from typing import Any, Dict, List


def filter_known_beacons(devices: Dict[str, tuple]) -> List[Dict[str, Any]]:
    filtered_beacons = []
    for key, rssi in devices.items():
        for known_beacon in KNOWN_BEACONS_ZILVERLING:
            if key == known_beacon.get("mac"):
                filtered_beacons.append({"mac": key,
                                         "rssi": rssi,
                                         "lon": known_beacon.get("longitude"),
                                         "lat": known_beacon.get("latitude")})

                print(f"Beacon MAC: {key}, RSSI: {rssi}, Room: {known_beacon.get('room')}")
    return filtered_beacons


# Create a global thread pool executor to run tasks
executor = ThreadPoolExecutor()


def run_scan(loop):
    asyncio.set_event_loop(loop)
    scanner = BluetoothScan()
    return loop.run_until_complete(scanner.start_scan())


# Create a global thread pool executor to run tasks
executor = ThreadPoolExecutor()


def run_scan(loop):
    asyncio.set_event_loop(loop)
    scanner = BluetoothScan()
    return loop.run_until_complete(scanner.start_scan())


def main_loop():
    loop = asyncio.get_event_loop()

    while True:
        try:
            # Submit scan task to the thread pool executor
            future = executor.submit(run_scan, loop)
            detected_devices = future.result()

            filtered_beacons = filter_known_beacons(detected_devices)  # Filter the known beacons
            if len(filtered_beacons) >= 3:
                estimated_position = perform_trilateration(filtered_beacons)
                if estimated_position:
                    visualize_estimated_position(estimated_position[0], estimated_position[1])
                    print("Pausing for 5, you can move for this time before the scan starts...")
                    time.sleep(5)
            else:
                print(
                    f"Less than 3 known beacons detected. Skipping trilateration. (Found {len(filtered_beacons)} known beacons)")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main_loop()
