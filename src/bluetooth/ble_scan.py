import asyncio
from bleak import BleakScanner


async def scan_ble_devices():
    devices = await BleakScanner.discover()
    print("Starting the scan..")
    for device in devices:
        print(f"Device: {device.address}, RSSI: {device.rssi}")
    print("Scan complete.")


asyncio.run(scan_ble_devices())
