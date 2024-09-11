package bluetooth;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class PythonBLEScanner {

    public void runPythonScript() {
        try {
            Process process = Runtime.getRuntime().exec("python src/bluetooth/ble_scan.py");

            // Capture the Python script output
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);  // Display the output
            }
            process.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        new PythonBLEScanner().runPythonScript();
    }
}
