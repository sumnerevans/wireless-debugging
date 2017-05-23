package com.google.wireless.debugger;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import java.net.URI;
import java.net.URISyntaxException;
import org.json.JSONObject;

class LogReader implements Runnable {

    private static final String TAG = "--- WDB Log Reader ---";
    private ArrayList<String> logs = new ArrayList<>();
    private Boolean hostAppTerminated = false;
    private Boolean threadRunning = true;

    private WebSocketClient mWebSocketClient;

    @Override
    public void run() {
        try {
            // Clear logcat buffer of any previous data and exit
            Runtime.getRuntime().exec("logcat -c");

            Process process = Runtime.getRuntime().exec("logcat -v threadtime");
            BufferedReader bufferedReader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()));

            String line;
            connectWebSocket();
            mWebSocketClient.connect();

            Log.d(TAG, "Begin Read line in buffer");
            while (!hostAppTerminated) {
                line = bufferedReader.readLine();

                if (line == null){
                    try {
                        /* This is mostly a test.  With high accelerometer logging this value
                           the difference between logs is about 20 ms, so hopefully a
                           sleep time of 10ms is enough to not miss any logs.
                         */
                        Thread.sleep(1);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    continue;
                }
                logs.add(line);
                //sendMessage(line);

            }

            outputLogs();
        }
        catch (IOException ioe) {
            Log.e(TAG, "IO Exception Occurred in run() thread " + ioe.toString());
        }

        // Signals to owning service that thread operations are complete
        threadRunning = false;
    }

    /**
     * Temporary function.
     * Called if the app terminates
     */
    void outputLogs()  {
        Log.d(TAG, "BEGIN LOG OUTPUT");
        for (String logLine : logs){
            Log.i(TAG, logLine);
        }
        Log.d(TAG, "END LOG OUTPUT");
    }

    private void connectWebSocket() {
        URI uri;
        try {
            uri = new URI("ws://10.0.2.2:8080/websocket");
        } catch (URISyntaxException e) {
            e.printStackTrace();
            return;
        }

        mWebSocketClient = new WebSocketClient(uri) {
            @Override
            public void onOpen(ServerHandshake serverHandshake) {
                Log.i("Websocket", "Connection opened!");

                JSONObject payload = new JSONObject();
                try {
                    payload.put("Message", "Hello from Android!");
                } catch (Exception e) {
                    Log.e("Websocket", e.toString());
                }
                mWebSocketClient.send(payload.toString());
            }

            @Override
            public void onMessage(String s) {
                Log.i("Websocket", "I got a message!");
            }

            @Override
            public void onClose(int i, String s, boolean b) {
                Log.i("Websocket", "Closed " + s);
            }

            @Override
            public void onError(Exception e) {
                Log.i("Websocket", "Error " + e.getMessage());
            }
        };
        //mWebSocketClient.connect();
    }

    public void sendMessage(String logContent) {
        JSONObject payload = new JSONObject();
        try {
            payload.put("Message", logContent);
        } catch (Exception e) {
            Log.e("Websocket", e.toString());
        }
        mWebSocketClient.send(payload.toString());
    }
    void setAppTerminated()  {
        hostAppTerminated = true;
    }

    boolean isThreadRunning()  {
        return threadRunning;
    }

}
