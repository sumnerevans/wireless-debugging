package com.google.wireless.debugger;

import android.os.Build;
import android.support.test.runner.AndroidJUnit4;
import android.util.Log;

import junit.framework.Assert;
import org.json.JSONException;
import org.json.JSONObject;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.util.ArrayList;

@RunWith(AndroidJUnit4.class)
public class MessageFormatTest {

    private static final String MESSAGE_TYPE = "messageType";
    private static final String OS_TYPE = "osType";
    private static final String API_KEY = "1dc3648d-e0ce-4abf-bf9b-1cf5683c7ea8";
    private static final String APP_NAME = "Wireless Debugger Test App";

    private WebSocketMessenger webSocketMessenger;

    @Before
    public void setupTestObjects() {
        webSocketMessenger = WebSocketMessenger.buildNewConnection("none", API_KEY, APP_NAME);
    }

    @Test
    public void testStartSession() throws JSONException {
        JSONObject startSessionObject = webSocketMessenger.createStartSessionObject();

        StringBuilder deviceName = new StringBuilder();
        deviceName.append(Build.MANUFACTURER);
        deviceName.append(" ");
        deviceName.append(Build.MODEL);
        deviceName.append(" ");
        deviceName.append(Build.DEVICE);

        Assert.assertEquals(startSessionObject.getString(MESSAGE_TYPE), "startSession");
        Assert.assertEquals(startSessionObject.getString(OS_TYPE), "Android");
        Assert.assertEquals(startSessionObject.getString("apiKey"), API_KEY);
        Assert.assertEquals(startSessionObject.getString("appName"), APP_NAME);
        Assert.assertEquals(startSessionObject.getString("deviceName"), deviceName.toString());
    }

    @Test
    public void testLogMessage() throws JSONException {
        ArrayList<String> testLogs = new ArrayList<>();
        testLogs.add("E AndroidRuntime: FATAL EXCEPTION: main");
        testLogs.add("E AndroidRuntime: Process: com.google.wireless.debugging, PID: 23930");
        testLogs.add("E AndroidRuntime: java.lang.RuntimeException: Forced Crash");
        testLogs.add("E AndroidRuntime: \tat com.google.wireless.debugging.example.MainFragment$2" +
                ".onClick(MainFragment.java:73)");
        testLogs.add("E AndroidRuntime: \tat android.view.View.performClick(View.java:4445)");
        testLogs.add("E AndroidRuntime: \tat android.view.View$PerformClick.run(View.java:18446)");
        testLogs.add("E AndroidRuntime: \tat android.os.Handler.handleCallback(Handler.java:733)");
        testLogs.add("E AndroidRuntime: \tat android.os.Handler.dispatchMessage(Handler.java:95)");
        testLogs.add("E AndroidRuntime: \tat android.os.Looper.loop(Looper.java:136)");
        testLogs.add("E AndroidRuntime: \tat android.app.ActivityThread.main(ActivityThread.java" +
                ":5146)");
        testLogs.add("E AndroidRuntime: \tat java.lang.reflect.Method.invokeNative(Native Method)");
        testLogs.add("E AndroidRuntime: \tat java.lang.reflect.Method.invoke(Method.java:515)");
        testLogs.add("E AndroidRuntime: \tat com.android.internal.os." +
                "ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)");
        testLogs.add("E AndroidRuntime: \tat com.android.internal.os.ZygoteInit.main(ZygoteInit." +
                "java:612)");
        testLogs.add("E AndroidRuntime: \tat dalvik.system.NativeStart.main(Native Method)");

        StringBuilder rawLogString = new StringBuilder();
        for (String logLine : testLogs) {
            rawLogString.append(logLine);
            rawLogString.append("\n");
        }


        JSONObject logMessage = webSocketMessenger.createLogMessageObject(testLogs);

        Assert.assertEquals(logMessage.getString(MESSAGE_TYPE), "logDump");
        Assert.assertEquals(logMessage.getString(OS_TYPE), "Android");
        Log.i("TESTING", testLogs.toString());
        Assert.assertEquals(logMessage.getString("rawLogData"), rawLogString.toString());
    }

    @Test
    public void testSystemMetricsMessage() throws JSONException {
        int totalSystemMemory = 1024;
        int memoryUsage = 425;
        double cpuUsage = 0.67;
        double bytesSentPerSec = 43.3;
        double bytesRecievedPerSec = 983.4;
        int time = 1233455678;

        JSONObject systeMetrics = webSocketMessenger.createSystemMetricsObject(memoryUsage,
                totalSystemMemory, cpuUsage, bytesSentPerSec, bytesRecievedPerSec, time);

        Assert.assertEquals(systeMetrics.getString(MESSAGE_TYPE), "deviceMetrics");
        Assert.assertEquals(systeMetrics.getString(OS_TYPE), "Android");
        Assert.assertEquals(systeMetrics.getInt("memTotal"), totalSystemMemory);
        Assert.assertEquals(systeMetrics.getInt("memUsage"), memoryUsage);
        Assert.assertEquals(systeMetrics.getDouble("cpuUsage"), cpuUsage);
        Assert.assertEquals(systeMetrics.getDouble("netSentPerSec"), bytesSentPerSec);
        Assert.assertEquals(systeMetrics.getDouble("netReceivePerSec"), bytesRecievedPerSec);
        Assert.assertEquals(systeMetrics.getInt("timeStamp"), time);
    }

    @Test
    public void testEndSessionMessage() throws JSONException {
        JSONObject endSessionObject = webSocketMessenger.createEndSessionObject();

        Assert.assertEquals(endSessionObject.getString(MESSAGE_TYPE), "endSession");
    }
}
