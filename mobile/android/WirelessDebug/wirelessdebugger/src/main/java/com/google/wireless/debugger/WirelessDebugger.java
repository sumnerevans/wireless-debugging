package com.google.wireless.debugger;


import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;

public class WirelessDebugger extends Service{

    private static WirelessDebugger theInstance;

    private static final String TAG = "------ WDB ------";

    private String mHostname;
    private float mTimeInterval;
    private Thread mLogThread;
    private LogReader logReader;


    public static void start(String hostname, float time, Context appContext)  {
        if (theInstance == null){
            theInstance = new WirelessDebugger(appContext);
        }
    }

    private WirelessDebugger(Context appContext)  {

        Intent startIntent = new Intent(appContext, this.getClass());
        appContext.startService(startIntent);

    }

    // TODO: This is needed by the Manifest to declare as a Service, WHY?
    public WirelessDebugger(){}


    @Override
    public void onCreate() {
        super.onCreate();
    }

    /**
     * Called by startService(Intent) from the constructor to start the service.
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
        logReader = new LogReader();
        mLogThread = new Thread(logReader);
        mLogThread.start();


        // TODO: Investigate the meaning of the return value
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
        }
        stopSelf();
    }

    @Override
    public void onDestroy() {

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
