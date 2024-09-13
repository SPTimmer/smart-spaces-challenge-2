import asyncio
from bleak import BleakScanner


class BluetoothScan:
    def __init__(self):
        self.devices = {}

    async def start_scan(self):
        scanner = BleakScanner()
        scanner.register_detection_callback(self.detection_callback)

        # Clear the devices dictionary before each scan
        self.devices = {}

        print("scan started")
        await scanner.start()
        await asyncio.sleep(5)  # Adjust scan duration if necessary
        await scanner.stop()
        print(f"scan completed, found {len(self.devices)} devices")
        return self.devices

    def detection_callback(self, device, advertisement_data):
        self.devices[device.address] = device.rssi
        print(f"Detected device: {device.address} with RSSI: {device.rssi}")

    def sync_scan(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.start_scan())

