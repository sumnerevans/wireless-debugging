package com.google.wireless.debugger;

import android.util.Log;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
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
    private ArrayList<String> mLogsToSend;
    private int mUpdateTimeInterval;
    private long mLastSendTime = 0;
    private boolean mRunning;

    /**
     * Creates a new WebSocketMessenger using the specified address.
     * If the address is invalid this function will return null.
     * @param socketAddress: The address (hostname or IP) of the WebSocket connection.
     * @return A new WebSocket messenger object, or null if the URI is invalid.
     */
    @CheckForNull
    public static WebSocketMessenger buildNewConnection(String socketAddress, int updateTime) {
        URI uri;
        Log.i(TAG, "URI: " + socketAddress);
        try {
            uri = new URI("ws://" + socketAddress + "/ws");
        } catch (URISyntaxException e) {
            e.printStackTrace();
            return null;
        }

        return new WebSocketMessenger(uri, updateTime);
    }

    /**
     * Constructs a new WebSocketMessenger object and attempts to establish a connection.
     * @param uri: Specifies address of the WebSocket connection.
     */
    private WebSocketMessenger(URI uri, int updateTime) {
        super(uri);
        mLogsToSend = new ArrayList<>();
        mUpdateTimeInterval = updateTime;
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

        // TODO (Reece): send a start session message
    }

    /**
     * Needs to be implemented for WebSocketClient.
     * However, we will never receive messages, so this is unused.
     * @param s, The received message.
     */
    @Override
    public void onMessage(String s) {}

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
    private void sendLogDump() {
        JSONObject payload = new JSONObject();
        // TODO (Reece): Check if mLogsToSend is empty, and don't send empty messages
        try {
            payload.put("messageType", "logDump");
            payload.put("osType", "Android");

            String queuedLogs = "";
            ArrayList<String> logsToSendCopy = mLogsToSend;
            mLogsToSend.clear();
            for( String logLine : logsToSendCopy) {
                queuedLogs += logLine + "\n";
            }
            payload.put("rawLogData", queuedLogs);
        } catch (Exception e) {
            Log.e(TAG, e.toString());
        }
        send(payload.toString());
    }

    /**
     * Places logLine in a queue to be sent to the server.
     * @param logLine Raw log to be sent.
     */
    public void enqueueLog(String logLine) {
        mLogsToSend.add(logLine);
        // TODO (Reece): Move this to another function
        long diff = System.currentTimeMillis() - mLastSendTime;
        if (diff > mUpdateTimeInterval && isOpen()) {
            sendLogDump();
        }
    }

    /**
     * Returns weather or not the connection is mRunning.
     * @return True if there is a connection, false otherwise.
     */
    public boolean isRunning() { return mRunning; }

}
