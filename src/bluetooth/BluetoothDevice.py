# BluetoothDevice.py defines a class to represent each detected bluetooth device.
# For every device the MAC-address and RSSI value are stored.

class BluetoothDevice:

    devices = []

    def __init__(self, mac_address, rssi):
        self.mac_address = mac_address
        self.rssi = rssi
        BluetoothDevice.devices.append(self)

    @classmethod
    def clear_devices(cls):
        cls.devices = []

    @classmethod
    def print_all_devices(cls):
        for device in cls.devices:
            print(f"MAC: {device.mac_address}, RSSI: {device.rssi}")

    @classmethod
    def get_devices(cls):
        return cls.devices
