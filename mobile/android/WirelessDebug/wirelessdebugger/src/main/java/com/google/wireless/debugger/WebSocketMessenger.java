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

    /**
     * @param uri: Specifies address of the WebSocket connection
     */
    public WebSocketMessenger(URI uri) {
        super(uri);
        logsToSend = new ArrayList<>();
        connect();
    }

    /**
     *
     * @param socketAddress: The address of the WebSocket connection
     * @return A new WebSocket messenger object, or null if the URI is invalid
     */
    public static WebSocketMessenger buildNewConnection(String socketAddress) {
        URI uri;
        try {
            uri = new URI(socketAddress);
        } catch (URISyntaxException e) {
            e.printStackTrace();
            return null;
        }

        return new WebSocketMessenger(uri);
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
        Log.i("Websocket", "Error " + e.getMessage());
    }

    // TODO: Make this a proper doc
    // Takes all of the queued logs, sends places them all in a JSON, clears the queue,
    // and finally sends the log dump to the server
    public void sendLogDump() {
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

    public void enqueueLog(String logLine) {
        logsToSend.add(logLine);
    }


}
