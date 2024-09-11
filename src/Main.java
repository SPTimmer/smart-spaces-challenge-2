import bluetooth.BeaconScanner;

import javax.bluetooth.BluetoothStateException;

public class Main {
    BeaconScanner beaconScanner;

    public Main() {
        try {
            beaconScanner = new BeaconScanner();
        } catch (BluetoothStateException e) {
            throw new RuntimeException(e);
        }
    }

    public void run() {
        beaconScanner.scan();
    }

    public static void main(String[] args) {
        new Main().run();
        System.out.print("Hello World!\n");
    }
}
