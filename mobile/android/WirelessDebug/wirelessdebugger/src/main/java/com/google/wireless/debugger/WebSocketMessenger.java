package com.google.wireless.debugger;

import android.util.Log;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;

/**
 * Creates a WebSocket connection with a specified server.
 */

public class WebSocketMessenger extends WebSocketClient {

    private ArrayList<String> logsToSend;
    private int updateTimeInterval;
    private long lastSendTime;
    private boolean running = true;


    /**
     *
     * @param socketAddress: The address of the WebSocket connection
     * @return A new WebSocket messenger object, or null if the URI is invalid
     */
    static WebSocketMessenger buildNewConnection(String socketAddress, int updateTime) {
        URI uri;
        Log.i("--Wide Bug WS -- ", "URI: " + socketAddress);
        try {
            uri = new URI(socketAddress);
        } catch (URISyntaxException e) {
            e.printStackTrace();
            return null;
        }

        return new WebSocketMessenger(uri, updateTime);
    }

    /**
     * @param uri: Specifies address of the WebSocket connection
     */
    private WebSocketMessenger(URI uri, int updateTime) {
        super(uri);
        logsToSend = new ArrayList<>();
        updateTimeInterval = updateTime;
        connect();
    }

    /**
     *
     * @param serverHandshake
     */
    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        Log.i("Websocket", "Connection opened!");

        JSONObject payload = new JSONObject();
        try {
            payload.put("Message", "Hello from Anrdoid: " + R.string.app_name);
        } catch (Exception e) {
            Log.e("Websocket", e.toString());
        }
        send(payload.toString());
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
        Log.i("Websocket", "Closed " + s);
    }


    @Override
    public void onError(Exception e) {
        running = false;
        Log.e("Websocket", "Error " + e.getMessage());

    }


    /**
     * Takes all the logs from the array list and places them all in a JSON object.
     * Clears the list then sends the the JSON object to the server
     */
    private void sendLogDump() {
        JSONObject payload = new JSONObject();
        try {
            payload.put("messageType", "logDump");
            payload.put("osType", "Android");

            String queuedLogs = "";
            for(String logLine : logsToSend) {
                queuedLogs += logLine + "\n";
            }
            payload.put("rawLogData", queuedLogs);
            logsToSend.clear();
        } catch (Exception e) {
            Log.e("Websocket", e.toString());
        }
        send(payload.toString());
    }


    void enqueueLog(String logLine) {
        logsToSend.add(logLine);
        long diff = System.currentTimeMillis() - lastSendTime;
        if (diff > updateTimeInterval && isOpen()){
            sendLogDump();
        }
    }

    boolean isRunning() { return running; }

}
