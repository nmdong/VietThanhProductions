//
//  Number+Extension.swift
//  FreshaForCustomer  Created by Admin on 11/04/2023.
//

import Foundation
extension Formatter {
    static let withDot: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.groupingSeparator = "."
        return formatter
    }()
}

extension Numeric {
    func formatnumber() -> String {
        return Formatter.withDot.string(for: self) ?? ""
    }
    func formatnumberVND() -> String {
        return "$" + (Formatter.withDot.string(for: self) ?? "0")
    }
    func formatVNDDiscount() -> String {
        if let value = (Formatter.withDot.string(for: self)), value != "0" {
            return "-$\(value)"
        } else {
            return "0"
        }
        
    }
}

extension Double {
    func round(to places: Int) -> Double {
        let divisor = pow(10.0, Double(places))
        return (self * divisor).rounded() / divisor
    }
}

extension Int {
    func toID() -> String {
        return "ID #\(self)" 
    }
}
