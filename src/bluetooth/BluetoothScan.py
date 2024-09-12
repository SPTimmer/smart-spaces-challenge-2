import json
import asyncio
from bleak import BleakScanner

DETECTED_DEVICES_PATH = 'src/data/detected_devices.json'


async def scan_ble_devices():
    devices = await BleakScanner.discover()
    print("Starting the scan...")

    detected_devices = []

    # Clear previous devices in the detected_devices.json file before scan
    with open(DETECTED_DEVICES_PATH, 'w') as f:
        json.dump([], f)  # Reset detected_devices.json

    for device in devices:
        mac_address = device.address
        rssi = device.rssi
        detected_devices.append({'mac_address': mac_address, 'rssi': rssi})

    print(f"Scan complete, found {len(devices)} devices")

    # Save detected devices to JSON
    with open(DETECTED_DEVICES_PATH, 'w') as f:
        json.dump(detected_devices, f)

    print(f"Detected devices written to {DETECTED_DEVICES_PATH}")


# Run BLE scan and store detected devices in JSON
asyncio.run(scan_ble_devices())
