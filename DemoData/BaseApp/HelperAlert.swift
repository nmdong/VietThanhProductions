//
//  Helper.swift
//  WeediesApp
//  Created by Admin on 6/11/22.
//

import Foundation
import Foundation
import UIKit

typealias cancelBlock = (()->(Void))?
typealias dismissBlock = (()->(Void))?

class HelperAlert: UIAlertController {
    static func showAlertWithMessage(_ message: String) {
        let alertController = UIAlertController(title: "", message: message, preferredStyle: .alert)
        let cancelAction = UIAlertAction(title: "OK", style: .default, handler: nil)
        alertController.addAction(cancelAction)
        AppDelegate.shared.window?.rootViewController?.present(alertController, animated: true, completion: nil)
    }
    static func showAlerWithTitle(_ titleString: String? = "",message messageString: String? = "") {
        let alertController = UIAlertController(title: titleString, message: messageString, preferredStyle: .alert)
        let cancelAction = UIAlertAction(title: "OK", style: .default, handler: nil)
        alertController.addAction(cancelAction)
        AppDelegate.shared.window?.rootViewController?.present(alertController, animated: true, completion: nil)
    }
    
    static func showAlerWithTitle(_ titleString: String? = "",message messageString: String? = "",_ controller: UIViewController) {
        let alertController = UIAlertController(title: titleString, message: messageString, preferredStyle: .alert)
        let cancelAction = UIAlertAction(title: "OK", style: .default, handler: nil)
        alertController.addAction(cancelAction)
        controller.present(alertController, animated: true, completion: nil)
    }
    
    static func showAlerWithTitleOK(_ titleString: String? = "",message messageString: String? = "",cancelTitle cancelTitleString: String? = "",_ cancelBlock: dismissBlock = nil,_ controller: UIViewController) {
        let alertController = UIAlertController(title: titleString, message: messageString, preferredStyle: .alert)
        
        if let cancelTitle = cancelTitleString {
            let cancelAction = UIAlertAction(title: cancelTitle, style: .cancel) { action in
                cancelBlock!()
            }
            alertController.addAction(cancelAction)
        }
        controller.present(alertController, animated: true, completion: nil)
    }
    
    static func showAlerWithTitle(_ titleString: String? = "",message messageString: String? = "",cancelTitle cancelTitleString: String? = "",_ cancelBlock: cancelBlock = nil,dismissTitle dismissTitleString: String? = "", dismissBlock: dismissBlock = nil,_ controller: UIViewController) {
        let alertController = UIAlertController(title: titleString, message: messageString, preferredStyle: .alert)
        
        if let cancelTitle = cancelTitleString {
            let cancelAction = UIAlertAction(title: cancelTitle, style: .cancel) { action in
                cancelBlock!()
            }
            alertController.addAction(cancelAction)
        }
        
        if let dismissTitle = dismissTitleString {
            let OKAction = UIAlertAction(title: dismissTitle, style: .default) { action in
                dismissBlock!()
            }
            alertController.addAction(OKAction)
        }
        controller.present(alertController, animated: true, completion: nil)
    }
    
}
