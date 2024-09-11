package bluetooth;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class BeaconScanner {

    // Store Bluetooth devices as a map with MAC address as the key
    private Map<String, BluetoothDevice> bluetoothDevices = new HashMap<>();

    public void scan() {
        try {
            // Run the Python script to scan for Bluetooth devices
            Process process = Runtime.getRuntime().exec("venv\\Scripts\\python.exe src/bluetooth/ble_scan.py");

            // Capture the output of the Python script
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;

            while ((line = reader.readLine()) != null) {
                // The Python script should output: "Device: <MAC>, RSSI: <RSSI>"
                if (line.startsWith("Device:")) {
                    String[] parts = line.split(", RSSI: ");
                    String macAddress = parts[0].split("Device: ")[1].trim();
                    int rssi = Integer.parseInt(parts[1].trim());

                    // Check if the device already exists
                    if (bluetoothDevices.containsKey(macAddress)) {
                        // Update the existing device's RSSI value
                        BluetoothDevice device = bluetoothDevices.get(macAddress);
                        device.setRssi(rssi);
                    } else {
                        // Create a new BluetoothDevice object and store it
                        BluetoothDevice newDevice = new BluetoothDevice(macAddress, rssi);
                        bluetoothDevices.put(macAddress, newDevice);
                    }
                }
            }

            process.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Print all detected devices
    public void printDevices() {
        for (BluetoothDevice device : bluetoothDevices.values()) {
            System.out.println(device.getMacAddress());
            System.out.println(device.getRssi());
            System.out.println("\n");
        }
    }
}
