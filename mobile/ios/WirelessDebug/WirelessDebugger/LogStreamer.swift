//
//  WirelessDebugger.swift
//  Wireless Debug iOS Test App
//

import Foundation

/// Main class for the Wireless Debugger library. This class handles capturing
/// logs and sends them to the WebSocketMessenger.
class LogStreamer {
    private static var logStreamer: LogStreamer?

    private var webSocketMessenger: WebSocketMessenger?
    private var timeInterval: UInt32

    /// Initialise the Wireless Debugger library.
    ///
    /// - Parameters:
    ///   - hostname: root hostname to connect to
    ///   - apiKey: the API Key provided by the web interface
    ///   - timeInterval: the interval at which to send logs
    private init(_ hostname: String, apiKey: String, timeInterval: Int) {
        self.webSocketMessenger = WebSocketMessenger("ws://\(hostname)/ws",
                                                     apiKey: apiKey)
        self.timeInterval = UInt32(timeInterval)

        // Create a Pipe and capture stderr.
        let stderrPipe = Pipe()
        dup2(stderrPipe.fileHandleForWriting.fileDescriptor, fileno(stderr))

        // Poll for data coming in on stderr. When logs come in, enqueue them
        // for sending to the server and re-output them on stdout.
        DispatchQueue.global().async {
            while true {
                // Wait until data is available in the pipe and grab it.
                let data = stderrPipe.fileHandleForReading.availableData
                let logData = String(data: data, encoding: .utf8) ?? ""
                self.webSocketMessenger?.enqueueLog(logLine: logData)
                print(logData)
            }
        }

        // Every time interval, send the logs if enough time has elapsed.
        DispatchQueue.global().async {
            while true {
                self.webSocketMessenger?.sendLogDump()
                // usleep requires nanoseconds, so multiply ms by 1000.
                usleep(self.timeInterval * 1000)
            }
        }
    }

    /// Start the wireless debugger.
    ///
    /// **Example:** `LogStreamer.start("localhost", "API-KEY")`
    ///
    /// - Parameters:
    ///   - hostname: root hostname to connect to
    ///   - apiKey: the API Key provided by the web interface
    ///   - timeInterval: the interval at which to send logs (in milliseconds)
    static func start(hostname: String, apiKey: String, timeInterval: Int = 100) {
        if logStreamer == nil {
            logStreamer = LogStreamer(hostname, apiKey: apiKey,
                                                timeInterval: timeInterval)
        }
    }
 
    static func handleUncaughtException(_ exception: NSException) {
        logStreamer?.webSocketMessenger?.sendUnhandledException(exception: exception)
    }
}
