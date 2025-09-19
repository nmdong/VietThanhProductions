//
//  UIView.swift
//  FreshaForCustomer  Created by Admin on 16/03/2023.
//

import Foundation
import UIKit

extension UIView {
    enum ViewSide {
        case Left, Right, Top, Bottom
    }
    
    func addBorder(toSide side: ViewSide, withColor color: CGColor, andThickness thickness: CGFloat) {
        let border = CALayer()
        border.backgroundColor = color
        
        switch side {
        case .Left: border.frame = CGRect(x: frame.minX, y: frame.minY, width: thickness, height: frame.height); break
        case .Right: border.frame = CGRect(x: self.frame.width, y: 0, width: thickness, height: frame.height); break
        case .Top: border.frame = CGRect(x: frame.minX, y: frame.minY, width: frame.width, height: thickness); break
        case .Bottom: border.frame = CGRect(x: 0, y: self.frame.height - thickness, width: self.frame.width, height: thickness); break
        }
        layer.addSublayer(border)
    }
    
    func addBottomBorder(color: UIColor = #colorLiteral(red: 0.5141947269, green: 0.5141947269, blue: 0.5141947269, alpha: 0.4), margins: CGFloat = 0, borderLineSize: CGFloat = 1) {
        let border = UIView()
        border.backgroundColor = color
        border.translatesAutoresizingMaskIntoConstraints = false
        self.addSubview(border)
        border.addConstraint(NSLayoutConstraint(item: border,
                                                attribute: .height,
                                                relatedBy: .equal,
                                                toItem: nil,
                                                attribute: .height,
                                                multiplier: 1, constant: borderLineSize))
        self.addConstraint(NSLayoutConstraint(item: border,
                                              attribute: .bottom,
                                              relatedBy: .equal,
                                              toItem: self,
                                              attribute: .bottom,
                                              multiplier: 1, constant: 0))
        self.addConstraint(NSLayoutConstraint(item: border,
                                              attribute: .leading,
                                              relatedBy: .equal,
                                              toItem: self,
                                              attribute: .leading,
                                              multiplier: 1, constant: margins))
        self.addConstraint(NSLayoutConstraint(item: border,
                                              attribute: .trailing,
                                              relatedBy: .equal,
                                              toItem: self,
                                              attribute: .trailing,
                                              multiplier: 1, constant: margins))
    }
}

extension UIWindow {
    func topViewController() -> UIViewController? {
        var top = self.rootViewController
        while true {
            if let presented = top?.presentedViewController {
                top = presented
            } else if let nav = top as? UINavigationController {
                top = nav.visibleViewController
            } else if let tab = top as? UITabBarController {
                top = tab.selectedViewController
            } else {
                break
            }
        }
        return top
    }
}
extension UIColor {
    static var startGradient : UIColor {
        return UIColor.init(hexString: "0F3EEF")
    }
    static var endGradient : UIColor {
        return UIColor.init(hexString: "5475F4")
    }
}


class GradientBorderButton: UIButton {
    var gradientColors: [UIColor] = [UIColor.startGradient, UIColor.endGradient] {
        didSet {
            setNeedsLayout()
        }
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()
        
        let gradient = UIImage.gradientImage(bounds: bounds, colors: gradientColors)
        layer.borderColor = UIColor(patternImage: gradient).cgColor
    }
    
}

class GradientBorderView: UIView {
    var gradientColors: [UIColor] = [UIColor.startGradient, UIColor.endGradient] {
        didSet {
            setNeedsLayout()
        }
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()
        
        let gradient = UIImage.gradientImage(bounds: bounds, colors: gradientColors)
        layer.borderColor = UIColor(patternImage: gradient).cgColor
    }
}




extension UIImage {
    static func gradientImage(bounds: CGRect, colors: [UIColor]) -> UIImage {
        let gradientLayer = CAGradientLayer()
        gradientLayer.frame = bounds
        gradientLayer.colors = colors.map(\.cgColor)
        
        // This makes it left to right, default is top to bottom
        gradientLayer.startPoint = CGPoint(x: 0.0, y: 0.5)
        gradientLayer.endPoint = CGPoint(x: 1.0, y: 0.5)
        
        let renderer = UIGraphicsImageRenderer(bounds: bounds)
        
        return renderer.image { ctx in
            gradientLayer.render(in: ctx.cgContext)
        }
    }
}

class GradientButton: UIButton {
    
    private var gradientLayer : CAGradientLayer?
    var gradientColors: [UIColor] = [UIColor.startGradient, UIColor.endGradient] {
        didSet {
            setNeedsLayout()
        }
    }
    
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        commonInit()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        commonInit()
    }
    
    func commonInit() {
        gradientLayer = self.fillGradientLayerWithColor(gradientColors)
        self.clipsToBounds = true
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()
        
        self.gradientLayer?.frame = self.bounds
    }
    
    
    func showGradient(show : Bool) {
        gradientLayer?.isHidden = !show
    }
}


class GradientView: UIView {
    private var gradientLayer : CAGradientLayer?
    var gradientColors: [UIColor] = [UIColor.startGradient, UIColor.endGradient] {
        didSet {
            setNeedsLayout()
        }
    }
    
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        commonInit()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        commonInit()
    }
    
    func commonInit() {
        gradientLayer = self.fillGradientLayerWithColor(gradientColors)
        self.clipsToBounds = true
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()
        self.gradientLayer?.frame = self.bounds
    }
    
    
    func showGradient(show : Bool) {
        gradientLayer?.isHidden = !show
    }
}


