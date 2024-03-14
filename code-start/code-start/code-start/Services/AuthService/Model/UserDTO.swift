//
//  UserDTO.swift
//  code-start
//
//  Created by Тимур Калимуллин on 23.02.2024.
//

import Foundation

struct UserDTO: Decodable {
    let nickname: String
    let email: String
    //let hashedPassword: String
    let id: String
    let userLevel: String
    //let isPremium: Bool
    //let disabled: Bool

    enum CodingKeys: String, CodingKey {
        case nickname
        case email
        //case hashedPassword = "hashed_password"
        case id
        case userLevel = "user_level"
        //case isPremium = "is_premium"
        //case disabled
    }
}
