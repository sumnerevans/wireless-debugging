package com.google.wireless.debugger;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

class LogReader implements Runnable {

    private static final String TAG = "--- WDB Log Reader ---";

    @Override
    public void run() {
        try {
            Process process = Runtime.getRuntime().exec("logcat -d");
            BufferedReader bufferedReader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()));

            ArrayList<String> log = new ArrayList<>();
            String line = "";

            Log.d(TAG, "Begin Read line in buffer");
            while (true) {
                line = bufferedReader.readLine();

                if (line == null){
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    continue;
                }
                log.add(line);

                if (log.size() > 100){
                    break;
                }
            }
            Log.d(TAG, "End Read line in buffer");
            Log.d(TAG, "BEGIN LOG OUTPUT");
            for (String logLine : log){
                Log.i(TAG, logLine);
            }
            Log.d(TAG, "END LOG OUTPUT");

        }
        catch (IOException ioe) {
            Log.e(TAG,
                    "IO Exception Occurred in Net Logging Thread " + ioe.toString());
        }
    }
}
