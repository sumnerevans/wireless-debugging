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
    
    private let stderrPipe = Pipe()
    private var dispatchQueue = DispatchQueue(label: "LogStreamer", attributes: .concurrent)

    /// Initialize the Wireless Debugger library.
    ///
    /// - Parameters:
    ///   - hostname: root hostname to connect to
    ///   - apiKey: the API Key provided by the web interface
    ///   - timeInterval: the interval at which to send logs
    private init(_ hostname: String, apiKey: String, timeInterval: Int, verbose: Bool) {
        self.webSocketMessenger = WebSocketMessenger("ws://\(hostname)/ws",
                                                     apiKey: apiKey,
                                                     verbose: verbose)
        self.timeInterval = UInt32(timeInterval)

        // Create a Pipe and capture stderr.
        dup2(self.stderrPipe.fileHandleForWriting.fileDescriptor, fileno(stderr))

        // Poll for data coming in on stderr. When logs come in, enqueue them
        // for sending to the server and re-output them on stdout.
        self.dispatchQueue.async(execute: self.readLogs)

        // Every time interval, send the logs if enough time has elapsed.
        self.dispatchQueue.async(execute: self.sendLogs)
    }
    
    /// Send the logs to the server and wait for the time interval before
    /// running this function again.
    private func sendLogs() {
        self.webSocketMessenger?.sendLogDump()
        let nextSendTime = DispatchTime.now() + Double(self.timeInterval) / 1000
        self.dispatchQueue.asyncAfter(deadline: nextSendTime, execute: sendLogs)
    }
    
    /// Read the NSLogs from stderr and enqueue them for sending by the
    /// WebSocketMessenger. Then, run this function again.
    private func readLogs() {
        // Wait until data is available in the pipe and grab it.
        let data = self.stderrPipe.fileHandleForReading.availableData
        let logData = String(data: data, encoding: .utf8) ?? ""
        self.webSocketMessenger?.enqueueLog(logLine: logData)
        print(logData)
        self.dispatchQueue.async(execute: readLogs)
    }

    /// Start the wireless debugger.
    ///
    /// **Example:** `LogStreamer.start("localhost", "API-KEY")`
    ///
    /// - Parameters:
    ///   - hostname: root hostname to connect to
    ///   - apiKey: the API Key provided by the web interface
    ///   - timeInterval: the interval at which to send logs (in milliseconds)
    static func start(hostname: String, apiKey: String, timeInterval: Int = 100,
                      verbose: Bool = false) {
        if logStreamer == nil {
            logStreamer = LogStreamer(hostname, apiKey: apiKey,
                                                timeInterval: timeInterval,
                                                verbose: verbose)
        }
    }
 
    static func handleUncaughtException(_ exception: NSException) {
        logStreamer?.webSocketMessenger?.sendUnhandledException(exception: exception)
    }
}
