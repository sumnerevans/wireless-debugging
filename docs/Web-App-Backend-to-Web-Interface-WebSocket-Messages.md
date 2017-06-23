There is a single type of WebSocket message that goes from the Web App Backend to the Web Interface, and it is the information with the formatted HTML logs.   

## Log Entries
- **Message Type**: `logData`
- **Payload Type**: JSON
- **Purpose**: when the Web App Backend receives a `logDump` from the Mobile API, it will parse the log via the parsing library and then it will send a logData message to all Web Interfaces that the user is connected to.
- **Fields:**
    - `messageType (string)`: the type of message being sent, which in this case will be `logData`.
    - `osType (string)`: the type of OS from which the logs are being sent. Valid values are: "Android" and "iOS".
    - `logEntries (stringHTML)`: formatted HTML table rows to append to the log table. The table divisions will be ordered: time, tag, log type, log text.
- **Example**:

      {
         "messageType": "logData",
         "osType": "Android",
         "logEntries" : "
         <tr class="exception">
         <td>2017-11-06 16:34:41.000</td>
         <td>TEST</td>
         <td>Exception</td>
         <td>FATAL EXCEPTION: main<br>
           Process: com.google.wireless.debugging, PID: 23930<br>
           java.lang.RuntimeException: Forced Crash<br>
           at com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)<br>
           at android.view.View.performClick(View.java:4445)<br>
           at android.view.View$PerformClick.run(View.java:18446)<br>
           at android.os.Handler.handleCallback(Handler.java:733)<br>
           at android.os.Handler.dispatchMessage(Handler.java:95)<br>
           at android.os.Looper.loop(Looper.java:136)<br>
           at java.lang.reflect.Method.invoke(Method.java:515)<br>
           at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)<br>
           at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)<br>
           at dalvik.system.NativeStart.main(Native Method)
         </td>
       </tr>
       <tr class="exception">
         <td>2017-11-06 16:34:41.001</td>
         <td>TEST</td>
         <td>Info</td>
         <td>test log</td>
       </tr>"
       }
