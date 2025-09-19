//
//  AppDelegate.swift
//  DemoData
//
//  Created by Admin on 19-09-25.
//

import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    static var shared: AppDelegate {
        guard let delegate = UIApplication.shared.delegate as? AppDelegate else {
            fatalError("AppDelegae not found. This could never happen!")
        }
        return delegate
    }
    var window: UIWindow?
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        window = UIWindow(frame: UIScreen.main.bounds)
        self.gotoGuide()
        window?.makeKeyAndVisible()
        return true
    }
    func gotoGuide()  {
        self.window?.rootViewController = LoginViewController()
    }
    // MARK: UISceneSession Lifecycle
    
    
    
    
}

