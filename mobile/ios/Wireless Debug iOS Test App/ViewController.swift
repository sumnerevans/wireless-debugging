//
//  ViewController.swift
//  Wireless Debug iOS Test App
//
//  Created by Sumner Evans on 5/28/17.
//  Copyright © 2017 Google Field Session Team. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UITextFieldDelegate {
    @IBOutlet weak var LogText: UITextField!
    @IBOutlet weak var AccelerometerToggle: UIButton!
    
    var loggingAccelerometer = false

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        LogText.delegate = self
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    @IBAction func logButton_pressed() {
        NSLog(LogText.text ?? "")
    }
    
    @IBAction func exception_pressed() {
        // TODO: throw an exception
        do {
            try raiseException();
        } catch let err {
            NSLog("\(err)")
        }
    }
    
    @IBAction func crash_pressed() throws {
        NSException(name:NSExceptionName(rawValue: "ForcedException"), reason:"You pressed the crash button", userInfo:nil).raise()
    }
    
    @IBAction func accelerometerToggle_pressed() {
        if loggingAccelerometer {
            AccelerometerToggle.setTitle("Start Accelerometer Logging", for: .normal)
            // TODO: stop accelerometer logging
        } else {
            AccelerometerToggle.setTitle("Stop Accelerometer Logging", for: .normal)
            // TODO: start accelerometer logging
        }
        
        loggingAccelerometer = !loggingAccelerometer
    }
    
    /// Handle enter on the log text field.
    ///
    /// - parameters:
    ///   - _ The text field whose return button was pressed.
    ///
    /// - returns: true if the text field should implement its default behavior for the return button; otherwise, false.
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        self.logButton_pressed()
        return true
    }
    
    enum ForcedError: Error {
        case ForcedError
    }
    
    func raiseException() throws {
        throw ForcedError.ForcedError
    }
}

