/*
* A model class representing a bluetooth device with properties like:
* MAC-address
* RSSI
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
