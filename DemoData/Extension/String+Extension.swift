//
//  String+Extension.swift
//  FreshaForCustomer  Created by Admin on 6/15/22.
//

import Foundation
import UIKit
let TimeZone_UTC = TimeZone(identifier: "UTC")
extension String {
    func height(withConstrainedWidth width: CGFloat, font: UIFont) -> CGFloat {
//        let constraintRect = CGSize(width: width, height: .greatestFiniteMagnitude)
//        let boundingBox = self.boundingRect(with: constraintRect, options: .usesLineFragmentOrigin, attributes: [NSAttributedString.Key.font: font], context: nil)
//        
//        return boundingBox.height
        
        let constraintRect = CGSize(width: width, height: .greatestFiniteMagnitude)
                let boundingBox = self.boundingRect(
                    with: constraintRect,
                    options: [.usesLineFragmentOrigin, .usesFontLeading],
                    attributes: [.font: font],
                    context: nil
                )
                return ceil(boundingBox.height)
    }
    
    func width(withConstrainedHeight height: CGFloat, font: UIFont) -> CGFloat {
        let constraintRect = CGSize(width: .greatestFiniteMagnitude, height: height)
        let boundingBox = self.boundingRect(with: constraintRect, options: .usesLineFragmentOrigin, attributes: [NSAttributedString.Key.font: font], context: nil)
        
        return boundingBox.width
    }
    
    private func toDate(withFormat format: String = "yyyy-MM-dd") -> Date? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = format
        dateFormatter.timeZone = TimeZone(identifier: "UTC")
        guard let date = dateFormatter.date(from: self) else {
            return nil
        }
        return date
    }
    
    func toDateNew() -> Date {
        let array: [String] =  [
            "yyyy-MM-dd'T'HH:mm:ssZZZZZ",
            "yyyy'-'MM'-'dd'T'HH':'mm':'ssZ",
            "yyyy'-'MM'-'dd'T'HH':'mm':'ss'.'SSSZ",
            "yyyy-MM-dd'T'HH:mm:ss.SSSZ",
            "yyyy-MM-dd HH:mm:ss",
            "yyyy-MM-dd HH:mm a",
            "yyyy-MM-dd HH:mm",
            "yyyy-MM-dd",
            "h:mm:ss A",
            "h:mm A",
            "MM/dd/yyyy",
            "MM/dd/yyyy HH:mm:ss",
            "MMMM d, yyyy",
            "MMMM d, yyyy LT",
            "dddd, MMMM D, yyyy LT",
            "yyyyyy-MM-dd",
            "yyyy-MM-dd",
            "yyyy-'W'ww-E",
            "GGGG-'['W']'ww-E",
            "yyyy-'W'ww",
            "GGGG-'['W']'ww",
            "yyyy'W'ww",
            "yyyy-ddd",
            "HH:mm:ss.SSSS",
            "HH:mm:ss",
            "HH:mm",
            "HH:mm A",
            "HH:mm a",
            "HH"
        ]
        for day in array {
            if let date = self.toDate(withFormat: day) as Date?  {
                return date
            }
        }
        return Date()
    }
    
    func htmlToAttributedString() -> NSAttributedString? {
        guard let data = self.data(using: .utf8) else { return nil }
        do {
            return try NSAttributedString(data: data,
                                          options: [.documentType: NSAttributedString.DocumentType.html,
                                                    .characterEncoding: String.Encoding.utf8.rawValue],
                                          documentAttributes: nil)
        } catch {
            print("Error parsing HTML: \(error)")
            return nil
        }
    }
    
}
extension Double {
    func asString(style: DateComponentsFormatter.UnitsStyle) -> String {
        if self < 10 {
            return "0\(Int(self))"
        }
        let formatter = DateComponentsFormatter()
        if self >= 3600 {
            formatter.allowedUnits = [.hour, .minute, .second]
        }else if self >= 60 {
            formatter.allowedUnits = [.minute, .second]
        }else {
            formatter.allowedUnits = [ .second]
        }
        formatter.unitsStyle = style
        formatter.zeroFormattingBehavior = .pad
        return formatter.string(from: self) ?? ""
    }
}
extension Date {
    func toString(format: String = "yyyy-MM-dd", _ timeZone : TimeZone? = nil) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeZone = timeZone ?? TimeZone.current
        formatter.dateFormat = format
        return formatter.string(from: self)
    }
    
    func toTimeString() -> String {
        let formatter = DateFormatter()
        formatter.timeStyle = .short
        formatter.dateFormat = "HH:mm"
        formatter.locale = Locale.current
        return formatter.string(from: self)
    }
    
    
