//
//  WebSocketMessenger.swift
//  Wireless Debug iOS Test App
//

import UIKit
import Foundation

class WebSocketMessenger {
    var ws: WebSocket?
    var logsToSend: [String] = []

    init(_ socketAddress: String, apiKey: String) {
        self.ws = WebSocket(socketAddress)
        self.ws!.event.open = {
            NSLog("WebSocket Connection to \(socketAddress) Opened")
            
            self.send("startSession", data: [
                "osType": "iOS",
                "apiKey": apiKey,
                "deviceName": UIDevice.current.name,
                "appName": Bundle.main.infoDictionary!["CFBundleName"] as! String,
            ])
        }

        self.ws!.event.close = { code, reason, clean in
            NSLog("WebSocket Connection Closed \(reason)")
        }

        self.ws!.event.error = { error in
            NSLog("Error on WebSocket Connection \(error)")
        }
    }
    
    public func sendLogDump() {
        if logsToSend.count == 0 {
            return
        }
        
        // Copy the array to avoid possible race conditions when sending/enqueueing logs.
        let logsToSendCopy = logsToSend
        logsToSend.removeAll()
        
        self.send("logDump", data: [
            "rawLogData": logsToSendCopy.joined(separator: "\n"),
        ])
    }
    
    public func enqueueLog(logLine: String) {
        logsToSend.append(logLine)
    }
    
    private func send(_ messageType: String, data: Dictionary<String, Any>) {
        var newData = data
        newData["messageType"] = messageType
        self.ws!.send(JSON(newData))
    }
}
