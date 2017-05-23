package com.google.wireless.debugger;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

class LogReader implements Runnable {

    private static final String TAG = "--- WDB Log Reader ---";
    private ArrayList<String> logs = new ArrayList<>();
    private Boolean hostAppRunning = true;
    private Boolean threadRunning = true;

    LogReader(String hostname, float timeInterval){
        // Create the Messenger Object

    }

    @Override
    public void run() {
        try {
            // Clear logcat buffer of any previous data and exit
            Runtime.getRuntime().exec("logcat -c");

            Process process = Runtime.getRuntime().exec("logcat -v threadtime");
            BufferedReader bufferedReader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()));

            String logLine;

            Log.d(TAG, "Begin Read line in buffer");
            while (hostAppRunning) {
                logLine = bufferedReader.readLine();

                if (logLine == null){
                    try {
                        /* This is mostly a test.  With high accelerometer logging this value
                           the difference between logs is about 20 ms, so hopefully a
                           sleep time of 10ms is enough to not miss any logs.
                         */
                        Thread.sleep(1);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    continue;
                }
                logs.add(logLine);

            }

            outputLogs();
        }
        catch (IOException ioe) {
            Log.e(TAG, "IO Exception Occurred in run() thread " + ioe.toString());
        }

        // Signals to owning service that thread operations are complete
        threadRunning = false;
    }

    /**
     * Temporary function.
     * Called if the app terminates
     */
    private void outputLogs()  {
        Log.d(TAG, "BEGIN LOG OUTPUT");
        for (String logLine : logs){
            Log.i(TAG, logLine);
        }
        Log.d(TAG, "END LOG OUTPUT");
    }

    void setAppTerminated()  {
        hostAppRunning = false;
    }

    boolean isThreadRunning()  {
        return threadRunning;
    }

}
