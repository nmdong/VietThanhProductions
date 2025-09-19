//
//  Networking+Extension.swift
//  WeediesApp
//  Created by Admin on 6/11/22.
//

import Foundation
extension Dictionary {
    func toCodableObject<T: Codable>() -> T? {
        
        if let jsonData = try? JSONSerialization.data(withJSONObject: self, options: .prettyPrinted) {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .useDefaultKeys
            if let obj = try? decoder.decode(T.self, from: jsonData) {
                return obj
            }
            
            return nil
        }
        return nil
    }
}

extension Data {
    func toCodableObject<T: Codable>() -> T? {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .useDefaultKeys
        if let obj = try? decoder.decode(T.self, from: self) {
            return obj
        }
        return nil
    }
    
}
