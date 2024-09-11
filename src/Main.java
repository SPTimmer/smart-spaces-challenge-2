import bluetooth.BeaconScanner;

public class Main {
    BeaconScanner beaconScanner;

    public Main() {
        beaconScanner = new BeaconScanner();
    }

    public void run() {
        beaconScanner.scan();
        beaconScanner.printDevices();
    }

    public static void main(String[] args) {
        new Main().run();
    }
}
