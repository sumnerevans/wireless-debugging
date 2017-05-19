package com.google.wireless.debugger;


public class WirelessDebugger {

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



}
