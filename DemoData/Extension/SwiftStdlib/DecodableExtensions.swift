// DecodableExtensions.swift - Copyright 2020 SwifterSwift

#if canImport(Foundation)
import Foundation
#endif

public extension Decodable {
    #if canImport(Foundation)
    /// SwifterSwift: Parsing the model in Decodable type.
    /// - Parameters:
    ///   - data: Data.
    ///   - decoder: JSONDecoder. Initialized by default.
    init?(from data: Data, using decoder: JSONDecoder = .init()) {
        guard let parsed = try? decoder.decode(Self.self, from: data) else { return nil }
        self = parsed
    }
    #endif
}

extension Encodable {
  func asDictionary() throws -> [String: Any] {
    let data = try JSONEncoder().encode(self)
    guard let dictionary = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as? [String: Any] else {
      throw NSError()
    }
    return dictionary
  }
}
