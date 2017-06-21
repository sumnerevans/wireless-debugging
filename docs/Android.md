# Android

## 1. Include the library in your app
1. Add: `compile 'live.flume.wireless.debugger:wirelessdebugger:1.0.0'` to your
   `build.gradle` file.

## 2. Setting up the Wireless Debugger

1. Create a new string resource file and add the following fields, replacing
   server and key with the appropriate values:

       <string name="wireless_debug_server">server</string>
       <string name="wireless_debug_api_key">key</string>

    **Note:** Creating a file to store your information is not required but is
    recommended in order to keep your information private. Do not add the file
    to your source control.

2. Start WirelessDebugger when your app starts by adding this line to your
   launcher activity’s `onCreate` method:

       WirelessDebugger.start(R.string.wireless_debug_server, R.string.wireless_debug_api_key, getApplicationContext());

Now, when your app starts Wireless Debugger will automatically start logging.

### Other Options
Wireless Debugger can also be given a time interval as an argument.  The time
interval tells Wireless Debugger how frequently to send messages to the server.
The default value is 200ms.  Increasing the interval will cause Wireless
Debugger to send messages less frequently, decreasing it does the opposite.
Most of the time changing the interval is not needed but with large logs or slow
network connection, you may find changing the interval is beneficial.

Example: Sending logs every 1 second

    WirelessDebugger.start(R.string.wireless_debug_server, R.string.wireless_debug_api_key, getApplicationContext(), 1000);
