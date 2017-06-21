# iOS
## 1. Include the library in your application
1. Copy the `mobile/ios/WirelessDebug` folder into your project.
2. In Xcode, right-click on your project and select "Add Files to
   "<PROJECT_NAME>"..."
3. Select all of the files in the `WirelessDebug` folder that you copied in step
   1.

## 2. Set up the Log Streamer
1. In your `AppDelegate.swift` file, add the following line in the `application`
   method:

       LogStreamer.start(hostname: self.hostname, apiKey: "test")

2. If you already have a `NSSetUncaughtExceptionHandler` statement, add the
   following line to the closure:

       LogStreamer.handleUncaughtException(exception)

3. If you do do not yet have an `NSSetUncaughtExceptionHandler` statement, add
   the following to the the `application` method:

       NSSetUncaughtExceptionHandler { exception in
           LogStreamer.handleUncaughtException(exception)
       }

### Additional Options
#### Time Interval
Wireless Debugger can also be given a time interval as an argument. The time
interval tells Wireless Debugger how frequently to send messages to the server.
The default value is 100ms. Increasing the interval will cause Wireless Debugger
to send messages less frequently, decreasing it does the opposite. Most of the
time changing the interval is not needed but with large logs or slow network
connection, you may find changing the interval is beneficial.

Example: sending logs every second (1000ms):

    LogStreamer.start(hostname: self.hostname, apiKey: "test", timeInterval: 1000)

#### Verbosity
If you would like to disable logs coming from the Wireless Debugging library,
you can set the `verbose` flag to false:

    LogStreamer.start(hostname: self.hostname, apiKey: "test", verbose: false)
