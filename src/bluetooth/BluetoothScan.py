import asyncio
from bleak import BleakScanner
from BluetoothDevice import BluetoothDevice

bluetooth_devices = {}


async def scan_bl_devices():
    devices = await BleakScanner.discover()
    print("Starting the scan..")

    for device in devices:
        mac_address = device.address
        rssi = device.rssi

        # If the device is already detected, update the RSSI value
        if mac_address in bluetooth_devices:
            bluetooth_devices[mac_address].update_rssi(rssi)
        else:
            # Create a new BluetoothDevice and store it
            new_device = BluetoothDevice(mac_address, rssi)
            bluetooth_devices[mac_address] = new_device

    print("Scan complete.")

    # Print all devices
    for device in bluetooth_devices.values():
        print(device)


# Main execution
if __name__ == "__main__":
    asyncio.run(scan_bl_devices())
