package bluetooth;

import javax.bluetooth.BluetoothStateException;
import javax.bluetooth.DiscoveryAgent;
import javax.bluetooth.LocalDevice;

/*
* Handles Bluetooth scanning using BlueCove
*
* It outputs RSSI data as Map<String, Integer> where the String would be the ID of the beacon,
* and the integer the RSSI.
* */
public class BeaconScanner {

    LocalDevice localDevice = LocalDevice.getLocalDevice();
    DiscoveryAgent discoveryAgent = localDevice.getDiscoveryAgent();

    public BeaconScanner() throws BluetoothStateException {
    }
}
