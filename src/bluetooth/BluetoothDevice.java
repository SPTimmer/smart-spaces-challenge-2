/*
* Instances of BluetoothDevice.java are generated by BeaconScanner.java. When BeaconScanner.java
* detects a new bluetooth device (that is, one which does not yet exist with that MAC-address,
* a new instance will be created. If however the device was already connected, only the RSSI
* value is updated.
* */

package bluetooth;

public class BluetoothDevice {
    private String macAddress;
    private int rssi;

    public BluetoothDevice(String macAddress, int rssi) {
        this.macAddress = macAddress;
        this.rssi = rssi;
    }

    public String getMacAddress() {
        return macAddress;
    }

    public int getRssi() {
        return rssi;
    }

    public void setRssi(int rssi) {
        this.rssi = rssi;
    }
}
