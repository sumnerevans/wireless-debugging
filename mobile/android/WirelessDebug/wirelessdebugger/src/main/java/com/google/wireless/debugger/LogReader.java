package com.google.wireless.debugger;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

class LogReader implements Runnable {

    private static final String TAG = "--- WDB Log Reader ---";
    private ArrayList<String> logs = new ArrayList<>();

    @Override
    public void run() {
        try {
            Process process = Runtime.getRuntime().exec("logcat -d");
            BufferedReader bufferedReader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()));

            String line;

            Log.d(TAG, "Begin Read line in buffer");
            while (true) {
                line = bufferedReader.readLine();

                if (line == null){
                    try {
                        /* This is mostly a test.  With high accelerometer logging this value
                           the difference between logs is about 20 ms, so hopefully a
                           sleep time of 10ms is enough to not miss any logs.
                         */
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    continue;
                }
                logs.add(line);

                /*
                if (log.size() > 100){
                    break;
                }
                */
            }
            /*
            Log.d(TAG, "End Read line in buffer");
            Log.d(TAG, "BEGIN LOG OUTPUT");
            for (String logLine : logs){
                Log.i(TAG, logLine);
            }
            Log.d(TAG, "END LOG OUTPUT");
            */

        }
        catch (IOException ioe) {
            Log.e(TAG, "IO Exception Occurred in run() thread " + ioe.toString());
        }
    }

    /**
     * Temporary function.
     * Called if the app terminates
     */
    void sendLogs(){
        Log.d(TAG, "BEGIN LOG OUTPUT");
        for (String logLine : logs){
            Log.i(TAG, logLine);
        }
        Log.d(TAG, "END LOG OUTPUT");
    }

}
