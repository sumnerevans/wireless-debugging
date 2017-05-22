package com.google.wireless.debugger;


import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.support.annotation.Nullable;

public class WirelessDebugger extends Service{

    private static WirelessDebugger theInstance;

    private static final String TAG = "------ WDB ------";

    private String mHostname;
    private float mTimeInterval;

    private Thread mNetLoggingThread;

    public static void start(String hostname, float time)  {
        if (theInstance == null){
            theInstance = new WirelessDebugger();
        }
    }

    private WirelessDebugger()  {

        mNetLoggingThread = new Thread(new LogReader());
        mNetLoggingThread.start();

    }


    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        // Create and start threads



        return super.onStartCommand(intent, flags, startId);
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
