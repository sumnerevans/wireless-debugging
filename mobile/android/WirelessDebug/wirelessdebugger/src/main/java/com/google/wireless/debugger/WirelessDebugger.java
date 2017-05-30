package com.google.wireless.debugger;


import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;

public class WirelessDebugger extends Service {

    private static WirelessDebugger theInstance;

    private static final String TAG = "------ WDB ------";

    // Extras to pass arguments to the intent that starts the service
    private static final String HOSTNAME_EXTRA = "hostname";
    private static final String TIME_INTERVAL_EXTRA = "time_interval";

    private LogReader logReader;


    /**
     * Starts wireless debugging for the calling application
     * @param hostname IP/domain of the server to send logs to
     * @param timeInterval Time interval (in ms) between sending logs
     * @param appContext Context of the calling application (use getApplicationContext())
     */
    public static void start(String hostname, int timeInterval, Context appContext) {
        if (theInstance == null) {
            theInstance = new WirelessDebugger(hostname, timeInterval, appContext);
        }
    }

    private WirelessDebugger(String hostname, int timeInterval, Context appContext) {
        Intent startIntent = new Intent(appContext, this.getClass());
        startIntent.putExtra(HOSTNAME_EXTRA, hostname);
        startIntent.putExtra(TIME_INTERVAL_EXTRA, timeInterval);
        appContext.startService(startIntent);
    }

    // TODO: This is needed by the Manifest to declare as a Service, WHY?
    public WirelessDebugger() {}


    /**
     * Called by the OS after startService(Intent) is called.
     * Creates and starts the log reading background thread
     * @param intent
     * @param flags
     * @param startId
     * @return
     */
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        Log.d(TAG, "Service Started");
        // Create and start threads
        String hostname = intent.getStringExtra(HOSTNAME_EXTRA);
        int timeInterval = intent.getIntExtra(TIME_INTERVAL_EXTRA, 500);
        logReader = new LogReader(hostname, timeInterval);
        Thread logThread = new Thread(logReader);
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
        logReader.setAppTerminated();
        while (logReader.isThreadRunning()){
            // Wait for logReader to finish sending logs
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
     * @param intent
     * @return
     */
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
