package com.google.wireless.debugger;

import android.util.Log;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

/**
 * Reads Logcat Logs from the buffer and sends them to a server using a WebSocketMessenger.
 * Implements Runnable so it can be run its own thread.
 */
class LogReader implements Runnable {

    private static final String TAG = "Log Reader";
    private ArrayList<String> logs = new ArrayList<>();
    private Boolean hostAppRunning = true;
    private Boolean threadRunning = true;
    private WebSocketMessenger webSocketMessenger;

    /**
     * Creates LogReader instance if none exists.
     * Creates a new WebSocketMessenger also.
     * @param hostname Server's IP/Host address
     * @param timeInterval Time interval between log sends
     */
    LogReader(String hostname, int timeInterval) {
        webSocketMessenger = WebSocketMessenger.buildNewConnection(hostname, timeInterval);
        if (webSocketMessenger == null) {
           Log.e(TAG, "Failed to create WebSocketMessenger Object");
        }
    }

    /**
     * Inherited from Runnable. Run on a separate thread.
     * Performs the logging and sending of logs.
     */
    @Override
    public void run() {

        if (webSocketMessenger == null){
            Log.e(TAG, "No WebSocketMessengerObject, exiting.");
            threadRunning = false;
            return;
        }

        try {
            // Clear logcat buffer of any previous data and exit
            Runtime.getRuntime().exec("logcat -c");

            // Start the logcat process
            Process logcatProcess = Runtime.getRuntime().exec("logcat -v threadtime");
            BufferedReader bufferedReader = new BufferedReader(
                    new InputStreamReader(logcatProcess.getInputStream()));

            String logLine = "";

            Log.d(TAG, "Begin Read line in buffer");
            while (hostAppRunning && webSocketMessenger.isRunning()) {
                logLine = bufferedReader.readLine();

                if (logLine == null) {
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
                webSocketMessenger.enqueueLog(logLine);
                logs.add(logLine);
            }


            // TODO: Replace with a send finished signal to the web socket messenger
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
    private void outputLogs() {
        Log.d(TAG, "BEGIN LOG OUTPUT");
        for (String logLine : logs) {
            Log.i(TAG, logLine);
        }
        Log.d(TAG, "END LOG OUTPUT");
    }

    /**
     * Notifies LogReader that the application is no longer running, logging is not longer required.
     */
    void setAppTerminated() {
        hostAppRunning = false;
    }

    /**
     * Tells the caller if LogReader is still working (reading logs or sending them).
     * @return True if it is still running.  False otherwise.
     */
    boolean isThreadRunning() {
        return threadRunning;
    }

}