//    func timeSinceDate(fromDate: Date) -> String {
//        let earliest = self < fromDate ? self  : fromDate
//        let latest = (earliest == self) ? fromDate : self
//        
//        let components:DateComponents = Calendar.current.dateComponents([.minute,.hour,.day,.weekOfYear,.month,.year,.second], from: earliest, to: latest)
//        let year = components.year  ?? 0
//        let month = components.month  ?? 0
//        let week = components.weekOfYear  ?? 0
//        let day = components.day ?? 0
//        let hours = components.hour ?? 0
//        let minutes = components.minute ?? 0
//        let seconds = components.second ?? 0
//        
//        
//        if year >= 2{
//            return "\(year) years ago"
//        }else if (year >= 1){
//            return "1 year ago"
//        }else if (month >= 2) {
//            return "\(month) \(localized("textMonthago"))"
//        }else if (month >= 1) {
//            return localized("text1Monthago")
//        }else  if (week >= 2) {
//            return "\(week) weeks ago"
//        } else if (week >= 1){
//            return localized("text1weekago")
//        } else if (day >= 2) {
//            return "\(day) \(localized("textdaysago"))"
//        } else if (day >= 1){
//            return localized("text1daysago")
//        } else if (hours >= 2) {
//            return "\(hours) \(localized("texthourssago"))"
//        } else if (hours >= 1){
//            return localized("text1hourssago")
//        } else if (minutes >= 2) {
//            return "\(minutes) \(localized("textMinutessago"))"
//        } else if (minutes >= 1){
//            return localized("text1Minutessago")
//        } else if (seconds >= 3) {
//            return "\(seconds) \(localized("textSecondsago"))"
//        } else {
//            return localized("textJustnow")
//        }
//    }
}

extension NSMutableAttributedString {
    
    public func color(string : String, color : UIColor)  -> Self {
        let attributedString = NSAttributedString.init(string: string, attributes: [NSAttributedString.Key.foregroundColor : color])
        self.append(attributedString)
        return self
    }
    
    public func backgroundColorColor(string : String, color : UIColor)  -> Self {
        let attributedString = NSAttributedString.init(string: string, attributes: [NSAttributedString.Key.backgroundColor : color])
        self.append(attributedString)
        return self
    }
    
    func addFont(string : String, font : UIFont){
        
        let currentString = NSString.init(string: self.string)
        self.addAttribute(NSAttributedString.Key.font, value: font, range: currentString.range(of: string))
    }
    
    func addColor(string : String, color : UIColor){
        let currentString = NSString.init(string: self.string)
        self.addAttribute(NSAttributedString.Key.foregroundColor, value: color, range: currentString.range(of: string))
    }
    
    func addBackgroundColor(string : String, color : UIColor){
        let currentString = NSString.init(string: self.string)
        self.addAttribute(NSAttributedString.Key.backgroundColor, value: color, range: currentString.range(of: string))
    }
    
    func addUnderline(string : String){
        let currentString = NSString.init(string: self.string)
        self.addAttribute(NSAttributedString.Key.underlineStyle, value: NSUnderlineStyle.single.rawValue, range: currentString.range(of: string))
    }
    func addStrikethroughStyle(string : String){
        let currentString = NSString.init(string: self.string)
        self.addAttribute(NSAttributedString.Key.strikethroughStyle, value: NSUnderlineStyle.single.rawValue, range: currentString.range(of: string))
    }
}

