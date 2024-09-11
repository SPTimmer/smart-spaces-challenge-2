class BluetoothDevice:
    def __init__(self, mac_address, rssi):
        self.mac_address = mac_address
        self.rssi = rssi

    def update_rssi(self, rssi):
        self.rssi = rssi

    def __str__(self):
        return f"MAC: {self.mac_address}, RSSI: {self.rssi}"
