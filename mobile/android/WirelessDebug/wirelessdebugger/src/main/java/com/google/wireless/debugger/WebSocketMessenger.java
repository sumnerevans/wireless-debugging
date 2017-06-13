package com.google.wireless.debugger;

import android.os.Build;
import android.util.Log;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONException;
import org.json.JSONObject;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import javax.annotation.CheckForNull;

/**
 * Creates a WebSocket connection with a specified server and sends packaged logs.
 */
class WebSocketMessenger extends WebSocketClient {

    private static final String TAG = "Web Socket Messenger";
    private final ArrayList<String> mLogsToSend;
    private final String mApiKey;
    private boolean mRunning;
    private String mHostAppName;

    /**
     * Creates a new WebSocketMessenger using the specified address.
     * If the address is invalid this function will return null.
     * @param socketAddress: The address (hostname or IP) of the WebSocket connection.
     * @return A new WebSocket messenger object, or null if the URI is invalid.
     */
    @CheckForNull
    public static WebSocketMessenger buildNewConnection(String socketAddress, String apiKey,
                                                        String appName) {
        URI uri;
        Log.i(TAG, "URI: " + socketAddress);
        try {
            uri = new URI("ws://" + socketAddress + "/ws");
        } catch (URISyntaxException e) {
            e.printStackTrace();
            return null;
        }

        return new WebSocketMessenger(uri, apiKey, appName);
    }

    /**
     * Constructs a new WebSocketMessenger object and attempts to establish a connection.
     * @param uri: Specifies address of the WebSocket connection.
     */
    private WebSocketMessenger(URI uri, String apiKey, String appName) {
        super(uri);
        mLogsToSend = new ArrayList<>();
        mApiKey = apiKey;
        mHostAppName = appName;
        connect();
        mRunning = true;
    }

    /**
     * Callback function for when a connection is opened.
     * @param serverHandshake
     */
    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        Log.i(TAG, "Connection opened!");

        JSONObject payload = new JSONObject();

        StringBuilder deviceNameBuilder = new StringBuilder();
        deviceNameBuilder.append(Build.MANUFACTURER);
        deviceNameBuilder.append(" ");
        deviceNameBuilder.append(Build.MODEL);
        deviceNameBuilder.append(" ");
        deviceNameBuilder.append(Build.DEVICE);

        try {
            payload.put("messageType", "startSession");
            payload.put("osType", "Android");
            payload.put("apiKey", mApiKey);
            payload.put("deviceName", deviceNameBuilder.toString());
            payload.put("appName", mHostAppName);

        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }
        // TODO(Reece): Handle WebsocketNotConnectedException
        send(payload.toString());
    }

    /**
     * Needs to be implemented for WebSocketClient.
     * However, we will never receive messages, so this is unused.
     * @param s, The received message.
     */
    @Override
    public void onMessage(String s) {
    }

    /**
     * Called by the parent when the web socket connection is closed.
     */
    @Override
    public void onClose(int i, String s, boolean b) {
        mRunning = false;
        Log.i(TAG, "Closed " + s);
    }

    /**
     * Called by the parent if a web socket error occurs.
     */
    @Override
    public void onError(Exception e) {
        mRunning = false;
        Log.e(TAG, "Error " + e.getMessage());
    }

    /**
     * Takes all the logs from the array list and places them all in a JSON object.
     * Clears the list then sends the the JSON object to the server.
     */
    public void sendLogDump() {
        if (mLogsToSend.isEmpty()) {
            return;
        }

        JSONObject payload = new JSONObject();
        try {
            payload.put("messageType", "logDump");
            payload.put("osType", "Android");

            String queuedLogs = "";

            // Copy the array list to prevent possible race conditions when sending/enqueuing logs
            ArrayList<String> logsToSendCopy = new ArrayList<>(mLogsToSend);
            mLogsToSend.clear();

            for (String logLine : logsToSendCopy) {
                queuedLogs += logLine + "\n";
            }
            payload.put("rawLogData", queuedLogs);
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }

        // TODO(Reece): Handle WebsocketNotConnectedException
        send(payload.toString());
    }

    /**
     * Places logLine in a queue to be sent to the server.
     * @param logLine Raw log to be sent.
     */
    public void enqueueLog(String logLine) {
        mLogsToSend.add(logLine);
    }

    public void sendSystemMetrics(int memUsed, int memTotal, double cpuUsage, double
            bytesSentPerSec, double
            bytesReceivedPerSec, long timeStamp) {
        JSONObject payload = new JSONObject();
        try {
            payload.put("messageType", "deviceMetrics");
            payload.put("osType", "Android");
            payload.put("timeStamp", timeStamp);
            payload.put("cpuUsage", cpuUsage);
            payload.put("memUsage", memUsed);
            payload.put("memTotal", memTotal);
            payload.put("netSentPerSec", bytesSentPerSec);
            payload.put("netReceivePerSec", bytesReceivedPerSec);
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }

        // TODO(Reece): Handle WebsocketNotConnectedException
        send(payload.toString());
    }

    /**
     * Returns weather or not the connection is mRunning.
     * @return True if there is a connection, false otherwise.
     */
    public boolean isRunning() {
        return mRunning;
    }
}
