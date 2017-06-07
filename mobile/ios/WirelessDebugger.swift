//
//  WirelessDebugger.swift
//  Wireless Debug iOS Test App
//
//  Created by Sumner Evans on 6/6/17.
//  Copyright © 2017 Google Field Session Team. All rights reserved.
//

import Foundation

class WirelessDebugger {
    
    init() {
    }
    
    static func start() {
        //let loggerThread = Thread.init(target:self, selector:#selector(logCapture), object:nil)
        //loggerThread.start()
        WirelessDebugger().openConsolePipe()
    }
    
    func openConsolePipe() {
        print("here")
        let inputPipe = Pipe()
        dup2(STDOUT_FILENO, inputPipe.fileHandleForWriting.fileDescriptor)
        var i = 0
        while i < 1 {
            let x = inputPipe.fileHandleForWriting.availableData
            print("here")
            print(x.count)
            usleep(100000)
            i += 1
        }
    }
    
    @objc static func logCapture(object: AnyObject?) {
        while true {
            NSLog("b")
            usleep(100000)
        }
    }
}
