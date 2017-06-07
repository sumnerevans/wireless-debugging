//
//  WirelessDebugger.swift
//  Wireless Debug iOS Test App
//

import Foundation

class WirelessDebugger {
    
    private static var wirelessDebugger: WirelessDebugger?
    
    private var webSocketMessenger: WebSocketMessenger?
    
    init(_ hostname: String, timeInterval: Int) {
        webSocketMessenger = WebSocketMessenger("ws://\(hostname)/ws")
        let stderrPipe = Pipe()
        dup2(stderrPipe.fileHandleForWriting.fileDescriptor, fileno(stderr))
        
        DispatchQueue.global().async {
            while(true) {
                let data = stderrPipe.fileHandleForReading.availableData
                DispatchQueue.main.async {
                    let logData = String(data: data, encoding: String.Encoding(rawValue: String.Encoding.utf8.rawValue)) ?? ""
                    print(logData)
                }
            }
        }
    }
    
    static func start(hostname: String, timeInterval: Int = 100) {
        if wirelessDebugger == nil {
            wirelessDebugger = WirelessDebugger(hostname, timeInterval: timeInterval)
        }
    }
}
