package com.google.wireless.debugger;

import android.util.Log;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONObject;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;

/**
 * Creates a WebSocket connection with a specified server and sends packaged logs.
 */
class WebSocketMessenger extends WebSocketClient {

    private static final String TAG = "Web Socket Messenger";
    private ArrayList<String> logsToSend;
    private int updateTimeInterval;
    private long lastSendTime = 0;
    private boolean running = true;

    /**
     * Creates a new WebSocketMessenger using the specified address.
     * If the address is invalid this function will return null.
     * @param socketAddress: The address (hostname or IP) of the WebSocket connection
     * @return A new WebSocket messenger object, or null if the URI is invalid
     */
    static WebSocketMessenger buildNewConnection(String socketAddress, int updateTime) {
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
     * @param uri: Specifies address of the WebSocket connection.
     */
    private WebSocketMessenger(URI uri, int updateTime) {
        super(uri);
        logsToSend = new ArrayList<>();
        updateTimeInterval = updateTime;
        connect();
    }

    /**
     * Callback function for when a connection is opened.
     * @param serverHandshake
     */
    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        Log.i(TAG, "Connection opened!");

        // TODO: send a start session message
    }

    /**
     * Needs to be implmented for WebSocketClient
     * However, we will never receive messages, so this is unused
     * @param s, The received message
     */
    @Override
    public void onMessage(String s) {}


    @Override
    public void onClose(int i, String s, boolean b) {
        Log.i(TAG, "Closed " + s);
    }


    @Override
    public void onError(Exception e) {
        running = false;
        Log.e(TAG, "Error " + e.getMessage());

    }


    /**
     * Takes all the logs from the array list and places them all in a JSON object.
     * Clears the list then sends the the JSON object to the server
     */
    private void sendLogDump() {
        JSONObject payload = new JSONObject();
        // TODO: Check if logsToSend is empty, and don't send empty messages
        try {
            payload.put("messageType", "logDump");
            payload.put("osType", "Android");

            String queuedLogs = "";
            for( String logLine : logsToSend ) {
                queuedLogs += logLine + "\n";
            }
            payload.put("rawLogData", queuedLogs);
            logsToSend.clear();
        } catch (Exception e) {
            Log.e(TAG, e.toString());
        }
        send(payload.toString());
    }


    public void enqueueLog(String logLine) {
        logsToSend.add(logLine);
        // TODO: Move this to another function
        long diff = System.currentTimeMillis() - lastSendTime;
        if (diff > updateTimeInterval && isOpen()) {
            sendLogDump();
        }
    }

    public boolean isRunning() { return running; }

}
