//
//  Viewcontroller+Ext.swift
//  Tourist
//
//  Created by Admin 11/23/18.
//  Copyright © 2018 TVT25. All rights reserved.
//

import Foundation
import UIKit

// MARK: - Methods
public extension UIViewController {
    
    
    
    func hideKeyboardWhenTappedAround() {
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIViewController.dismissKeyboard))
        tap.cancelsTouchesInView = false
        view.addGestureRecognizer(tap)
    }
    
    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
    
    public class func getTopViewController(from window: UIWindow? = UIApplication.shared.keyWindow) -> UIViewController? {
        return getTopViewController(from: window?.rootViewController)
    }
    
    public func getTopViewController_(from window: UIWindow? = UIApplication.shared.keyWindow) -> UIViewController? {
        return UIViewController.getTopViewController(from: window?.rootViewController)
    }
    
    
    
    class func getTopViewController(from rootVC: UIViewController?) -> UIViewController? {
        if let nav = rootVC as? UINavigationController, let navFirst = nav.visibleViewController {
            return getTopViewController(from: navFirst)
        } else if let tab = rootVC as? UITabBarController, let selectedTab = tab.selectedViewController {
            return getTopViewController(from: selectedTab)
        } else if let split = rootVC as? UISplitViewController, let splitLast = split.viewControllers.last {
            return getTopViewController(from: splitLast)
        } else if let presented = rootVC?.presentedViewController {
            return getTopViewController(from: presented)
        }
        
        return rootVC
    }
}

extension UINavigationController {
    func popToRootViewController(animated:Bool = true, completion: @escaping ()->()) {
        CATransaction.begin()
        CATransaction.setCompletionBlock(completion)
        self.popToRootViewController(animated: animated)
        CATransaction.commit()
    }
    
    func popToViewController(ofClass: AnyClass, animated: Bool = true) {
        if let vc = viewControllers.last(where: { $0.isKind(of: ofClass) }) {
            popToViewController(vc, animated: animated)
        }
    }
    
    func canPopToViewController(ofClass: AnyClass) -> Bool {
        if let _ = viewControllers.last(where: { $0.isKind(of: ofClass) }) {
            return true
        } else {
            return false
        }
    }
}

extension UITapGestureRecognizer {

    func didTapAttributedTextInLabel(label: UILabel, inRange targetRange: NSRange) -> Bool {
        // Create instances of NSLayoutManager, NSTextContainer and NSTextStorage
        let layoutManager = NSLayoutManager()
        let textContainer = NSTextContainer(size: CGSize.zero)
        let textStorage = NSTextStorage(attributedString: label.attributedText!)

        // Configure layoutManager and textStorage
        layoutManager.addTextContainer(textContainer)
        textStorage.addLayoutManager(layoutManager)

        // Configure textContainer
        textContainer.lineFragmentPadding = 0.0
        textContainer.lineBreakMode = label.lineBreakMode
        textContainer.maximumNumberOfLines = label.numberOfLines
        let labelSize = label.bounds.size
        textContainer.size = labelSize

        // Find the tapped character location and compare it to the specified range
        let locationOfTouchInLabel = self.location(in: label)
        let textBoundingBox = layoutManager.usedRect(for: textContainer)
        let textContainerOffset = CGPoint(x: (labelSize.width - textBoundingBox.size.width) * 0.5 - textBoundingBox.origin.x, y: (labelSize.height - textBoundingBox.size.height) * 0.5 - textBoundingBox.origin.y)

        let locationOfTouchInTextContainer = CGPoint(x: locationOfTouchInLabel.x - textContainerOffset.x, y: locationOfTouchInLabel.y - textContainerOffset.y)
        let indexOfCharacter = layoutManager.characterIndex(for: locationOfTouchInTextContainer, in: textContainer, fractionOfDistanceBetweenInsertionPoints: nil)
        return NSLocationInRange(indexOfCharacter, targetRange)
    }
}
