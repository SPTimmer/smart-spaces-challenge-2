# BluetoothScan.py is responsible for scanning Bluetooth devices using the Bleak library, which is installed in the
# virtual python environment (venv, using pip install bleak). Before it scans for bluetooth devices, it first clears
# all data of stored bluetooth devices, ensuring that the data used by the algorithms is always from the most recent
# scan.

import asyncio
from bleak import BleakScanner
from BluetoothDevice import BluetoothDevice

BluetoothDevice.clear_devices()


async def scan_ble_devices():
    devices = await BleakScanner.discover()
    print("Starting the scan...")

    for device in devices:
        mac_address = device.address
        rssi = device.rssi

        BluetoothDevice(mac_address, rssi)

    print("Scan complete.")
    BluetoothDevice.print_all_devices()


if __name__ == "__main__":
    asyncio.run(scan_ble_devices())
