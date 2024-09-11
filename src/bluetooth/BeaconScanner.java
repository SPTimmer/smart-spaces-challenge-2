package bluetooth;

import javax.bluetooth.BluetoothStateException;
import javax.bluetooth.DiscoveryAgent;
import javax.bluetooth.LocalDevice;
import javax.bluetooth.RemoteDevice;

public class BeaconScanner {

    LocalDevice localDevice;
    DiscoveryAgent discoveryAgent;

    public BeaconScanner() throws BluetoothStateException {
        localDevice = LocalDevice.getLocalDevice();
        discoveryAgent = localDevice.getDiscoveryAgent();
    }

    public void scan() {
        RemoteDevice[] remoteDevices = discoveryAgent.retrieveDevices(DiscoveryAgent.PREKNOWN);
        for (RemoteDevice remoteDevice : remoteDevices) {
            System.out.println(remoteDevice.getBluetoothAddress());

        }
    }
}
