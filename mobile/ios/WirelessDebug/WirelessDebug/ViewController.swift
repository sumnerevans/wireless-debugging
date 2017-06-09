//
//  ViewController.swift
//  Wireless Debug iOS Test App
//

import Foundation
import UIKit
import CoreMotion

class ViewController: UIViewController, UITextFieldDelegate {
    @IBOutlet weak var LogText: UITextField!
    @IBOutlet weak var AccelerometerToggle: UIButton!
    
    private var loggingAccelerometer = false
    private let manager = CMMotionManager()

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Needed to enable handling of return key on the LogText box.
        LogText.delegate = self
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    
    // Log the text in the LogText box.
    @IBAction func logButton_pressed() {
        NSLog(LogText.text ?? "")
    }
    
    /// Log an exception.
    @IBAction func exception_pressed() {
        do {
            try raiseException();
        } catch let err {
            NSLog("\(err)")
        }
    }
    
    /// Crash the application
    @IBAction func crash_pressed() throws {
        NSException(name:NSExceptionName(rawValue: "ForcedException"), reason:"You pressed the crash button", userInfo:nil).raise()
    }
    
    /// Toggle logging of accelerometer data.
    @IBAction func accelerometerToggle_pressed() {
        if loggingAccelerometer {
            AccelerometerToggle.setTitle("Start Accelerometer Logging", for: .normal)
            manager.stopAccelerometerUpdates()
            loggingAccelerometer = false
        } else {
            AccelerometerToggle.setTitle("Stop Accelerometer Logging", for: .normal)
            print(manager.isAccelerometerAvailable)
            if manager.isAccelerometerAvailable {
                manager.accelerometerUpdateInterval = 0.01
                manager.startAccelerometerUpdates(to: .main) {(data: CMAccelerometerData?, error: Error?) in
                    if let acceleration = data?.acceleration {
                        NSLog("x: \(acceleration.x), y: \(acceleration.y)")
                    }
                }
            }
            loggingAccelerometer = true
        }
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
    
    // ForcedError enum to show how errors are handled.
    enum ForcedError: Error {
        case ForcedError
    }
    
    // I had to make this a function so that I could use it in a do-try-catch block.
    func raiseException() throws {
        throw ForcedError.ForcedError
    }
}