public extension UIView {
    
    func fillGradientLayerWithColor(_ colors: [UIColor]) -> CAGradientLayer {
        let gradient: CAGradientLayer = CAGradientLayer()
        gradient.colors = colors.map({ color in
            return color.cgColor
        })
        gradient.locations = [0.0 , 1.0]
        gradient.startPoint = CGPoint(x: 0.0, y: 1.0)
        gradient.endPoint = CGPoint(x: 1.0, y: 1.0)
        gradient.frame = CGRect(x: 0.0, y: 0.0, width: self.bounds.size.width, height: self.bounds.size.height)
        self.layer.insertSublayer(gradient, at: 0)
        return gradient
    }
    
    
    func removeColorGradient() {
        if let layers = self.layer.sublayers , layers.count > 1  {
            layers[0].removeFromSuperlayer()
        }
    }
}
// MARK: - Properties
public extension UIView {

    /// SwifterSwift: Border color of view; also inspectable from Storyboard.
    @IBInspectable var borderColor: UIColor? {
        get {
            guard let color = layer.borderColor else { return nil }
            return UIColor(cgColor: color)
        }
        set {
            guard let color = newValue else {
                layer.borderColor = nil
                return
            }
            // Fix React-Native conflict issue
            guard String(describing: type(of: color)) != "__NSCFType" else { return }
            layer.borderColor = color.cgColor
        }
    }

    /// SwifterSwift: Border width of view; also inspectable from Storyboard.
    @IBInspectable var borderWidth: CGFloat {
        get {
            return layer.borderWidth
        }
        set {
            layer.borderWidth = newValue
        }
    }

    /// SwifterSwift: Corner radius of view; also inspectable from Storyboard.
    @IBInspectable var cornerRadius: CGFloat {
        get {
            return layer.cornerRadius
        }
        set {
            layer.masksToBounds = true
            layer.cornerRadius = abs(CGFloat(Int(newValue * 100)) / 100)
        }
    }

    /// SwifterSwift: Height of view.
    var height: CGFloat {
        get {
            return frame.size.height
        }
        set {
            frame.size.height = newValue
        }
    }

    /// SwifterSwift: Check if view is in RTL format.
    var isRightToLeft: Bool {
        if #available(iOS 10.0, *, tvOS 10.0, *) {
            return effectiveUserInterfaceLayoutDirection == .rightToLeft
        } else {
            return false
        }
    }

    /// SwifterSwift: Take screenshot of view (if applicable).
    var screenshot: UIImage? {
        UIGraphicsBeginImageContextWithOptions(layer.frame.size, false, 0)
        defer {
            UIGraphicsEndImageContext()
        }
        guard let context = UIGraphicsGetCurrentContext() else { return nil }
        layer.render(in: context)
        return UIGraphicsGetImageFromCurrentImageContext()
    }

    /// SwifterSwift: Shadow color of view; also inspectable from Storyboard.
//    @IBInspectable
    var shadowColor: UIColor? {
        get {
            guard let color = layer.shadowColor else { return nil }
            return UIColor(cgColor: color)
        }
        set {
            layer.shadowColor = newValue?.cgColor
        }
    }

    /// SwifterSwift: Shadow offset of view; also inspectable from Storyboard.
//    @IBInspectable
    var shadowOffset: CGSize {
        get {
            return layer.shadowOffset
        }
        set {
            layer.shadowOffset = newValue
        }
    }

    /// SwifterSwift: Shadow opacity of view; also inspectable from Storyboard.
//    @IBInspectable
    var shadowOpacity: Float {
        get {
            return layer.shadowOpacity
        }
        set {
            layer.shadowOpacity = newValue
        }
    }

    /// SwifterSwift: Shadow radius of view; also inspectable from Storyboard.
//    @IBInspectable
    var shadowRadius: CGFloat {
        get {
            return layer.shadowRadius
        }
        set {
            layer.shadowRadius = newValue
        }
    }

    /// SwifterSwift: Size of view.
    var size: CGSize {
        get {
            return frame.size
        }
        set {
            width = newValue.width
            height = newValue.height
        }
    }

    /// SwifterSwift: Get view's parent view controller
    var parentViewController: UIViewController? {
        weak var parentResponder: UIResponder? = self
        while parentResponder != nil {
            parentResponder = parentResponder!.next
            if let viewController = parentResponder as? UIViewController {
                return viewController
            }
        }
        return nil
    }

    /// SwifterSwift: Width of view.
    var width: CGFloat {
        get {
            return frame.size.width
        }
        set {
            frame.size.width = newValue
        }
    }

    /// SwifterSwift: x origin of view.
    // swiftlint:disable:next identifier_name
    var x: CGFloat {
        get {
            return frame.origin.x
        }
        set {
            frame.origin.x = newValue
        }
    }

    /// SwifterSwift: y origin of view.
    // swiftlint:disable:next identifier_name
    var y: CGFloat {
        get {
            return frame.origin.y
        }
        set {
            frame.origin.y = newValue
        }
    }

}
