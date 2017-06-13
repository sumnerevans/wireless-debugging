//
//  WebSocketMessenger.swift
//  Wireless Debug iOS Test App
//

import UIKit
import Foundation

/// Handles opening a WebSocket connection and sending the necessary messages
/// across that connection.
class WebSocketMessenger {
    var webSocket = WebSocket()
    var logsToSend: [String] = []
    var connectionRetries = 0
    var verbose: Bool

    /// Create a WebSocket connection to the given socket address and API Key.
    ///
    /// - Parameters:
    ///   - socketAddress: the WebSocket address to connect to
    ///   - apiKey: the API Key provided by the web interface
    init(_ socketAddress: String, apiKey: String, verbose: Bool) {
        self.verbose = verbose
        // When the WebSocket connection opens, send a startSession message.
        self.webSocket.event.open = {
            self.log("WebSocket Connection to \(socketAddress) Opened")

            self.send("startSession", data: [
                "osType": "iOS",
                "apiKey": apiKey,
                "deviceName": UIDevice.current.name,
                "appName": Bundle.main.infoDictionary!["CFBundleName"] as! String,
            ])
            self.connectionRetries = 0
        }

        // If the connection closes, try to reconnect 10 times.
        self.webSocket.event.close = { code, reason, clean in
            self.log("WebSocket Connection Closed \(reason)")

            // Retry the connection 10 times with 2 seconds inbetween retries.
            if self.connectionRetries < 10 {
                DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                    self.webSocket.open(socketAddress)
                }
                self.connectionRetries += 1
            }
        }

        self.webSocket.event.error = { error in
            self.log("Error on WebSocket Connection \(error)")
        }

        // Now actually try to open the WebSocket connection.
        self.webSocket.open(socketAddress)
    }

    /// Send the queued logs across the WebSocket connection.
    public func sendLogDump() {
        if logsToSend.count == 0 || self.webSocket.readyState != .open {
            return
        }

        // Copy the array to avoid possible race conditions when sending/
        // enqueueing logs.
        let logsToSendCopy = logsToSend
        logsToSend.removeAll()

        self.send("logDump", data: [
            "rawLogData": logsToSendCopy.joined(),
        ])
    }

    /// Send the queued logs across the WebSocket connection.
    ///
    /// - Parameter logLine: the NSLog line to enqueue
    public func enqueueLog(logLine: String) {
        logsToSend.append(logLine)
    }

    /// Sends information for an unhandled exception.
    ///
    /// - Parameter exception: the exception to send information for
    public func sendUnhandledException(exception: NSException) {
        var exceptionString = "\(Date.init())---------- BEGIN UNHANDLED EXCEPTION\n"
        exceptionString += "Name: \(exception.name.rawValue)\n"
        exceptionString += "Reason: \(exception.reason ?? "nil")\n"
        exceptionString += "Call Stack:\n\(exception.callStackSymbols.joined(separator: "\n"))"

        print(exceptionString)
        self.send("logDump", data: [
            "rawLogData": exceptionString,
        ])
    }

    /// Send a message over the WebSocket connection.
    ///
    /// - Parameters:
    ///   - messageType: the message type being sent
    ///   - data: a dictionary of the data to send in the message
    private func send(_ messageType: String, data: Dictionary<String, Any>) {
        if self.webSocket.readyState != .open { return }
        var newData = data
        newData["messageType"] = messageType
        self.webSocket.send(JSON(newData))
    }
    
    private func log(_ message: String) {
        if self.verbose {
            NSLog(message)
        }
    }
}
