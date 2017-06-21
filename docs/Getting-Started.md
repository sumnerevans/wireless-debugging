# Getting Started
There are many ways to use Wireless Debugger. This article describes the
simplest case where you want to use Wireless Debug without any modifications.
There are two main steps that you need to perform to use Wireless Debug:

## 1. Deploy the Wireless Debug server component
The easiest way to deploy the Wireless Debug server component is using
[Docker](https://www.docker.com/). Instructions for installing Docker can be
found at [their website](https://docs.docker.com/engine/installation/). For
other deployment options, see the [Deployment](Deployment) wiki page.

After installing Docker, all you need to do is run:

    docker pull jsve/wireless-debugging
    docker run -p 80:80 jsve/wireless-debugging

*Note: you may have to prepend `sudo` to the above commands to run them with
elevated privileges.*

## 2. Include the Wireless Debug library in your application
### Android
*See the full guide [here](Android).*

1. Add: `compile 'live.flume.wireless.debugger:wirelessdebugger:1.0.0'` to your
   build.gradle

2. Create a new string resource file and add the following fields, replacing
   server and key with the appropriate values:

       <string name="wireless_debug_server">server</string>
       <string name="wireless_debug_api_key">key</string>

    Note: Creating a file to store your information is not required but is
    recommended in order to keep your information private. Do not add the file
    to your source control.

3. Start WirelessDebugger when your app starts by adding this line to your
   launcher activity’s `onCreate` method:

       WirelessDebugger.start(R.string.wireless_debug_server, R.string.wireless_debug_api_key, getApplicationContext());

### iOS
*See the full guide [here](iOS).*

1. Copy the `mobile/ios/WirelessDebug` folder into your project.
2. In Xcode, right-click on your project and select "Add Files to
   "<PROJECT_NAME>"..."
3. Select all of the files in the `WirelessDebug` folder that you copied in step
   1.
4. In your `AppDelegate.swift` file, add the following line in the `application`
   method:

       LogStreamer.start(hostname: self.hostname, apiKey: "test")

5. If you already have a `NSSetUncaughtExceptionHandler` statement, add the
   following line to the closure:

       LogStreamer.handleUncaughtException(exception)

6. If you do do not yet have an `NSSetUncaughtExceptionHandler` statement, add
   the following to the `application` method:

       NSSetUncaughtExceptionHandler { exception in
           LogStreamer.handleUncaughtException(exception)
       }
