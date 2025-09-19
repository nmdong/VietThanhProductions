// LocaleExtensions.swift - Copyright 2020 SwifterSwift

#if canImport(Foundation)
import Foundation
import UIKit

// MARK: - Properties

public extension Locale {
    /// SwifterSwift: UNIX representation of locale usually used for normalizing.
    static var posix: Locale {
        return Locale(identifier: "en_US_POSIX")
    }

    /// SwifterSwift: Returns bool value indicating if locale has 12h format.
    var is12HourTimeFormat: Bool {
        let dateFormatter = DateFormatter()
        dateFormatter.timeStyle = .short
        dateFormatter.dateStyle = .none
        dateFormatter.locale = self
        let dateString = dateFormatter.string(from: Date())
        return dateString.contains(dateFormatter.amSymbol) || dateString.contains(dateFormatter.pmSymbol)
    }
}

// MARK: - Functions

public extension Locale {
    /// SwifterSwift: Get the flag emoji for a given country region code.
    /// - Parameter isoRegionCode: The IOS region code.
    ///
    /// Adapted from https://stackoverflow.com/a/30403199/1627511
    /// - Returns: A flag emoji string for the given region code (optional).
    static func flagEmoji(forRegionCode isoRegionCode: String) -> String? {
        #if !os(Linux)
        guard isoRegionCodes.contains(isoRegionCode) else { return nil }
        #endif

        return isoRegionCode.unicodeScalars.reduce(into: String()) {
            guard let flagScalar = UnicodeScalar(UInt32(127_397) + $1.value) else { return }
            $0.unicodeScalars.append(flagScalar)
        }
    }
}

#endif
//extension UILabel {
//    
//    @IBInspectable var localizedText: String {
//        get { return "" }
//        set(key) {
//            text = localized(key)
//        }
//    }
//}
//
//extension UINavigationItem {
//    
//    @IBInspectable var localizedTitle: String {
//        get { return "" }
//        set(key) {
//            title = localized(key)
//        }
//    }
//}
//
//extension UIButton {
//    
//    @IBInspectable var localizedTitle: String {
//        get { return "" }
//        set(key) {
//            self.setTitle(localized(key), for: .normal)
//        }
//        
//    }
//}
//extension UITextField {
//    
//    @IBInspectable var localizedPlaceholder: String {
//        get { return "" }
//        set(key) {
//            placeholder = localized(key)
//        }
//    }
//    
//    @IBInspectable var localizedText: String {
//        get { return "" }
//        set(key) {
//            text = localized(key)
//        }
//    }
//}
//
//extension UITextView {
//    
//    @IBInspectable var localizedText: String {
//            get { return "" }
//            set(key) {
//                text = localized(key)
//            }
//        }
//}
//
//extension UISearchBar {
//    
//    @IBInspectable var localizedPrompt: String {
//        get { return "" }
//        
//        set(key) {
//            self.prompt = localized(key)
//        }
//    }
//    
//    @IBInspectable var localizedPlaceholder: String {
//        get { return "" }
//        set(key) {
////            title(localized(key), for: .normal)
//        }
//    }
//}

extension UILabel {

    enum InterFont: Int {
        case bold, medium, regular, black, blackItalic, boldItalic, extraBold, extraBoldItalic,
             extraLight, extraLightItalic, italic, light, lightItalic, mediumItalic, semiBold,
             semiBoldItalic, thin, thinItalic
        
        var fontName: String {
            switch self {
            case .bold: return "Inter-Bold"
            case .medium: return "Inter-Medium"
            case .regular: return "Inter-Regular"
            case .black: return "Inter-Black"
            case .blackItalic: return "Inter-BlackItalic"
            case .boldItalic: return "Inter-BoldItalic"
            case .extraBold: return "Inter-ExtraBold"
            case .extraBoldItalic: return "Inter-ExtraBoldItalic"
            case .extraLight: return "Inter-ExtraLight"
            case .extraLightItalic: return "Inter-ExtraLightItalic"
            case .italic: return "Inter-Italic"
            case .light: return "Inter-Light"
            case .lightItalic: return "Inter-LightItalic"
            case .mediumItalic: return "Inter-MediumItalic"
            case .semiBold: return "Inter-SemiBold"
            case .semiBoldItalic: return "Inter-SemiBoldItalic"
            case .thin: return "Inter-Thin"
            case .thinItalic: return "Inter-ThinItalic"
            }
        }
    }
    
    @IBInspectable var interFont: Int {
        get { return 0 }
        set {
            let selectedFont = InterFont(rawValue: newValue) ?? .regular
            self.font = UIFont(name: selectedFont.fontName, size: self.font.pointSize)
        }
    }

    @IBInspectable var fontSize: CGFloat {
        get { return self.font.pointSize }
        set {
            self.font = self.font.withSize(newValue)
        }
    }
}
