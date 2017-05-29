//
//  ViewController.swift
//  Wireless Debug iOS Test App
//
//  Created by Sumner Evans on 5/28/17.
//  Copyright © 2017 Google Field Session Team. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var LogText: UITextField!
    @IBOutlet weak var AccelerometerToggle: UIButton!
    
    var loggingAccelerometer = false

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
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
    }
    
    @IBAction func crash_pressed() {
        // TODO: crash the app
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

}

