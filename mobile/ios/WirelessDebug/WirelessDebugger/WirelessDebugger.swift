//
//  WirelessDebugger.swift
//  Wireless Debug iOS Test App
//

import Foundation

/// Main class for the Wireless Debugger library. This class handles capturing
/// logs and sends them to the WebSocketMessenger.
class WirelessDebugger {
    private static var wirelessDebugger: WirelessDebugger?

    private var webSocketMessenger: WebSocketMessenger?
    private var lastSendTime: UInt64 = 0
    private var timeInterval: Int

    /// Initialise the Wireless Debugger library.
    ///
    /// - Parameters:
    ///   - hostname: root hostname to connect to
    ///   - apiKey: the API Key provided by the web interface
    ///   - timeInterval: the interval at which to send logs
    private init(_ hostname: String, apiKey: String, timeInterval: Int) {
        self.webSocketMessenger = WebSocketMessenger("ws://\(hostname)/ws",
                                                     apiKey: apiKey)
        self.timeInterval = timeInterval

        // Create a Pipe and capture stderr.
        let stderrPipe = Pipe()
        dup2(stderrPipe.fileHandleForWriting.fileDescriptor, fileno(stderr))

        // Poll for data coming in on stderr. When logs come in, enqueue them
        // for sending to the server and re-output them on stdout.
        DispatchQueue.global().async {
            while true {
                let data = stderrPipe.fileHandleForReading.availableData
                DispatchQueue.main.async {
                    // Capture the log
                    let logData = String(data: data, encoding: .utf8) ?? ""
                    self.webSocketMessenger!.enqueueLog(logLine: logData)
                    print(logData)
                }
            }
        }

        // Every 10ms, send the logs if enough time has elapsed.
        DispatchQueue.global().async {
            while true {
                self.sendLogsIfReady()
                usleep(10000) // sleep for 10 ms, usleep accepts microseconds
            }
        }
    }

    /// Start the wireless debugger.
    ///
    /// - Parameters:
    ///   - hostname: root hostname to connect to
    ///   - apiKey: the API Key provided by the web interface
    ///   - timeInterval: the interval at which to send logs (in milliseconds)
    static func start(hostname: String, apiKey: String, timeInterval: Int = 100) {
        if wirelessDebugger == nil {
            wirelessDebugger = WirelessDebugger(hostname, apiKey: apiKey,
                                                timeInterval: timeInterval)
        }
    }

    /// Sends logs if enough time has elapsed.
    private func sendLogsIfReady() {
        let currentTime = UInt64(Date().timeIntervalSince1970 * 1000)
        if Int(currentTime - self.lastSendTime) > self.timeInterval {
            webSocketMessenger?.sendLogDump()
            self.lastSendTime = currentTime
        }
    }
}
