package live.flume.wireless.debugger;

import android.os.Build;
import android.util.Log;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.exceptions.WebsocketNotConnectedException;
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
    private boolean mIsRunning;
    private int mConnectionRetriesRemaining;
    private String mHostAppName;

    /**
     * Creates a new WebSocketMessenger using the specified address.
     * If the address is invalid this function will return null.
     * @param socketAddress: The address (hostname or IP) of the WebSocket connection.
     * @param apiKey: User's API key.
     * @param appName: Name of the application being debugged.
     * @return A new WebSocket messenger object, or null if the URI is invalid.
     */
    @CheckForNull
    public static WebSocketMessenger buildNewConnection(String socketAddress, String apiKey,
                                                        String appName) {
        URI uri;
        // Log.i(TAG, "URI: " + socketAddress);
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
        mConnectionRetriesRemaining = 10;
        connect();
        mIsRunning = true;
    }

    /**
     * Callback function for when a connection is opened.
     * @param serverHandshake
     */
    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        //Log.i(TAG, "Connection opened!");
        sendAndCatch(createStartSessionObject().toString());
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
        mIsRunning = false;
        // Log.i(TAG, "Closed " + s);
    }

    /**
     * Called by the parent if a web socket error occurs.
     */
    @Override
    public void onError(Exception e) {
        mIsRunning = false;
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

        // Copy the array list to prevent possible race conditions when sending/enqueuing logs
        ArrayList<String> logsToSendCopy = new ArrayList<>(mLogsToSend);
        mLogsToSend.clear();

        sendWithRetries(createLogMessageObject(logsToSendCopy).toString(), logsToSendCopy);
    }

    /**
     * Places logLine in a queue to be sent to the server.
     * @param logLine Raw log to be sent.
     */
    public void enqueueLog(String logLine) {
        mLogsToSend.add(logLine);
    }

    /**
     * Sends a message to server indicating all logs have been send and the session is over.
     * Also checks to see if all the logs queued have been sent by calling sendLogDump().
     */
    public void sendEndSessionMessage() {
        sendLogDump();
        sendAndCatch(createEndSessionObject().toString());
    }

    /**
     * Sends system metrics through the web socket to the server.
     * @param memUsed Memory currently being used.
     * @param memTotal Total memory on the system.
     * @param cpuUsage CPU Usage as a double.
     * @param bytesSentPerSec Number of bytes sent per second.
     * @param bytesReceivedPerSec Number of bytes received per second.
     * @param timeStamp Time the metrics were collected in ms UTC.
     */
    public void sendSystemMetrics(int memUsed, int memTotal, double cpuUsage,
            double bytesSentPerSec, double bytesReceivedPerSec, long timeStamp) {

        String payload = createSystemMetricsObject(memUsed, memTotal, cpuUsage, bytesSentPerSec,
                    bytesReceivedPerSec, timeStamp).toString();

        sendAndCatch(payload);
    }

    /**
     * Returns weather or not the connection is mIsRunning.
     * @return True if there is a connection, false otherwise.
     */
    public boolean isRunning() {
        return mIsRunning;
    }

    /**
     * Sends a message over the websocket.  If the send fails or throws an exception, the message
     * will be put back into the queue to try again later.  This function allows 10 retries of
     * seding until it stops.
     * @param message Message to be send.
     * @param logsCopy Array List containing the original messages.  Needed to re-queue messages
     *                 in the event of a failed send.
     */
    private void sendWithRetries(String message, ArrayList<String> logsCopy) {
        try {
            if (isOpen()) {
                mConnectionRetriesRemaining = 10;
            }
            send(message);
        } catch (WebsocketNotConnectedException wse) {
            Log.e(TAG, wse.toString());

            if (mConnectionRetriesRemaining > 0) {
                mLogsToSend.addAll(logsCopy);
                mConnectionRetriesRemaining--;
            } else {
                Log.e(TAG, "Failed to send data, stopping.");
                mIsRunning = false;
            }
        }
    }

    /**
     * Sends data across the websocket and catches a WebsocketNotConnected exception if thrown.
     * @param message Message to be sent to the server.
     */
    private void sendAndCatch(String message) {
        try {
            send(message);
        } catch (WebsocketNotConnectedException wse) {
            Log.e(TAG, wse.toString());
            mIsRunning = false;
        }
    }

    /**
     * Creates a JSON object containing startSession information.  This includes the OS type,
     * device name, API Key, and App name.
     * @return Complete JSONObject.
     */
    public JSONObject createStartSessionObject() {
        JSONObject message = new JSONObject();

        StringBuilder deviceNameBuilder = new StringBuilder();
        deviceNameBuilder.append(Build.MANUFACTURER);
        deviceNameBuilder.append(" ");
        deviceNameBuilder.append(Build.MODEL);
        deviceNameBuilder.append(" ");
        deviceNameBuilder.append(Build.DEVICE);

        try {
            message.put("messageType", "startSession");
            message.put("osType", "Android");
            message.put("apiKey", mApiKey);
            message.put("deviceName", deviceNameBuilder.toString());
            message.put("appName", mHostAppName);
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }
        return message;
    }

    /**
     * Creates a JSON object containing a Log Dump message.
     * @param logQueue Array list containing log lines.
     * @return Complete JSONObject.
     */
    public JSONObject createLogMessageObject(ArrayList<String> logQueue) {
        JSONObject message = new JSONObject();
        try {
            message.put("messageType", "logDump");
            message.put("osType", "Android");

            String queuedLogs = "";

            for (String logLine : logQueue) {
                queuedLogs += logLine + "\n";
            }
            message.put("rawLogData", queuedLogs);
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }
        return message;
    }

    /**
     * Creates a JSON Object containing all device metric information.
     * @param memUsed Memory currently being used.
     * @param memTotal Total memory on the system.
     * @param cpuUsage CPU Usage as a double.
     * @param bytesSentPerSec Number of bytes sent per second.
     * @param bytesReceivedPerSec Number of bytes received per second.
     * @param timeStamp Time the metrics were collected in ms UTC.
     * @return Complete JSONObject.
     */
    public JSONObject createSystemMetricsObject(int memUsed, int memTotal, double cpuUsage, double
            bytesSentPerSec, double bytesReceivedPerSec, long timeStamp) {
        JSONObject message = new JSONObject();
        try {
            message.put("messageType", "deviceMetrics");
            message.put("osType", "Android");
            message.put("timeStamp", timeStamp);
            message.put("cpuUsage", cpuUsage);
            message.put("memUsage", memUsed);
            message.put("memTotal", memTotal);
            message.put("netSentPerSec", bytesSentPerSec);
            message.put("netReceivePerSec", bytesReceivedPerSec);
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }
        return message;
    }

    /**
     * Creates a JSON Object containing end session information.
     * @return Complete JSONObject.
     */
    public JSONObject createEndSessionObject() {
        JSONObject message = new JSONObject();
        try {
            message.put("messageType", "endSession");
        } catch (JSONException e) {
            Log.e(TAG, e.toString());
        }
        return message;
    }

}
