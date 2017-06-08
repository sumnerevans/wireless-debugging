//
//  WirelessDebugger.swift
//  Wireless Debug iOS Test App
//

import Foundation

class WirelessDebugger {
    
    private static var wirelessDebugger: WirelessDebugger?
    
    private var webSocketMessenger: WebSocketMessenger?
    private var lastSendTime: UInt64 = 0
    private var timeInterval: Int
    
    init(_ hostname: String, apiKey: String, timeInterval: Int) {
        self.webSocketMessenger = WebSocketMessenger("ws://\(hostname)/ws", apiKey: apiKey)
        self.timeInterval = timeInterval
        
        let stderrPipe = Pipe()
        dup2(stderrPipe.fileHandleForWriting.fileDescriptor, fileno(stderr))
        
        DispatchQueue.global().async {
            while true {
                let data = stderrPipe.fileHandleForReading.availableData
                DispatchQueue.main.async {
                    // Capture the log
                    let logData = String(data: data, encoding: String.Encoding(rawValue: String.Encoding.utf8.rawValue)) ?? ""
                    self.webSocketMessenger!.enqueueLog(logLine: logData)
                    print(logData)
                }
            }
        }
        
        DispatchQueue.global().async {
            while true {
                self.sendLogsIfReady()
                usleep(10000) // sleep for 10 ms, usleep accepts microseconds
            }
        }
    }
    
    
    static func start(hostname: String, apiKey: String, timeInterval: Int = 100) {
        if wirelessDebugger == nil {
            wirelessDebugger = WirelessDebugger(hostname, apiKey: apiKey, timeInterval: timeInterval)
        }
    }
    
    private func sendLogsIfReady() {
        let currentTime = UInt64(Date().timeIntervalSince1970 * 1000)
        if Int(currentTime - self.lastSendTime) > self.timeInterval {
            webSocketMessenger?.sendLogDump()
            self.lastSendTime = currentTime
        }
    }
}
