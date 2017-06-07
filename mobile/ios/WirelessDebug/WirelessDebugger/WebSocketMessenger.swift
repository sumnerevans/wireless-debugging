//
//  WebSocketMessenger.swift
//  Wireless Debug iOS Test App
//

import Foundation

class WebSocketMessenger {
    var ws: WebSocket?

    init(_ socketAddress: String) {
        self.ws = WebSocket(socketAddress)
        self.ws!.event.open = {
            print("opened")
        }
        self.ws!.event.close = { code, reason, clean in
            print("close")
        }
        self.ws!.event.error = { error in
            print("error \(error)")
        }
    }
}
