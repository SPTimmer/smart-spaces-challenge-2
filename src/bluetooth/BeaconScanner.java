/*
* BeaconScanner.java uses the virtual python environment to run ble_scan.py. This retrieves all
* found bluetooth devices, their MAC-address and their RSSI value. These are then processed
* as BluetoothDevice instances, which will be used by the algorithms.
* */

package bluetooth;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class BeaconScanner {

    private Map<String, BluetoothDevice> bluetoothDevices = new HashMap<>();
    public void scan() {
        try {
            Process process = Runtime.getRuntime().exec("venv\\Scripts\\python.exe src/bluetooth/ble_scan.py");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;

            while ((line = reader.readLine()) != null) {
                if (line.startsWith("Device:")) {
                    String[] parts = line.split(", RSSI: ");
                    String macAddress = parts[0].split("Device: ")[1].trim();
                    int rssi = Integer.parseInt(parts[1].trim());

                    if (bluetoothDevices.containsKey(macAddress)) {
                        BluetoothDevice device = bluetoothDevices.get(macAddress);
                        device.setRssi(rssi);
                    } else {
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

    // DEBUGGING PURPOSES
    public void printDevices() {
        for (BluetoothDevice device : bluetoothDevices.values()) {
            System.out.println(device.getMacAddress());
            System.out.println(device.getRssi());
            System.out.println("\n");
        }
    }
}
