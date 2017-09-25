# WebSocket API From Mobile to Web App Backend
The Mobile library sends four WebSocket message types to the Web App Backend:
`startSession`, `logDump`, `deviceMetrics`, and `endSession`.

## Start Session

- **Message Type**: `startSession`
- **Payload Type**: JSON
- **Purpose**: when the app starts, a WebSockets connection to the Web App
  Backend will be established and a `startSession` message will immediately be
  sent to the Web App Backend. This message will tell the Web App Backend which
  device and app has connected.
- **Fields**:
    - `messageType (string)`: the type of message being sent, which in this case
      will be `startSession`.
    - `apiKey (string)`: the user’s API Key that is shown to the user on the Web
      Interface.
    - `osType (string)`: the type of OS from which the logs are being sent.
      Valid values are: "Android" and "iOS".
    - `deviceName (string)`: the device name from which the logs are being sent.
    - `appName (string)`: the name of the application from which logs are being
      sent.
- **Example**:

      {
        "messageType": "startSession",
        "apiKey": { ... },
        "osType": "Android",
        "deviceName": "Google Pixel",
        "appName": "Google Hangouts"
      }

## Log Dump
- **Message Type**: `logDump`
- **Payload Type**: JSON
- **Purpose**: the Mobile API will send a `logDump` message to the Web App
  Backend with raw log data at an interval configured by the user of the Mobile
  API. Log entries in `rawLogData` are delimited by newline characters.
- **Fields**:
    - `messageType (string)`: the type of message being sent, which in this case
      will be `logDump`.
    - `rawLogData (string)`: the actual raw log data
    - `osType (string)`: the type of OS from which the logs are being sent.
      Valid values are: "Android" and "iOS".

- **Example 1:**

      {
        "messageType": "logDump",
        "osType": "Android",
        "rawLogData": "05-22 11:44:31.180 7080-7080/com.google.wireless.debugging I/WiDB Example: aX: 3.0262709 aY: 2.0685902\n05-22 11:44:31.182 7080-7080/com.google.wireless.debugging I/WiDB Example: aX: 3.193911 aY: 2.3091934"
      }

- **Example 2:**

      {
        "messageType": "logDump",
        "osType": "Android",
        "rawLogData": "05-24 12:12:49.247 23930 23930 E AndroidRuntime: FATAL EXCEPTION: main\n05-24 12:12:49.247 23930 23930 E AndroidRuntime: Process: com.google.wireless.debugging, PID: 23930\n05-24 12:12:49.247 23930 23930 E AndroidRuntime: \tat java.lang.reflect.Method.invokeNative(Native Method)\n05-24 12:12:49.247 23930 23930 E AndroidRuntime: \tat java.lang.reflect.Method.invoke(Method.java:515)\n05-24 12:12:49.247 23930 23930 E AndroidRuntime: \tat com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)\n05-24 12:12:49.247 23930 23930 E AndroidRuntime: \tat com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)\n05-24 12:12:49.247 23930 23930 E AndroidRuntime: \tat dalvik.system.NativeStart.main(Native Method)"
      }

## Device Metrics
- **Message Type**: `deviceMetrics`
- **Payload Type**: JSON
- **Purpose**: the Mobile API will send a `deviceMetrics` message to the Web App
  Backend with statistics regarding the device health and performance. All data
  is specified in bytes.
- **Fields**:
    - `messageType (string)`: the type of message being sent, which in this case
      will be `deviceMetrics`.
    - `osType (string)`: the type of OS from which the logs are being sent.
      Valid values are: "Android" and "iOS".
    - `cpuUsage (double)`: the actual raw log data
    - `memUsage (int)`: current kilobytes used (active)
    - `memTotal (int)`: total amount of memory available
    - `netSentPerSec (double)`: bytes sent per second over the network
    - `netReceivePerSec (double)`: bytes received per second over the network
    - `timeStamp (int)`: the difference, measured in milliseconds, between the
      time of recording metrics, and midnight, January 1, 1970 UTC. 

## End Session
- **Message Type**: `endSession`
- **Payload Type**: JSON
- **Purpose**: when the app closes and the Mobile API has finished sending all
  the logs to the Web App Backend, an `endSession` message will be sent which
  will tell the Web App Backend that the session is over.
- **Fields**: 
    - `messageType (string)`: the type of message being sent, which in this case
      will be `endSession`.
- **Example**:

      {
        "messageType": "endSession"
      }
