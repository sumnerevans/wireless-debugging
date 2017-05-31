package com.google.wireless.debugger;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;

/**
 * Wireless Debugger is a background service that run for the lifetime of the app it is attached to.
 * During this time it will send device logs to a server.
 * To start this service use the WirelessDebugger start method.
 */
public class WirelessDebugger extends Service {

    private static WirelessDebugger mWirelessDebuggerInstance;

    private static final String TAG = "Wireless Debugger";
    // Extras to pass arguments to the intent that starts the service
    private static final String HOSTNAME_EXTRA = "hostname";
    private static final String TIME_INTERVAL_EXTRA = "time_interval";

    private LogReader mLogReader;

    /**
     * Starts wireless debugging for the calling application.
     * @param hostname IP/domain of the server to send logs to
     * @param timeInterval Time interval (in ms) between sending logs
     * @param appContext Context of the calling application (use getApplicationContext())
     */
    public static void start(String hostname, int timeInterval, Context appContext) {
        if (mWirelessDebuggerInstance == null) {
            mWirelessDebuggerInstance = new WirelessDebugger(hostname, timeInterval, appContext);
        }
    }

    /**
     * Private Constructor that starts the WirelessDebugger service.
     * @param hostname Server IP/Hostname
     * @param timeInterval Time Interval between sending logs
     * @param appContext Hosting application's context
     */
    private WirelessDebugger(String hostname, int timeInterval, Context appContext) {
        Intent startIntent = new Intent(appContext, this.getClass());
        startIntent.putExtra(HOSTNAME_EXTRA, hostname);
        startIntent.putExtra(TIME_INTERVAL_EXTRA, timeInterval);
        appContext.startService(startIntent);
    }

    /**
     * Required by Android
     * DO NOT CALL
     */
    public WirelessDebugger() {}

    /**
     * Called by the OS after startService(Intent) is called.
     * Creates and starts the log reading background thread
     * @param intent Intent used to start the service (must contain host and time interval extras)
     * @param flags Used by OS
     * @param startId Used by OS
     * @return Integer telling the OS how to handle the service if it exits.
     */
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        Log.d(TAG, "Service Started");
        // Create and start threads
        String hostname = intent.getStringExtra(HOSTNAME_EXTRA);
        int timeInterval = intent.getIntExtra(TIME_INTERVAL_EXTRA, 500);
        mLogReader = new LogReader(hostname, timeInterval);
        Thread logThread = new Thread(mLogReader);
        logThread.start();

        // Prevents OS from attempting to restart the service if it is killed
        return START_NOT_STICKY;
    }

    /**
     * Called when the hosting application is removed. (swiped away on the multi-taking menu)
     * Will need to research further if this is the best way to stop the logging
     * @param rootIntent
     */
    @Override
    public void onTaskRemoved(Intent rootIntent) {
        super.onTaskRemoved(rootIntent);
        Log.d(TAG, "Service Stopped, Task Removed");
        mLogReader.setAppTerminated();
        while (mLogReader.isThreadRunning()){
            // Wait for mLogReader to finish sending logs
            // Probably should set timeouts for this
        }
        stopSelf();
    }

    @Override
    public void onDestroy() {
        // Debugging Only
        Log.d(TAG, "Service Destroyed");
    }

    /**
     * Wireless Debugger runs as an unbound service, thus this method is not needed
     */
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