extension String {
    var isValidPhone: Bool {
        return self.westernArabicNumeralsOnly.validateRegex("^[0-9]{10}$")
    }
    
    func validateRegex(_ typeRegex: String) -> Bool {
        
        if self.isEmpty {
            return false
        }
        
        let resultTest  = NSPredicate(format:"SELF MATCHES %@", typeRegex)
        return resultTest.evaluate(with: self)
    }
    
    var westernArabicNumeralsOnly: String {
        let pattern = UnicodeScalar("0")..."9"
        return String(unicodeScalars
            .flatMap { pattern ~= $0 ? Character($0) : nil })
    }
}

extension String {
    
    func fotmatTimeWithFormat(format: String) -> String {
        let dateFormatterGet = DateFormatter()
        dateFormatterGet.dateFormat = "yyyy-MM-dd HH:mm:ss"
        
        let dateFormatterPrint = DateFormatter()
        dateFormatterPrint.dateFormat = format
        
        let date: Date? = dateFormatterGet.date(from: self)
        let stringDate = dateFormatterPrint.string(from: date!)
        
        return stringDate
    }
    
    func fotmatDateFromString() -> Date? {
        let dateFormatterGet = DateFormatter()
        dateFormatterGet.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let date: Date? = dateFormatterGet.date(from: self)
        
        return date
    }
    
    func getTimeFromDate() -> String? {
        guard let date = self.fotmatDateFromString() else { return "" }
        let calendar = Calendar.current
        let hour = calendar.component(.hour, from: date)
        let minute = calendar.component(.minute, from: date)
        
        let strMinutes = minute != 0 ? "\(minute)" : "00"
        
        return "\(hour):\(strMinutes)"
    }
    
    func getHourFromDate() -> Int {
        guard let date = self.fotmatDateFromString() else { return 0 }
        let calendar = Calendar.current
        let hour = calendar.component(.hour, from: date)
        
        return hour
    }
    
    func getMinutesFromDate() -> Int {
        guard let date = self.fotmatDateFromString() else { return 0 }
        let calendar = Calendar.current
        let minute = calendar.component(.minute, from: date)
        
        return minute
    }
    
    
    
}
extension String {
    
    func unFormatnumberUSA() -> String {
        var number = self
        number = number.replacingOccurrences(of: "(", with: "")
        number = number.replacingOccurrences(of: ")", with: "")
        //        number = number.replacingOccurrences(of: "-", with: "")
        number = number.replacingOccurrences(of: " ", with: "")
        number = number.replacingOccurrences(of: "$", with: "")
        number = number.replacingOccurrences(of: "￥", with: "")
        number = number.replacingOccurrences(of: ",", with: ".")
        return number
    }
    
    func unNumberFormatterPhoneUS() -> String {
        var number = self
        //        number = number.replacingOccurrences(of: "+", with: "")
        number = number.replacingOccurrences(of: "(", with: "")
        number = number.replacingOccurrences(of: ")", with: "")
        number = number.replacingOccurrences(of: "-", with: "")
        number = number.replacingOccurrences(of: " ", with: "")
        return number
    }
    
    func validateEmail() -> Bool {
        let emailRegEx = "^.+@([A-Za-z0-9-]+\\.)+[A-Za-z]{2}[A-Za-z]*$"
        
        let emailTest = NSPredicate(format:"SELF MATCHES %@", emailRegEx)
        return emailTest.evaluate(with: self)
    }
    
    var isNotEmpty: Bool {
        return !self.isEmpty
    }
    
    func validatePhone() -> Bool {
        if self.count != 10 {
            return false
        }
        let phoneRegex = "^[0-9+]{0,1}+[0-9]{5,16}$"
        let phoneTest = NSPredicate(format: "SELF MATCHES %@", phoneRegex)
        return phoneTest.evaluate(with: self)
    }
    
}
