import json
import asyncio
from bleak import BleakScanner

DETECTED_DEVICES_PATH = 'src/data/detected_devices.json'


# For the Bluetooth Scanner we use BleakScanner from the bleak library.
# It works as following:
#   Step 1) Clear all data from detected_devices.json
#   Step 2) Append all new (freshly) scanned beacons and their RSSI to detected_devices.json
#   Step 3) Save the .json, so that it can be used by other parts of the system.

async def scan_ble_devices():
    devices = await BleakScanner.discover()

    detected_devices = []

    with open(DETECTED_DEVICES_PATH, 'w') as f:
        json.dump([], f)

    for device in devices:
        mac_address = device.address
        rssi = device.rssi
        detected_devices.append({'mac_address': mac_address, 'rssi': rssi})

    print(f"Scan complete, found {len(devices)} devices")

    with open(DETECTED_DEVICES_PATH, 'w') as f:
        json.dump(detected_devices, f)


# Run BLE scan and store detected devices in JSON
asyncio.run(scan_ble_devices())
