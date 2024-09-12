class BluetoothDevice:
    devices = []  # Shared across all instances

    def __init__(self, mac_address, rssi):
        self.mac_address = mac_address
        self.rssi = rssi

    @classmethod
    def add_device(cls, mac_address, rssi):
        # Check if the device is already in the list
        for device in cls.devices:
            if device.mac_address == mac_address:
                print(f"Device {mac_address} already exists, updating RSSI.")
                device.rssi = rssi
                return
        # Otherwise, add new device
        print(f"Adding new device: {mac_address}, RSSI: {rssi}")
        cls.devices.append(BluetoothDevice(mac_address, rssi))  # Add new device

    @classmethod
    def get_devices(cls):
        print(f"Returning {len(cls.devices)} stored devices.")
        return cls.devices

    @classmethod
    def clear_devices(cls):
        print("Clearing devices...")
        cls.devices = []

    @classmethod
    def print_devices(cls):
        print("Devices currently stored:")
        for device in cls.devices:
            print(f"MAC: {device.mac_address}, RSSI: {device.rssi}")